'use client';
import { Button as PButton } from 'primereact/button';
import { ButtonHTMLAttributes } from 'react';


export function Button({ className, ...rest }: ButtonHTMLAttributes<HTMLButtonElement>) {
    return <PButton className={className} {...rest} />;
}