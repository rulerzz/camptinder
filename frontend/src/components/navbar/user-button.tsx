'use client';

import { DottedSeparator } from '@/components/dotted-separator';
import { Avatar } from '@/components/ui/avatar';
import {
        DropdownMenu,
        DropdownMenuTrigger,
        DropdownMenuContent,
        DropdownMenuItem,
} from '@/components/ui/dropdown-menu';
import { useCurrentUser } from '@/hooks/use-current-user';

import { Loader, LogOutIcon, Settings2Icon, UserIcon } from 'lucide-react';
import { signOut } from 'next-auth/react';
import Image from 'next/image';
import { useRouter } from 'next/navigation';

export const UserButton = () => {
        const { user, loading: isLoading } = useCurrentUser();
        const router = useRouter();

        if (!user) {
                return null;
        }
        if (isLoading)
                return (
                        <div className="size-10 rounded-full flex items-center justify-center bg-neutral-200 border border-neutral-300">
                                <Loader className="size-4 animate-spin text-muted-foreground" />
                        </div>
                );

        return (
                <DropdownMenu modal={false}>
                        <DropdownMenuTrigger className="outline-none relative">
                                <Avatar className="size-10 hover:opacity-75 transition border border-neutral-100">
                                        <Image
                                                src={user.imageUrl ? user.imageUrl : '/placeholder.png'}
                                                alt="User Avatar"
                                                width={80}
                                                height={80}
                                                className="rounded-full"
                                        />
                                </Avatar>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end" side="bottom" className="w-60" sideOffset={10}>
                                <div className="flex flex-col items-center justify-center gap-2 px-2 py-4">
                                        <Avatar className="size-20 transition border border-neutral-100">
                                                <Image
                                                        src={user.imageUrl ? user.imageUrl : '/placeholder.png'}
                                                        alt="User Avatar"
                                                        width={80}
                                                        height={80}
                                                        className="rounded-full"
                                                />
                                        </Avatar>
                                        <div className="flex flex-col justify-center items-center">
                                                <p className="text-lg font-medium text-neutral-900">
                                                        {user.first_name} {user.last_name}
                                                </p>
                                                <p className="text-sm text-muted-foreground">{user.email}</p>
                                        </div>
                                </div>
                                <DottedSeparator className="my-1" />
                                <DropdownMenuItem
                                        onClick={() => router.push('/profile')}
                                        className="h-10 flex items-center  font-medium cursor-pointer"
                                >
                                        <UserIcon className="size-4 mr-2" />
                                        My Profile
                                </DropdownMenuItem>
                                <DottedSeparator className="my-1" />
                                <DropdownMenuItem
                                        onClick={() => signOut()}
                                        className="h-10 flex items-center text-amber-700 font-medium cursor-pointer"
                                >
                                        <LogOutIcon className="size-4 mr-2" />
                                        Sign Out
                                </DropdownMenuItem>
                        </DropdownMenuContent>
                </DropdownMenu>
        );
};
