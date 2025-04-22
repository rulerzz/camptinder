import Navbar from '@/components/navbar/navbar';
import React from 'react';

interface DashboardLayoutProps {
        children: React.ReactNode;
}
const DashboardLayout = ({ children }: DashboardLayoutProps) => {
        return (
                <div className="min-h-screen">
                        <div className="mx-auto max-w-screen-[2520px] h-full">
                                <Navbar />
                                <main className="h-full py-8 px-6 flex flex-col">{children}</main>
                        </div>
                </div>
        );
};

export default DashboardLayout;
