'use client';

import Link from 'next/link';
import Container from '../container';
import { Button } from '../ui/button';
import Logo from './logo';
import Search from './search';
import { useCurrentUser } from '@/hooks/use-current-user';
import { UserButton } from './user-button';
import { redirect, useRouter } from 'next/navigation';
import { Skeleton } from '../ui/skeleton';
import { Loader } from 'lucide-react';

const Navbar = () => {
        const { user: currentUser, loading: isLoading } = useCurrentUser();
        const router = useRouter();
        return (
                <div className="fixed w-full bg-white z-10 shadow-sm">
                        <div className="py-4 border-b-1">
                                <Container>
                                        <div className="flex flex-row items-center justify-between gap-3 md:gap-0">
                                                <Logo />
                                                <Search />
                                                {isLoading ? (
                                                        // During loading, show a skeleton
                                                        <div className="size-10 rounded-full flex items-center justify-center bg-primary border border-neutral-300">
                                                                <Loader className="size-4 animate-spin text-white" />
                                                        </div>
                                                ) : currentUser ? (
                                                        // If user is logged in, show user button
                                                        <UserButton />
                                                ) : (
                                                        // If user is not logged in, show sign in button
                                                        <Button
                                                                onClick={() => router.push('/sign-in')}
                                                                variant={'default'}
                                                                size={'lg'}
                                                        >
                                                                Sign In
                                                        </Button>
                                                )}
                                        </div>
                                </Container>
                        </div>
                </div>
        );
};

export default Navbar;
