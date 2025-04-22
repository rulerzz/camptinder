'use client';

import type React from 'react';

import { useCurrentUser } from '@/hooks/use-current-user';
import { useRef, useState } from 'react';
import type { User } from '../../../../types/user';

import { Camera, Loader2, PencilIcon } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { PhoneInput } from '@/components/ui/phone-input';
import Image from 'next/image';
import { useUpdateUser } from '../api/use-update-user';
import { toast } from 'sonner';

export const ProfilePageViewEdit = () => {
        const { user, loading: isLoading, setUser } = useCurrentUser();

        const { updateUser, uploadAvatar, isUpdating, isUploading } = useUpdateUser({
                onSuccess: (updatedUser) => {
                        // Update the local user state immediately
                        setUser(updatedUser);
                        toast.success('Profile updated!');
                },
        });

        const [isEditing, setIsEditing] = useState(false);
        const [formData, setFormData] = useState<Partial<User>>({});

        const fileInputRef = useRef<HTMLInputElement>(null);

        const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
                setFormData({
                        ...formData,
                        [e.target.name]: e.target.value,
                });
        };

        const handlePhoneChange = (value: string) => {
                setFormData({
                        ...formData,
                        phone: value,
                });
        };

        const handleImageClick = () => {
                if (isEditing) {
                        fileInputRef.current?.click();
                }
        };

        const handleImageChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
                const file = e.target.files?.[0];
                if (!file) return;

                // Check file size (limit to 5MB)
                if (file.size > 5 * 1024 * 1024) {
                        toast.error('Image size should be less than 5MB');
                        return;
                }

                // Check file type
                if (!file.type.startsWith('image/')) {
                        toast.error('Please select an image file');
                        return;
                }

                const imageUrl = await uploadAvatar(file);
                if (imageUrl) {
                        // Update form data
                        setFormData({
                                ...formData,
                                imageUrl,
                        });

                        // Update local user state immediately
                }
        };

        const handleSubmit = async (e: React.FormEvent) => {
                e.preventDefault();
                if (!user) return;

                const updatedUser = await updateUser(formData);
                if (updatedUser) {
                        setIsEditing(false);
                        setFormData({});
                }
        };

        if (isLoading) {
                return (
                        <div className="flex justify-center items-center min-h-[400px]">
                                <Loader2 className="h-8 w-8 animate-spin text-primary" />
                        </div>
                );
        }

        if (!user) {
                return <div className="text-center py-8">User not found</div>;
        }

        return (
                <Card className="w-full max-w-3xl mx-auto">
                        <CardHeader className="flex flex-row items-center justify-between">
                                <CardTitle className="text-2xl font-bold">Profile Settings</CardTitle>
                                {!isEditing && (
                                        <Button onClick={() => setIsEditing(true)}>
                                                <PencilIcon className="size-4 mr-2" />
                                                Edit Profile
                                        </Button>
                                )}
                        </CardHeader>
                        <CardContent>
                                <div className="flex flex-col gap-6">
                                        <div className="flex flex-col items-center space-y-4">
                                                <div className="relative group" onClick={handleImageClick}>
                                                        <Avatar
                                                                className={`size-40 ${
                                                                        isEditing ? 'cursor-pointer' : ''
                                                                }`}
                                                        >
                                                                {formData.imageUrl || user.imageUrl ? (
                                                                        <AvatarImage
                                                                                src={
                                                                                        formData.imageUrl ||
                                                                                        user.imageUrl ||
                                                                                        ''
                                                                                }
                                                                                alt={`${user.first_name} ${user.last_name}`}
                                                                                className={`transition duration-300 ${
                                                                                        isEditing
                                                                                                ? 'group-hover:opacity-60 '
                                                                                                : ''
                                                                                }`}
                                                                        />
                                                                ) : (
                                                                        <AvatarFallback>
                                                                                <Image
                                                                                        src={
                                                                                                user.imageUrl
                                                                                                        ? user.imageUrl
                                                                                                        : '/placeholder.png'
                                                                                        }
                                                                                        alt="User Avatar"
                                                                                        width={160}
                                                                                        height={160}
                                                                                        className="rounded-full"
                                                                                />
                                                                        </AvatarFallback>
                                                                )}
                                                        </Avatar>

                                                        {/* Icon camera or loader */}
                                                        {isEditing && (
                                                                <div className="absolute inset-0 flex items-center justify-center text-primary-foreground rounded-full p-1 shadow-sm z-10 opacity-0 group-hover:opacity-100 group-hover:scale-100 scale-0 transition-all duration-300">
                                                                        {isUploading ? (
                                                                                <Loader2 className="size-8 animate-spin" />
                                                                        ) : (
                                                                                <Camera className="size-8 cursor-pointer" />
                                                                        )}
                                                                </div>
                                                        )}

                                                        <input
                                                                type="file"
                                                                ref={fileInputRef}
                                                                className="hidden"
                                                                accept="image/*"
                                                                onChange={handleImageChange}
                                                        />
                                                </div>

                                                <div className="text-center">
                                                        <p className="font-medium">{user.email}</p>
                                                        <p className="text-sm text-muted-foreground">
                                                                Joined on{' '}
                                                                {new Date(user.date_joined).toLocaleDateString()}
                                                        </p>
                                                </div>
                                        </div>

                                        {isEditing ? (
                                                <form onSubmit={handleSubmit} className="flex-1">
                                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                                <div className="space-y-2">
                                                                        <Label htmlFor="first_name">First Name</Label>
                                                                        <Input
                                                                                id="first_name"
                                                                                name="first_name"
                                                                                defaultValue={user.first_name}
                                                                                onChange={handleChange}
                                                                        />
                                                                </div>

                                                                <div className="space-y-2">
                                                                        <Label htmlFor="last_name">Last Name</Label>
                                                                        <Input
                                                                                id="last_name"
                                                                                name="last_name"
                                                                                defaultValue={user.last_name}
                                                                                onChange={handleChange}
                                                                        />
                                                                </div>

                                                                <div className="space-y-2">
                                                                        <Label htmlFor="email">Email</Label>
                                                                        <Input
                                                                                id="email"
                                                                                name="email"
                                                                                type="email"
                                                                                defaultValue={user.email}
                                                                                onChange={handleChange}
                                                                        />
                                                                </div>

                                                                <div className="space-y-2">
                                                                        <Label htmlFor="phone">Phone Number</Label>
                                                                        <PhoneInput
                                                                                international
                                                                                type="tel"
                                                                                id="phone"
                                                                                name="phone"
                                                                                value={
                                                                                        formData.phone ||
                                                                                        user.phone ||
                                                                                        ''
                                                                                }
                                                                                onChange={handlePhoneChange}
                                                                        />
                                                                </div>

                                                                {user.role && (
                                                                        <div className="space-y-2">
                                                                                <Label htmlFor="role">Role</Label>
                                                                                <Input
                                                                                        id="role"
                                                                                        value={
                                                                                                user.role_name ||
                                                                                                user.role
                                                                                        }
                                                                                        disabled
                                                                                />
                                                                        </div>
                                                                )}
                                                        </div>

                                                        <div className="flex justify-end mt-6 space-x-2">
                                                                <Button
                                                                        type="button"
                                                                        variant="outline"
                                                                        onClick={() => setIsEditing(false)}
                                                                >
                                                                        Cancel
                                                                </Button>
                                                                <Button type="submit" disabled={isUpdating}>
                                                                        {isUpdating ? (
                                                                                <>
                                                                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                                                                        Saving...
                                                                                </>
                                                                        ) : (
                                                                                'Save Profile'
                                                                        )}
                                                                </Button>
                                                        </div>
                                                </form>
                                        ) : (
                                                <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-4">
                                                        <div className="space-y-1">
                                                                <p className="text-sm font-medium text-muted-foreground">
                                                                        First Name
                                                                </p>
                                                                <p className="font-medium">{user.first_name}</p>
                                                        </div>

                                                        <div className="space-y-1">
                                                                <p className="text-sm font-medium text-muted-foreground">
                                                                        Last Name
                                                                </p>
                                                                <p className="font-medium">{user.last_name}</p>
                                                        </div>

                                                        <div className="space-y-1">
                                                                <p className="text-sm font-medium text-muted-foreground">
                                                                        Email
                                                                </p>
                                                                <p className="font-medium">{user.email}</p>
                                                        </div>

                                                        <div className="space-y-1">
                                                                <p className="text-sm font-medium text-muted-foreground">
                                                                        Phone Number
                                                                </p>
                                                                <p className="font-medium">
                                                                        {user.phone || 'Not provided'}
                                                                </p>
                                                        </div>

                                                        {user.role && (
                                                                <div className="space-y-1">
                                                                        <p className="text-sm font-medium text-muted-foreground">
                                                                                Role
                                                                        </p>
                                                                        <p className="font-medium">
                                                                                {user.role_name || user.role}
                                                                        </p>
                                                                </div>
                                                        )}

                                                        <div className="space-y-1">
                                                                <p className="text-sm font-medium text-muted-foreground">
                                                                        Account Status
                                                                </p>
                                                                <div className="flex items-center">
                                                                        <div
                                                                                className={`h-2 w-2 rounded-full mr-2 ${
                                                                                        user.is_active
                                                                                                ? 'bg-green-500'
                                                                                                : 'bg-red-500'
                                                                                }`}
                                                                        ></div>
                                                                        <p className="font-medium">
                                                                                {user.is_active ? 'Active' : 'Inactive'}
                                                                        </p>
                                                                </div>
                                                        </div>

                                                        <div className="space-y-1">
                                                                <p className="text-sm font-medium text-muted-foreground">
                                                                        Verification Status
                                                                </p>
                                                                <div className="flex items-center">
                                                                        <div
                                                                                className={`h-2 w-2 rounded-full mr-2 ${
                                                                                        user.is_verified
                                                                                                ? 'bg-green-500'
                                                                                                : 'bg-yellow-500'
                                                                                }`}
                                                                        ></div>
                                                                        <p className="font-medium">
                                                                                {user.is_verified
                                                                                        ? 'Verified'
                                                                                        : 'Not Verified'}
                                                                        </p>
                                                                </div>
                                                        </div>
                                                </div>
                                        )}
                                </div>
                        </CardContent>
                </Card>
        );
};
