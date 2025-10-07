'use client';

import { FormProvider, useFormContext } from '@/components/form/FormProvider';
import FormInputField from '@/components/form/FormInputField';
import FormInputPassword from '@/components/form/FormInputPassword';
import { Button } from 'primereact/button';
import { required } from '@/components/form/validators';

function LoginForm() {
    const form = useFormContext();

    const onValid = async (values: Record<string, unknown>) => {
        alert('Login OK');
        console.log(values);
    };

    const onInvalid = async () => {
        alert('Usuario o contraseña requeridos');
    };

    return (
        <form onSubmit={form.handleSubmit(onValid, onInvalid)} className="space-y-4 max-w-md">
            <FormInputField
                name="username"
                label="Usuario"
                validators={[required]}
                containerClassName="w-full"
                className="w-full"
                autoComplete="username"
                required
            />

            <FormInputPassword
                name="password"
                label="Contraseña"
                validators={[required]}
                containerClassName="w-full"
                className="w-full"
                autoComplete="current-password"
                required
                feedback={false}
                showHelp={false}
                toggleMask
            />

            <Button type="submit" label="Entrar" />
        </form>
    );
}

export default function LoginPage() {
    return (
        <div className="p-4">
            <FormProvider
                initialValues={{ username: '', password: '' }}
                defaults={{ validateOn: 'both', touchOnMount: false, validateOnMount: false }}
            >
                <LoginForm />
            </FormProvider>
        </div>
    );
}
