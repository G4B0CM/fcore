'use client';

import { useRef } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Toast } from 'primereact/toast';
import { FormProvider } from '@/components/form/FormProvider';
import FormInputField from '@/components/form/FormInputField';
import FormInputPassword from '@/components/form/FormInputPassword';
import FormSubmitButton from '@/components/form/FormSubmitButton';
import { required, minLen } from '@/components/form/validators';

export default function LoginPage() {
    const toast = useRef<Toast>(null);
    const router = useRouter();
    const sp = useSearchParams();
    const redirectTo = sp.get('redirectTo') || '/dashboard';

    return (
        <div className="flex min-h-screen align-items-center justify-content-center p-4">
            <Toast ref={toast} position="bottom-right" />
            <div className="surface-card p-5 shadow-2 border-round w-full sm:w-25rem">
                <h2 className="text-2xl mb-4">Ingresar</h2>
                <FormProvider
                    initialValues={{ username: '', password: '' }}
                    defaults={{ validateOn: 'both', touchOnMount: true, validateOnMount: true }}
                >
                    <form className="space-y-4">
                        <FormInputField
                            name="username"
                            label="Usuario"
                            placeholder="usuario"
                            validators={[required]}
                        />
                        <FormInputPassword
                            name="password"
                            label="Contraseña"
                            toggleMask
                            feedback={false}
                            validators={[required, minLen(3)]}
                        />
                        <FormSubmitButton
                            label="Entrar"
                            icon="pi pi-sign-in"
                            className="w-full"
                            severity="primary"
                            onValid={async (values) => {
                                const { username, password } = values as { username: string; password: string };
                                try {
                                    const res = await fetch('/api/auth/login', {
                                        method: 'POST',
                                        headers: { 'Content-Type': 'application/json' },
                                        body: JSON.stringify({ username, password }),
                                    });
                                    if (!res.ok) {
                                        const data = await res.json().catch(() => ({}));
                                        throw new Error(data?.detail ?? 'Credenciales inválidas');
                                    }
                                    toast.current?.show({ severity: 'success', summary: 'Bienvenido', detail: username, life: 1200 });
                                    setTimeout(() => router.replace(redirectTo), 300);
                                } catch (e: any) {
                                    toast.current?.show({ severity: 'error', summary: 'Error de acceso', detail: e?.message ?? 'Error', life: 3000 });
                                }
                            }}
                            onInvalid={(errors) => {
                                const first = Object.values(errors).find(Boolean) as string | null;
                                toast.current?.show({ severity: 'warn', summary: 'Revisa el formulario', detail: first ?? 'Campos requeridos', life: 2500 });
                            }}
                        />
                    </form>
                </FormProvider>
            </div>
        </div>
    );
}
