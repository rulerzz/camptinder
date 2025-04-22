import { getToken } from 'next-auth/jwt';
import { type NextRequest, NextResponse } from 'next/server';

export async function middleware(req: NextRequest) {
        const secret = process.env.NEXTAUTH_SECRET;
        if (!secret) {
                throw new Error('NEXTAUTH_SECRET is not defined');
        }
        const token = await getToken({ req, secret });

        // List of paths that should be private (authentication required)
        const privatePaths = ['/profile']; // Example private paths

        // Check if the current path is private
        const isPrivatePath = privatePaths.some((path) => req.nextUrl.pathname.startsWith(path));

        // If the user is logged in and tries to access a private path, continue the request
        if (token && isPrivatePath) {
                return NextResponse.next();
        }

        // If the user is not logged in and tries to access a private path, redirect to sign-in
        if (!token && isPrivatePath) {
                return NextResponse.redirect(new URL('/sign-in', req.url));
        }

        // If the path is public (not in privatePaths), allow access
        return NextResponse.next();
}

export const config = {
        matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
