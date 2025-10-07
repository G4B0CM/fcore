// src/app/(protected)/analysts/page.tsx
import { requireRole } from '@/lib/auth/server';

export default async function AnalystsPage() {
    await requireRole(['admin']);
    return (
        <div className="surface-card p-4 border-round shadow-1">
            <h2 className="text-2xl mb-2">Analistas</h2>
            <p>Base de administración de analistas.</p>
        </div>
    );
}
