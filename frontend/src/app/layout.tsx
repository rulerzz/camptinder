import type { Metadata } from 'next';
import { League_Spartan } from 'next/font/google';
import './globals.css';
import { cn } from '@/utils/utils';
import { Toaster } from 'sonner';
import Footer from '@/components/footer';
import { AuthProvider } from '@/components/auth-provider';
import { ThemeProvider } from 'next-themes';
import React from 'react';

const leagueSpartan = League_Spartan({
        subsets: ['latin'],
        variable: '--font-league-spartan',
});
export const metadata: Metadata = {
        title: 'Camp Tinder',
        description: 'Your camping equipment marketplace',
};

export default function RootLayout({
        children,
}: Readonly<{
        children: React.ReactNode;
}>) {
        return (
                <html lang="en">
                        <body className={cn(leagueSpartan.className, 'antialiased min-h-screen')}>
                                <Toaster />
                                <AuthProvider>{children}</AuthProvider>
                                <Footer />
                        </body>
                </html>
        );
}
