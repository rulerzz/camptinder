'use client';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import React from 'react';
import LogoImage from '@public/logo.svg';
interface LogoProps {
        width?: number;
        height?: number;
}
const Logo = ({ width, height }: LogoProps) => {
        const router = useRouter();
        return (
                <div>
                        <Image
                                onClick={() => router.push('/')}
                                src={LogoImage}
                                alt="logo"
                                width={width || 120}
                                height={height || 40}
                                className="hidden md:block cursor-pointer"
                        />
                </div>
        );
};

export default Logo;
