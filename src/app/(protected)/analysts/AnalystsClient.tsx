// src/app/(protected)/analysts/AnalystsClient.tsx
'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Toast } from 'primereact/toast';
import { Toolbar } from 'primereact/toolbar';
import AppButton from '@/components/ui/AppButton';
import DataTablePro from '@/components/ui/DataTablePro';
import TagCell from '@/components/ui/TagCell';
import BoolIconCell from '@/components/ui/BoolIconCell';
import FormDialog from '@/components/form/FormDialog';
import FormInputField from '@/components/form/FormInputField';
import FormInputPassword from '@/components/form/FormInputPassword';
import FormSelectField from '@/components/form/FormSelectField';
import { required, minLen } from '@/components/form/validators';
import { oficialService } from '@/services/oficial.service';
import { rolesService } from '@/services/roles.service';
import type { RolResponseDto } from '@/types/rol';
import AppToolbar from '@/components/ui/AppToolbar';

type Row = {
    id: number;
    qcode: string;
    is_active: boolean;
    rolId: number | null;
    rolName: string | null;
};

export default function AnalystsClient() {
    const toast = useRef<Toast>(null);

    const [rows, setRows] = useState<Row[]>([]);
    const [loading, setLoading] = useState(false);

    const [createOpen, setCreateOpen] = useState(false);
    const [editOpen, setEditOpen] = useState<{ open: boolean; row: Row | null }>({ open: false, row: null });

    const [roles, setRoles] = useState<RolResponseDto[]>([]);
    const [debugOpen, setDebugOpen] = useState(false);
    const rawOfsRef = useRef<any[]>([]);
    const mappedRef = useRef<any[]>([]);

    const pick = (o: any, keys: string[]) => {
        for (const k of keys) if (o && o[k] !== undefined && o[k] !== null) return o[k];
        return undefined;
    };

    const normalizeOficial = (o: any) => {
        const idCand = pick(o, ['id', '_id', 'id_oficial', 'oficial_id']);
        const idNum = typeof idCand === 'number' ? idCand : Number(idCand);
        const id = Number.isFinite(idNum) ? idNum : NaN;
        const qcodeCand = pick(o, ['qcode', 'q_code', '_q_code', 'qCode']);
        const qcode = typeof qcodeCand === 'string' ? qcodeCand : String(qcodeCand ?? '');
        const isActiveCand = pick(o, ['is_active', '_is_active', 'active', 'enabled']);
        const is_active = typeof isActiveCand === 'boolean' ? isActiveCand : Boolean(isActiveCand);
        return { id, qcode, is_active };
    };

    const loadData = useCallback(async () => {
        setLoading(true);
        try {
            const [ofs, allRoles] = await Promise.all([oficialService.list(), rolesService.getAll()]);
            rawOfsRef.current = Array.isArray(ofs) ? ofs : [];
            const mappedRaw = rawOfsRef.current.map((raw) => ({ raw, norm: normalizeOficial(raw) }));
            const mapped = mappedRaw.filter((x) => Number.isFinite(x.norm.id) && x.norm.qcode);
            mappedRef.current = mapped;
            const withRoles = await Promise.all(
                mapped.map(async ({ raw, norm }) => {
                    const embedded = Array.isArray(raw?._roles) && raw._roles.length > 0 ? raw._roles[0] : null;
                    if (embedded) {
                        const rId = embedded?._id ?? embedded?.id ?? null;
                        const rName = embedded?._main_name ?? embedded?.name ?? null;
                        return { id: norm.id, qcode: norm.qcode, is_active: norm.is_active, rolId: rId ?? null, rolName: rName ?? null } as Row;
                    }
                    try {
                        const assigned = await oficialService.getRoles(norm.id);
                        const first = assigned?.[0] ?? null;
                        return { id: norm.id, qcode: norm.qcode, is_active: norm.is_active, rolId: first?.id ?? null, rolName: first?.name ?? null } as Row;
                    } catch {
                        return { id: norm.id, qcode: norm.qcode, is_active: norm.is_active, rolId: null, rolName: null } as Row;
                    }
                })
            );
            setRoles(allRoles);
            setRows(withRoles);
            if (withRoles.length === 0) {
                toast.current?.show({ severity: 'warn', summary: 'Sin filas visibles', detail: `Registros crudos: ${rawOfsRef.current.length} | Mapeados: ${mapped.length}`, life: 3000 });
            }
        } catch (e: any) {
            toast.current?.show({ severity: 'error', summary: 'Error cargando datos', detail: e?.message ?? 'Error', life: 3000 });
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadData();
    }, [loadData]);

    const roleOptions = useMemo(
        () => roles.filter((r) => r.is_active).map((r) => ({ label: r.name, value: r.id })),
        [roles]
    );

    const createOne = useCallback(async (values: Record<string, unknown>) => {
        const payload = {
            q_code: String(values.q_code ?? '').trim(),
            name: String(values.name ?? '').trim(),
            lastname: String(values.lastname ?? '').trim(),
            password: String(values.password ?? ''),
            rolId: Number(values.rolId ?? 0),
        };
        const res = await fetch('/api/oficials/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            throw new Error(data?.detail ?? 'Error al crear');
        }
        return res.json();
    }, []);

    const onCreateValid = useCallback(async (values: Record<string, unknown>) => {
        try {
            if (!values.rolId) throw new Error('Debe seleccionar un rol');
            await createOne(values);
            toast.current?.show({ severity: 'success', summary: 'Creado', detail: 'Oficial creado y rol asignado', life: 2000 });
            setCreateOpen(false);
            await loadData();
        } catch (e: any) {
            toast.current?.show({ severity: 'error', summary: 'No se pudo crear', detail: e?.message ?? 'Error', life: 3000 });
        }
    }, [createOne, loadData]);

    const onUpdateValid = useCallback(async (values: Record<string, unknown>, row: Row) => {
        const name = String(values.name ?? '').trim();
        const lastname = String(values.lastname ?? '').trim();
        const rolId = Number(values.rolId ?? 0);
        try {
            await oficialService.update({ id: row.id, name, lastname });
            const current = await oficialService.getRoles(row.id).catch(() => []);
            const currentId = current?.[0]?.id ?? null;
            if (rolId && currentId !== rolId) {
                if (currentId) await oficialService.removeRole(row.id, currentId);
                await oficialService.assignRole(row.id, rolId);
            }
            toast.current?.show({ severity: 'success', summary: 'Actualizado', detail: `Oficial ${row.qcode}`, life: 2000 });
            setEditOpen({ open: false, row: null });
            await loadData();
        } catch (e: any) {
            toast.current?.show({ severity: 'error', summary: 'No se pudo actualizar', detail: e?.message ?? 'Error', life: 3000 });
        }
    }, [loadData]);

    const onDeactivate = useCallback(async (r: Row) => {
        try {
            await oficialService.deactivate(r.qcode);
            toast.current?.show({ severity: 'success', summary: 'Desactivado', detail: r.qcode, life: 1500 });
            await loadData();
        } catch (e: any) {
            toast.current?.show({ severity: 'error', summary: 'No se pudo desactivar', detail: e?.message ?? 'Error', life: 3000 });
        }
    }, [loadData]);

    const header = (
        <AppToolbar
            start={
                <div className="flex align-items-center gap-2">
                    <AppButton label="Nuevo analista" icon="pi pi-plus" severity="primary" onClick={() => setCreateOpen(true)} />
                    <AppButton label={debugOpen ? 'Ocultar debug' : 'Debug'} icon="pi pi-bug" severity="secondary" outlined onClick={() => setDebugOpen((v) => !v)} />
                </div>
            }
            end={<h2 className="text-600">Administración de analistas</h2>}
            className="mb-3"
        />
    );

    const columns = [
        { field: 'id', header: 'ID', sortable: true, style: { width: '6rem' } },
        { field: 'qcode', header: 'QCode', sortable: true },
        { field: 'rolName', header: 'Rol', sortable: true, body: (r: Row) => <TagCell value={r.rolName ?? 'Sin rol'} severity={r.rolName ? 'info' : 'warning'} /> },
        { field: 'is_active', header: 'Activo', sortable: true, body: (r: Row) => <BoolIconCell value={r.is_active} /> },
        {
            field: 'actions',
            header: 'Acciones',
            body: (r: Row) => (
                <div className="flex gap-2">
                    <AppButton label="Editar" icon="pi pi-pencil" size="small" onClick={() => setEditOpen({ open: true, row: r })} />
                    <AppButton label="Desactivar" icon="pi pi-ban" size="small" severity="danger" outlined onClick={() => onDeactivate(r)} />
                </div>
            ),
            style: { width: '18rem' },
        },
    ];

    return (
        <div>
            <Toast ref={toast} position="bottom-right" />
            {header}

            {debugOpen && (
                <div className="surface-100 border-1 surface-border p-3 border-round mb-3">
                    <div className="text-sm mb-2">Debug</div>
                    <div className="grid">
                        <div className="col-12 md:col-6">
                            <div className="text-700 mb-1">Raw /oficial/list</div>
                            <pre className="overflow-auto" style={{ maxHeight: 240 }}>{JSON.stringify(rawOfsRef.current, null, 2)}</pre>
                        </div>
                        <div className="col-12 md:col-6">
                            <div className="text-700 mb-1">Mapeados</div>
                            <pre className="overflow-auto" style={{ maxHeight: 240 }}>{JSON.stringify(mappedRef.current.map(m => m.norm), null, 2)}</pre>
                        </div>
                    </div>
                </div>
            )}

            <DataTablePro
                value={rows}
                dataKey="id"
                loading={loading}
                globalFilterFields={['qcode', 'rolName']}
                columns={columns as any}
                paginator
                rows={10}
                rowsPerPageOptions={[10, 20, 50]}
                selectionMode="none"
            />

            <FormDialog
                visible={createOpen}
                onClose={() => setCreateOpen(false)}
                title="Nuevo analista"
                initialValues={{ q_code: '', name: '', lastname: '', password: '', rolId: null }}
                defaults={{ validateOn: 'change', touchOnMount: true, validateOnMount: true }}
                submitLabel="Crear"
                submitIcon="pi pi-check"
                submitSeverity="success"
                size="lg"
                onValid={onCreateValid}
                onInvalid={(errors) => {
                    const first = Object.values(errors).find(Boolean) as string | null;
                    if (first) toast.current?.show({ severity: 'warn', summary: 'Revisa el formulario', detail: first, life: 2500 });
                }}
            >
                <div className="grid">
                    <div className="col-12 md:col-6">
                        <FormInputField name="q_code" label="QCode" placeholder="QCode" validators={[required]} />
                    </div>
                    <div className="col-12 md:col-6">
                        <FormInputPassword name="password" label="Contraseña" placeholder="••••••••" toggleMask feedback={false} validators={[required, minLen(6)]} />
                    </div>
                    <div className="col-12 md:col-6">
                        <FormInputField name="name" label="Nombre" placeholder="Nombre" validators={[required]} />
                    </div>
                    <div className="col-12 md:col-6">
                        <FormInputField name="lastname" label="Apellido" placeholder="Apellido" validators={[required]} />
                    </div>
                    <div className="col-12">
                        <FormSelectField name="rolId" label="Rol" options={roleOptions} placeholder="Seleccione un rol" showClear={false} appendTo="self" validators={[required]} />
                    </div>
                </div>
            </FormDialog>

            <FormDialog
                visible={editOpen.open}
                onClose={() => setEditOpen({ open: false, row: null })}
                title={`Editar analista${editOpen.row ? ` ${editOpen.row.qcode}` : ''}`}
                initialValues={{
                    name: '',
                    lastname: '',
                    rolId: editOpen.row?.rolId ?? null,
                }}
                defaults={{ validateOn: 'change', touchOnMount: true, validateOnMount: true }}
                submitLabel="Guardar"
                submitIcon="pi pi-save"
                submitSeverity="success"
                size="lg"
                onValid={async (values) => {
                    if (!editOpen.row) return;
                    await onUpdateValid(values, editOpen.row);
                }}
                onInvalid={(errors) => {
                    const first = Object.values(errors).find(Boolean) as string | null;
                    if (first) toast.current?.show({ severity: 'warn', summary: 'Revisa el formulario', detail: first, life: 2500 });
                }}
            >
                <div className="grid">
                    <div className="col-12 md:col-6">
                        <FormInputField name="name" label="Nombre" placeholder="Nombre" validators={[required]} />
                    </div>
                    <div className="col-12 md:col-6">
                        <FormInputField name="lastname" label="Apellido" placeholder="Apellido" validators={[required]} />
                    </div>
                    <div className="col-12">
                        <FormSelectField name="rolId" label="Rol" options={roleOptions} placeholder="Seleccione un rol" showClear={false} appendTo="self" validators={[required]} />
                    </div>
                </div>
            </FormDialog>
        </div>
    );
}
