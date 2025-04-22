import NextAuth from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import GoogleProvider from 'next-auth/providers/google';
import GithubProvider from 'next-auth/providers/github';

const handler = NextAuth({
        providers: [
                GoogleProvider({
                        clientId: process.env.GOOGLE_CLIENT_ID!,
                        clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
                }),
                GithubProvider({
                        clientId: process.env.GITHUB_ID!,
                        clientSecret: process.env.GITHUB_SECRET!,
                }),
                CredentialsProvider({
                        name: 'Credentials',
                        credentials: {
                                email: { label: 'Email', type: 'email' },
                                password: { label: 'Password', type: 'password' },
                        },
                        async authorize(credentials) {
                                if (!credentials?.email || !credentials?.password) {
                                        throw new Error('Email and password are required');
                                }

                                // Call Django API to authenticate
                                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login/`, {
                                        method: 'POST',
                                        headers: {
                                                'Content-Type': 'application/json',
                                        },
                                        body: JSON.stringify({
                                                email: credentials.email,
                                                password: credentials.password,
                                        }),
                                });

                                const data = await response.json();

                                if (!response.ok) {
                                        throw new Error(data.detail || 'Authentication failed');
                                }

                                // Return user data
                                return {
                                        id: data.user.id.toString(),
                                        email: data.user.email,
                                        name: `${data.user.first_name} ${data.user.last_name}`,
                                        accessToken: data.access,
                                        refreshToken: data.refresh,
                                };
                        },
                }),
        ],
        callbacks: {
                async signIn({ user, account, profile }) {
                        if (account?.provider === 'google' || account?.provider === 'github') {
                                try {
                                        // Generate a secure password
                                        const securePassword = `${account.provider
                                                .charAt(0)
                                                .toUpperCase()}${account.provider.slice(1)}${
                                                user.email.split('@')[0]
                                        }123`;

                                        // Get profile image if available
                                        const imageUrl = user.image || null;

                                        // First check if user exists by trying to login directly
                                        let loginResponse = await fetch(
                                                `${process.env.NEXT_PUBLIC_API_URL}/api/auth/login/`,
                                                {
                                                        method: 'POST',
                                                        headers: {
                                                                'Content-Type': 'application/json',
                                                        },
                                                        body: JSON.stringify({
                                                                email: user.email,
                                                                password: securePassword,
                                                        }),
                                                },
                                        );

                                        let loginData = await loginResponse.json();

                                        // If login successful, user exists and we're done
                                        if (loginResponse.ok) {
                                                user.accessToken = loginData.access;
                                                user.refreshToken = loginData.refresh;
                                                user.id = loginData.user.id.toString();
                                                return true;
                                        }

                                        // If login failed, try to register (user might not exist)
                                        const registerResponse = await fetch(
                                                `${process.env.NEXT_PUBLIC_API_URL}/api/auth/register/`,
                                                {
                                                        method: 'POST',
                                                        headers: {
                                                                'Content-Type': 'application/json',
                                                        },
                                                        body: JSON.stringify({
                                                                email: user.email,
                                                                first_name: user.name?.split(' ')[0] || '',
                                                                last_name:
                                                                        user.name?.split(' ').slice(1).join(' ') || '',
                                                                // Phone is now optional, so we don't need to send it
                                                                imageUrl: imageUrl,
                                                                password: securePassword,
                                                                password_confirm: securePassword,
                                                        }),
                                                },
                                        );

                                        const registerData = await registerResponse.json();

                                        // If registration successful, try to login
                                        if (registerResponse.ok) {
                                                loginResponse = await fetch(
                                                        `${process.env.NEXT_PUBLIC_API_URL}/api/auth/login/`,
                                                        {
                                                                method: 'POST',
                                                                headers: {
                                                                        'Content-Type': 'application/json',
                                                                },
                                                                body: JSON.stringify({
                                                                        email: user.email,
                                                                        password: securePassword,
                                                                }),
                                                        },
                                                );

                                                loginData = await loginResponse.json();

                                                if (loginResponse.ok) {
                                                        user.accessToken = loginData.access;
                                                        user.refreshToken = loginData.refresh;
                                                        user.id = loginData.user.id.toString();
                                                        return true;
                                                }
                                        }
                                        // If user already exists but we couldn't login with that password,
                                        // this probably means user was registered with a different method
                                        else if (registerData.email && registerData.email[0].includes('exists')) {
                                                throw new Error(
                                                        'User exists but needs different authentication method',
                                                );
                                        }

                                        throw new Error(loginData.detail || 'Authentication failed');
                                } catch (error) {
                                        console.error('Social auth error:', error);
                                        throw new Error('Authentication failed');
                                }
                        }
                        return true;
                },
                async jwt({ token, user }) {
                        if (user) {
                                token.accessToken = user.accessToken;
                                token.refreshToken = user.refreshToken;
                                token.userId = user.id;
                        }
                        return token;
                },

                async session({ session, token }) {
                        if (token) {
                                session.user.id = token.userId as string;
                                session.accessToken = token.accessToken as string;
                                session.refreshToken = token.refreshToken as string;
                        }
                        return session;
                },
        },
        pages: {
                signIn: '/sign-in',
                signOut: '/',
                error: '/',
        },
        session: {
                strategy: 'jwt',
                maxAge: 30 * 24 * 60 * 60, // 30 days
        },
        secret: process.env.NEXTAUTH_SECRET,
});

export { handler as GET, handler as POST };
