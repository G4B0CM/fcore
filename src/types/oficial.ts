import type { RolResponseDto } from "./role";

export interface CreateOficialDto {
    q_code: string;
    name: string;
    lastname: string;
    password: string;
}

export interface UpdateOficialDto {
    id: number;
    name: string;
    lastname: string;
}

export interface ResponseOficialDto {
    id: number;
    qcode: string;       // nota: en backend es qcode, en create es q_code
    is_active: boolean;
}

// Para endpoints que devuelven listado/entidad completa (si amplías luego):
export interface OficialFull extends ResponseOficialDto {
    name?: string;
    lastname?: string;
    roles?: RolResponseDto[];
}
