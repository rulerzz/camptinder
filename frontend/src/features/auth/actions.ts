'use server';

import type { signUpSchema, signInSchema } from './schema';
import type { z } from 'zod';

export async function registerUser(formData: z.infer<typeof signUpSchema>) {
        try {
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/register/`, {
                        method: 'POST',
                        headers: {
                                'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                                email: formData.email,
                                first_name: formData.firstName,
                                last_name: formData.lastName,
                                phone: formData.phone,
                                password: formData.password,
                                password_confirm: formData.confirmPassword,
                        }),
                });

                const data = await response.json();

                if (!response.ok) {
                        throw new Error(data.detail || 'Registration failed');
                }

                return { success: true, data };
        } catch (error) {
                console.error('Registration error:', error);
                return { success: false, error: (error as Error).message };
        }
}
