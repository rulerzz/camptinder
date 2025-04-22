import { SignInCard } from '@/features/auth/components/sign-in-card';
import Image from 'next/image';

const SignInPage = () => {
        return (
                <div className="relative min-h-screen w-full flex items-center justify-center">
                        <Image
                                src="/forest.jpeg"
                                alt="Forest Background"
                                fill
                                style={{ objectFit: 'cover' }}
                                quality={100}
                        />

                        <div className="relative z-10 w-full max-w-md p-6">
                                <SignInCard />
                        </div>
                </div>
        );
};

export default SignInPage;
