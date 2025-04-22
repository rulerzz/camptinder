import { z } from 'zod';

export const signInSchema = z.object({
        email: z.string().email(),
        password: z.string().min(1, 'Password is required'),
});

// Define form schema for validation
export const signUpSchema = z
        .object({
                firstName: z.string().min(1, 'First name is required'),
                lastName: z.string().min(1, 'Last name is required'),
                email: z.string().email('Invalid email address'),
                phone: z.string().min(10, 'Phone number must be at least 10 digits'),
                password: z
                        .string()
                        .min(8, 'Password must be at least 8 characters')
                        .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
                        .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
                        .regex(/[0-9]/, 'Password must contain at least one number'),
                confirmPassword: z.string(),
        })
        .refine((data) => data.password === data.confirmPassword, {
                message: 'Passwords do not match',
                path: ['confirmPassword'],
        });
