
import React, { JSX, useState } from "react";
import { Password } from 'primereact/password';
import { Divider } from 'primereact/divider';

interface InputPasswordProps {
    header?: (JSX.Element | boolean);
    footer?: (JSX.Element | boolean);
    feedback?: boolean;
    size?: number;
}

export default function InputPassword({ header, footer, feedback, size }: InputPasswordProps) {
    const [value, setValue] = useState<string>('');
    if (feedback) {
        header = <div className="font-bold mb-3">Elige una contraseña</div>;
        footer = (
            <>
                <Divider />
                <p className="mt-2">Recomendaciones</p>
                <ul className="pl-2 ml-2 mt-0 line-height-3">
                    <li>Al menos una minúscula</li>
                    <li>Al menos una mayúscula</li>
                    <li>Al menos un número</li>
                    <li>Mínimo 8 caracteres</li>
                </ul>
            </>
        );
    }


    return (
        <div className="card flex justify-content-center">
            <Password value={value}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) => setValue(e.target.value)}
                header={header} footer={footer} feedback={feedback}
                size={size} />
        </div>
    )
}
