import Link from 'next/link';
import { Facebook, Twitter, Youtube, Linkedin, Instagram } from 'lucide-react';
import AIChat from './ai-chat';

export default function Footer() {
        return (
                <footer className="bg-[#111827] text-white py-12">
                        <div className="container mx-auto">
                                {/* Two-column layout: Main content + AI chat */}
                                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                                        {/* Left section: Three columns + social + copyright */}
                                        <div className="lg:col-span-8">
                                                {/* Three columns */}
                                                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
                                                        {/* How to? Column */}
                                                        <div>
                                                                <h3 className="text-xl font-medium mb-6">How to?</h3>
                                                                <nav className="flex flex-col space-y-3 text-neutral-300">
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                Buy
                                                                        </Link>
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                Rent
                                                                        </Link>
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                Camping equipments
                                                                        </Link>
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                Liquids
                                                                        </Link>
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                Feedback!
                                                                        </Link>
                                                                </nav>
                                                        </div>

                                                        {/* Products Column */}
                                                        <div>
                                                                <h3 className="text-xl font-medium mb-6">Products</h3>
                                                                <nav className="flex flex-col space-y-3 text-neutral-300">
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                Firewood
                                                                        </Link>
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                Pellets
                                                                        </Link>
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                Camping equipments
                                                                        </Link>
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                Liquids
                                                                        </Link>
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                Other
                                                                        </Link>
                                                                </nav>
                                                        </div>

                                                        {/* Company Column */}
                                                        <div>
                                                                <h3 className="text-xl font-medium mb-6">Company</h3>
                                                                <nav className="flex flex-col space-y-3 text-neutral-300">
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                About Us
                                                                        </Link>
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                Our offerings
                                                                        </Link>
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                Newsroom
                                                                        </Link>
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                Investors
                                                                        </Link>
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                Blog
                                                                        </Link>
                                                                        <Link
                                                                                href="#"
                                                                                className="hover:text-white transition"
                                                                        >
                                                                                Careers
                                                                        </Link>
                                                                </nav>
                                                        </div>
                                                </div>

                                                {/* Social Media Icons */}
                                                <div className="flex space-x-6 pt-24">
                                                        <Link href="#" aria-label="Facebook">
                                                                <Facebook className="h-5 w-5" />
                                                        </Link>
                                                        <Link href="#" aria-label="Twitter">
                                                                <Twitter className="h-5 w-5" />
                                                        </Link>
                                                        <Link href="#" aria-label="Youtube">
                                                                <Youtube className="h-5 w-5" />
                                                        </Link>
                                                        <Link href="#" aria-label="LinkedIn">
                                                                <Linkedin className="h-5 w-5" />
                                                        </Link>
                                                        <Link href="#" aria-label="Instagram">
                                                                <Instagram className="h-5 w-5" />
                                                        </Link>
                                                </div>

                                                {/* Copyright */}
                                                <div className="my-4">
                                                        <p>© 2025 Camptinder.com All rights reserved.</p>
                                                </div>
                                        </div>

                                        {/* Right section: AI Chat */}
                                        <div className="lg:col-span-4">
                                                <AIChat />
                                        </div>
                                </div>
                        </div>
                </footer>
        );
}
