export type User = {
        id: number;
        email: string;
        first_name: string;
        last_name: string;
        phone?: string | null;
        role?: string | null;
        role_name?: string | null;
        imageUrl?: string | null;
        is_active: boolean;
        is_verified: boolean;
        date_joined: string;
};
