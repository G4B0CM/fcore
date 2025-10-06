export interface CreateRolDto {
    name: string;
    description: string;
}

export interface UpdateRolDto {
    name: string;
    description: string;
}

export interface RolResponseDto {
    id: number;
    name: string;         // mapeado desde rol.main_name en el backend
    description: string;
    is_active: boolean;
}
