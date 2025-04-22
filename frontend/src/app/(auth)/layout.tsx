'use client';
import { Button } from '@/components/ui/button';
import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import React from 'react';
interface AuthLayoutProps {
        children: React.ReactNode;
}
const AuthLayout = ({ children }: AuthLayoutProps) => {
        return (
                <main className="bg-neutral-100 min-h-screen">
                        <div className="flex flex-col items-center justify-center mx-auto">{children}</div>
                </main>
        );
};

export default AuthLayout;
