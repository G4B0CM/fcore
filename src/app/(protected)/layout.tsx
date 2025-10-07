// src/app/(protected)/layout.tsx
import ClientShell from '@/components/layout/ClientShell';
import { requireAuth } from '@/lib/auth/server';

export default async function ProtectedLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const { payload } = await requireAuth();

    const roles = (payload?.roles ?? (payload?.role ? [payload.role] : [])) as string[];
    const username = (payload?.username ?? payload?.sub ?? '') as string;

    return (
        <ClientShell roles={roles} username={username || null}>
            {children}
        </ClientShell>
    );
}
