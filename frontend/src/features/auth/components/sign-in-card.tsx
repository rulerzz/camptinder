'use client';
import { FcGoogle } from 'react-icons/fc';
import { FaGithub } from 'react-icons/fa';
import { DottedSeparator } from '@/components/dotted-separator';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Form, FormControl, FormField, FormItem, FormMessage } from '@/components/ui/form';

import { signInSchema } from '../schema';
import Logo from '@/components/navbar/logo';

import { useRouter } from 'next/navigation';

import { toast } from 'sonner';
import Link from 'next/link';
import { signIn } from 'next-auth/react';

export const SignInCard = () => {
        const form = useForm<z.infer<typeof signInSchema>>({
                resolver: zodResolver(signInSchema),
                defaultValues: {
                        email: '',
                        password: '',
                },
        });
        const router = useRouter();
        //Change isPending after adding the submit handler
        const isPending = form.formState.isSubmitting;
        const onSubmit = async (values: z.infer<typeof signInSchema>) => {
                const result = await signIn('credentials', {
                        email: values.email,
                        password: values.password,
                        redirect: false,
                });

                if (result?.ok && !result.error) {
                        toast.success('Login successful');
                        router.push('/');
                        router.refresh();
                } else {
                        toast.error(result?.error || 'Login failed');
                }
        };

        const handleSocialSignIn = async (provider: 'google' | 'github') => {
                const result = await signIn(provider, { redirect: false, callbackUrl: '/' });
                console.log(result);
                if (result?.error) {
                        // Show error
                        toast.error(`Sign In with ${provider} failed: ${result.error}`);
                }
        };

        return (
                <Card className="w-full h-full md:w-[480px] border-none shadow-none">
                        <CardHeader className="flex items-center justify-center text-center p-7">
                                <Logo width={240} />
                                <CardTitle className="text-2xl pt-8 text-primary">Welcome Back!</CardTitle>
                        </CardHeader>
                        <div className="px-7">
                                <DottedSeparator />
                        </div>
                        <CardContent className="p-7">
                                <Form {...form}>
                                        <form className="space-y-4" onSubmit={form.handleSubmit(onSubmit)}>
                                                {/* Email Field */}
                                                <FormField
                                                        control={form.control}
                                                        name="email"
                                                        render={({ field }) => (
                                                                <FormItem>
                                                                        <FormControl>
                                                                                <Input
                                                                                        type="email"
                                                                                        placeholder="Enter email address"
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
                                                                                <Input
                                                                                        type="password"
                                                                                        placeholder="Enter password"
                                                                                        {...field}
                                                                                />
                                                                        </FormControl>
                                                                        <FormMessage />
                                                                </FormItem>
                                                        )}
                                                />
                                                <div className="text-sm flex justify-end">
                                                        <Link
                                                                href="/reset-password"
                                                                className=" text-muted-foreground hover:underline"
                                                        >
                                                                Forgot Password?
                                                        </Link>
                                                </div>
                                                <Button disabled={isPending} size="lg" className="w-full">
                                                        Sign In
                                                </Button>
                                        </form>
                                </Form>
                        </CardContent>
                        <div className="px-7">
                                <DottedSeparator />
                        </div>
                        <CardContent className="p-7 flex flex-col gap-y-4">
                                <Button
                                        onClick={() => handleSocialSignIn('google')}
                                        variant={'secondary'}
                                        size={'lg'}
                                        className="w-full"
                                        disabled={isPending}
                                >
                                        <FcGoogle className="size-5 mr-1" />
                                        Sign In with Google
                                </Button>
                                <Button
                                        onClick={() => handleSocialSignIn('github')}
                                        variant={'secondary'}
                                        size={'lg'}
                                        className="w-full"
                                        disabled={isPending}
                                >
                                        <FaGithub className="size-5 mr-1" />
                                        Sign In with Github
                                </Button>
                                <div className="px-7">
                                        <DottedSeparator />
                                </div>
                                <CardContent className="p-7 flex items-center justify-center">
                                        <p>Don&apos;t have an account?</p>
                                        <Link href="/sign-up" className="text-secondary ml-1 hover:underline">
                                                Sign Up
                                        </Link>
                                </CardContent>
                        </CardContent>
                </Card>
        );
};
