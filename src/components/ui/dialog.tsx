'use client';
import { Dialog as PDialog, DialogProps } from 'primereact/dialog';


export function Dialog(props: DialogProps) {
    return <PDialog dismissableMask modal {...props} />;
}