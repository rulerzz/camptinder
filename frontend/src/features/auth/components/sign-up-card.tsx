'use client';

import { FcGoogle } from 'react-icons/fc';
import { FaGithub } from 'react-icons/fa';
import { DottedSeparator } from '@/components/dotted-separator';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Form, FormControl, FormField, FormItem, FormMessage } from '@/components/ui/form';
import React, { useState } from 'react';
import Link from 'next/link';
import { signUpSchema } from '../schema';
import Logo from '@/components/navbar/logo';
import { Checkbox } from '@/components/ui/checkbox';
import { PhoneInput } from '@/components/ui/phone-input';
import { Eye, EyeOff } from 'lucide-react';
import { registerUser } from '../actions';

import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import { signIn } from 'next-auth/react';

export const SignUpCard = () => {
        const [showPassword, setShowPassword] = useState(false);
        const [showConfirmPassword, setShowConfirmPassword] = useState(false);
        const router = useRouter();
        const form = useForm<z.infer<typeof signUpSchema>>({
                resolver: zodResolver(signUpSchema),
                defaultValues: {
                        firstName: '',
                        lastName: '',
                        email: '',
                        phone: '',
                        password: '',
                        confirmPassword: '',
                },
        });
        //Change isPending after adding the submit handler
        const isPending = form.formState.isSubmitting;
        const onSubmit = async (values: z.infer<typeof signUpSchema>) => {
                try {
                        const result = await registerUser(values);
                        if (result.success) {
                                await signIn('credentials', {
                                        email: values.email,
                                        password: values.password,
                                        redirect: false,
                                });
                                toast.success('Registration successful');
                                router.push('/');
                        } else {
                                toast.error(result.error || 'Registration failed');
                        }
                } catch (error) {
                        toast.error('Registration failed');
                }
        };
        const handleSocialSignUp = async (provider: 'google' | 'github') => {
                const result = await signIn(provider, { redirect: false, callbackUrl: '/' });
                if (result?.error) {
                        // Show error
                        toast.error(`Sign Up with ${provider} failed: ${result.error}`);
                }
        };
        return (
                <Card className="w-full h-full md:w-[480px] border-none shadow-none">
                        <CardHeader className="flex items-center justify-center text-center p-7">
                                <Logo width={240} />
                                <CardTitle className="text-2xl pt-8 text-primary">
                                        Join the Camptinder.com Community
                                </CardTitle>
                        </CardHeader>
                        <div className="px-7">
                                <DottedSeparator />
                        </div>
                        <CardContent className="p-7">
                                <Form {...form}>
                                        <form className="space-y-4" onSubmit={form.handleSubmit(onSubmit)}>
                                                {/* First Name Field */}
                                                <FormField
                                                        control={form.control}
                                                        name="firstName"
                                                        render={({ field }) => (
                                                                <FormItem>
                                                                        <FormControl>
                                                                                <Input
                                                                                        type="text"
                                                                                        placeholder="First name"
                                                                                        {...field}
                                                                                />
                                                                        </FormControl>
                                                                        <FormMessage />
                                                                </FormItem>
                                                        )}
                                                />

                                                {/* Last Name Field */}
                                                <FormField
                                                        control={form.control}
                                                        name="lastName"
                                                        render={({ field }) => (
                                                                <FormItem>
                                                                        <FormControl>
                                                                                <Input
                                                                                        type="text"
                                                                                        placeholder="Last name"
                                                                                        {...field}
                                                                                />
                                                                        </FormControl>
                                                                        <FormMessage />
                                                                </FormItem>
                                                        )}
                                                />

                                                {/* Email Field */}
                                                <FormField
                                                        control={form.control}
                                                        name="email"
                                                        render={({ field }) => (
                                                                <FormItem>
                                                                        <FormControl>
                                                                                <Input
                                                                                        type="email"
                                                                                        placeholder="Email address"
                                                                                        {...field}
                                                                                />
                                                                        </FormControl>
                                                                        <FormMessage />
                                                                </FormItem>
                                                        )}
                                                />

                                                {/* Phone Field */}
                                                <FormField
                                                        control={form.control}
                                                        name="phone"
                                                        render={({ field }) => (
                                                                <FormItem>
                                                                        <FormControl>
                                                                                <PhoneInput
                                                                                        international
                                                                                        type="tel"
                                                                                        placeholder="Phone number"
                                                                                        {...field}
                                                                                />
                                                                        </FormControl>
                                                                        <FormMessage />
                                                                </FormItem>
                                                        )}
                                                />

                                                {/* Password Field */}
                                                <FormField
                                                        control={form.control}
                                                        name="password"
                                                        render={({ field }) => (
                                                                <FormItem>
                                                                        <FormControl>
                                                                                <div className="relative">
                                                                                        <Input
                                                                                                type={
                                                                                                        showPassword
                                                                                                                ? 'text'
                                                                                                                : 'password'
                                                                                                }
                                                                                                placeholder="Password"
                                                                                                {...field}
                                                                                                className="pr-10"
                                                                                        />
                                                                                        <Button
                                                                                                type="button"
                                                                                                variant="ghost"
                                                                                                size="icon"
                                                                                                className="absolute right-0 top-0 h-full px-6 py-2 text-muted-foreground"
                                                                                                onClick={() =>
                                                                                                        setShowPassword(
                                                                                                                !showPassword,
                                                                                                        )
                                                                                                }
                                                                                        >
                                                                                                {showPassword ? (
                                                                                                        <EyeOff className="h-4 w-4" />
                                                                                                ) : (
                                                                                                        <Eye className="h-4 w-4" />
                                                                                                )}
                                                                                                <span className="sr-only">
                                                                                                        {showPassword
                                                                                                                ? 'Hide password'
                                                                                                                : 'Show password'}
                                                                                                </span>
                                                                                        </Button>
                                                                                </div>
                                                                        </FormControl>
                                                                        <FormMessage />
                                                                </FormItem>
                                                        )}
                                                />

                                                {/* Password Confirmation Field */}
                                                <FormField
                                                        control={form.control}
                                                        name="confirmPassword"
                                                        render={({ field }) => (
                                                                <FormItem>
                                                                        <FormControl>
                                                                                <div className="relative">
                                                                                        <Input
                                                                                                type={
                                                                                                        showConfirmPassword
                                                                                                                ? 'text'
                                                                                                                : 'password'
                                                                                                }
                                                                                                placeholder="Confirm password"
                                                                                                {...field}
                                                                                                className="pr-10"
                                                                                        />
                                                                                        <Button
                                                                                                type="button"
                                                                                                variant="ghost"
                                                                                                size="icon"
                                                                                                className="absolute right-0 top-0 h-full px-6 py-2 text-muted-foreground"
                                                                                                onClick={() =>
                                                                                                        setShowConfirmPassword(
                                                                                                                !showConfirmPassword,
                                                                                                        )
                                                                                                }
                                                                                        >
                                                                                                {showConfirmPassword ? (
                                                                                                        <EyeOff className="h-4 w-4" />
                                                                                                ) : (
                                                                                                        <Eye className="h-4 w-4" />
                                                                                                )}
                                                                                                <span className="sr-only">
                                                                                                        {showConfirmPassword
                                                                                                                ? 'Hide password'
                                                                                                                : 'Show password'}
                                                                                                </span>
                                                                                        </Button>
                                                                                </div>
                                                                        </FormControl>
                                                                        <FormMessage />
                                                                </FormItem>
                                                        )}
                                                />

                                                <div className="flex items-center space-x-2 py-2">
                                                        <Checkbox id="terms" />
                                                        <CardDescription className="leading-none">
                                                                <label
                                                                        htmlFor="terms"
                                                                        className="cursor-pointer select-none"
                                                                >
                                                                        By signing up, you agree to our{' '}
                                                                        <Link href="/privacy">
                                                                                <span className="text-primary hover:text-secondary underline">
                                                                                        Privacy Policy
                                                                                </span>
                                                                        </Link>{' '}
                                                                        and{' '}
                                                                        <Link href="/terms">
                                                                                <span className="text-primary hover:text-secondary underline">
                                                                                        Terms of Service
                                                                                </span>
                                                                        </Link>
                                                                        .
                                                                </label>
                                                        </CardDescription>
                                                </div>
                                                <div className="flex items-center space-x-2 pb-2">
                                                        <Checkbox id="marketing" />
                                                        <CardDescription className="leading-none">
                                                                <label
                                                                        htmlFor="marketing"
                                                                        className="cursor-pointer select-none"
                                                                >
                                                                        You consent to receive marketing emails from us.
                                                                </label>
                                                        </CardDescription>
                                                </div>

                                                <Button disabled={isPending} size="lg" className="w-full">
                                                        Sign Up
                                                </Button>
                                        </form>
                                </Form>
                        </CardContent>
                        <div className="px-7">
                                <DottedSeparator />
                        </div>
                        <CardContent className="p-7 flex flex-col gap-y-4">
                                <Button
                                        onClick={() => handleSocialSignUp('google')}
                                        variant={'secondary'}
                                        size={'lg'}
                                        className="w-full"
                                        disabled={isPending}
                                >
                                        <FcGoogle className="size-5 mr-1" />
                                        Sign Up with Google
                                </Button>
                                <Button
                                        onClick={() => handleSocialSignUp('github')}
                                        variant={'secondary'}
                                        size={'lg'}
                                        className="w-full"
                                        disabled={isPending}
                                >
                                        <FaGithub className="size-5 mr-1" />
                                        Sign Up with Github
                                </Button>
                        </CardContent>
                        <div className="px-7">
                                <DottedSeparator />
                        </div>
                        <CardContent className="p-7 flex items-center justify-center">
                                <p>Already have an account? </p>
                                <Link href="/sign-in" className="text-secondary ml-1 hover:underline">
                                        Sign In
                                </Link>
                        </CardContent>
                </Card>
        );
};
