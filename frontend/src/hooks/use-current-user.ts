'use client';

import { useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import axios from 'axios';
import { User } from '../../types/user';

export const useCurrentUser = () => {
        const { data: session, status } = useSession();
        const [user, setUser] = useState<User | null>(null);
        const [loading, setLoading] = useState(true);
        const [error, setError] = useState(null);

        useEffect(() => {
                const fetchUser = async () => {
                        if (status === 'authenticated' && session?.accessToken) {
                                try {
                                        const response = await axios.get(
                                                `${process.env.NEXT_PUBLIC_API_URL}/api/users/profile/`,
                                                {
                                                        headers: { Authorization: `Bearer ${session.accessToken}` },
                                                },
                                        );

                                        setUser(response.data);
                                } catch (err: any) {
                                        setError(err);
                                } finally {
                                        setLoading(false);
                                }
                        } else if (status !== 'loading') {
                                setLoading(false);
                        }
                };

                fetchUser();
        }, [session, status]);

        return { user, setUser, loading, error };
};
