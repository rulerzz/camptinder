'use client';

import { useState } from 'react';

import { toast } from 'sonner';
import { useSession } from 'next-auth/react';
import axios from 'axios';
import { User } from '../../../../types/user';

interface UpdateUserOptions {
        onSuccess?: (user: User) => void;
        onError?: (error: Error) => void;
}

export const useUpdateUser = (options?: UpdateUserOptions) => {
        const { data: session } = useSession();
        const [isUpdating, setIsUpdating] = useState(false);
        const [isUploading, setIsUploading] = useState(false);

        const updateUser = async (userData: Partial<User>): Promise<User | null> => {
                if (!session?.accessToken) {
                        toast.error('You must be logged in to update your profile');
                        return null;
                }

                setIsUpdating(true);

                try {
                        const response = await axios.patch(
                                `${process.env.NEXT_PUBLIC_API_URL}/api/users/profile/`,
                                userData,
                                {
                                        headers: { Authorization: `Bearer ${session.accessToken}` },
                                },
                        );

                        const updatedUser = response.data;
                        options?.onSuccess?.(updatedUser);
                        return updatedUser;
                } catch (error: any) {
                        const errorMessage = error.response?.data?.message || 'Failed to update profile';
                        toast.error(errorMessage);
                        options?.onError?.(new Error(errorMessage));
                        return null;
                } finally {
                        setIsUpdating(false);
                }
        };

        const uploadAvatar = async (file: File): Promise<string | null> => {
                if (!session?.accessToken) {
                        toast.error('You must be logged in to upload an avatar');
                        return null;
                }

                setIsUploading(true);

                try {
                        // Create a FormData instance for Cloudinary upload
                        const formData = new FormData();
                        formData.append('file', file);
                        formData.append('upload_preset', process.env.NEXT_PUBLIC_CLOUDINARY_UPLOAD_PRESET || '');

                        // Upload to Cloudinary
                        const cloudinaryResponse = await axios.post(
                                `https://api.cloudinary.com/v1_1/${process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME}/image/upload`,
                                formData,
                        );

                        // Get the secure URL from the response
                        const imageUrl = cloudinaryResponse.data.secure_url;

                        // Update the user profile with the new image URL
                        if (imageUrl) {
                                const updatedUser = await updateUser({ imageUrl });
                                if (updatedUser) {
                                        return imageUrl;
                                }
                        }

                        return null;
                } catch (error: any) {
                        const errorMessage = error.response?.data?.message || 'Failed to upload avatar';
                        toast.error(errorMessage);
                        return null;
                } finally {
                        setIsUploading(false);
                }
        };

        return {
                updateUser,
                uploadAvatar,
                isUpdating,
                isUploading,
        };
};
