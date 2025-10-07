'use client';

import { FormProvider, useFormContext } from '@/components/form/FormProvider';
import FormInputField from '@/components/form/FormInputField';
import FormInputPassword from '@/components/form/FormInputPassword';
import { Button } from 'primereact/button';
import { required, minLen, email, hasLower, hasUpper, hasDigit, matchField } from '@/components/form/validators';
import { useRef } from 'react';
import ToastProvider from '@/components/ui/ToastComponent';

function RegisterForm() {
    const form = useFormContext();
    const pwdRefVal = useRef<string>('');

    const onValid = async (values: Record<string, unknown>) => {
        alert(JSON.stringify(values, null, 2));
    };

    const onInvalid = async (errors: Record<string, string | null>) => {
        alert('Corrige los errores del formulario');
        console.error(errors);
    };

    return (
        <div className='p-4'>
            <ToastProvider position='bottom-right' life={2000} />
            <form onSubmit={form.handleSubmit(onValid, onInvalid)} className="space-y-4 max-w-md">
                <FormInputField
                    name="username"
                    label="Usuario"
                    validators={[required, minLen(3)]}
                    containerClassName="w-full"
                    className="w-full"
                    autoComplete="username"
                    required
                />

                <FormInputField
                    name="email"
                    label="Email"
                    validators={[required, email]}
                    containerClassName="w-full"
                    className="w-full"
                    autoComplete="email"
                    required
                />

                <FormInputPassword
                    name="password"
                    label="Contraseña"
                    validators={[required, minLen(8), hasLower, hasUpper, hasDigit]}
                    containerClassName="w-full"
                    className="w-full"
                    autoComplete="new-password"
                    required
                    feedback
                    showHelp
                    toggleMask
                    initiallyTouched
                    validateOnMount
                    onValueChange={(v) => {
                        pwdRefVal.current = v;
                    }}
                    value={pwdRefVal.current}
                />

                <FormInputPassword
                    name="confirm"
                    label="Confirmar contraseña"
                    validators={[required, matchField('contraseña', () => pwdRefVal.current)]}
                    containerClassName="w-full"
                    className="w-full"
                    autoComplete="new-password"
                    required
                    feedback={false}
                    showHelp={false}
                    toggleMask
                    initiallyTouched
                    validateOnMount
                />

                <Button type="submit" label="Crear cuenta" />
            </form>
        </div>
    );
}

export default function RegisterPage() {
    return (
        <div className="p-4">
            <FormProvider
                initialValues={{ username: '', email: '', password: '', confirm: '' }}
                defaults={{ validateOn: 'both', touchOnMount: true, validateOnMount: true }}
            >
                <RegisterForm />
            </FormProvider>
        </div>
    );
}
