import { SignUpCard } from '@/features/auth/components/sign-up-card';
import Image from 'next/image';

const SignUpPage = async () => {
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
                                <SignUpCard />
                        </div>
                </div>
        );
};

export default SignUpPage;
