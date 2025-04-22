'use client';
import { useCurrentUser } from '@/hooks/use-current-user';

export default function Home() {
        const { user } = useCurrentUser();

        return <div className="pt-40 text-chart-1">{JSON.stringify(user)}</div>;
}
