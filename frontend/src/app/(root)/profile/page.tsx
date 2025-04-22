'use client';

import { ProfilePageViewEdit } from '@/features/profile/components/profile-page-view-edit';

import React from 'react';

const ProfilePage = () => {
        return (
                <div className="pt-40 container mx-auto py-10 space-y-10">
                        <ProfilePageViewEdit />
                </div>
        );
};

export default ProfilePage;
