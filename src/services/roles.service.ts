// src/services/roles.service.ts
import { apiClient } from './apiClient';
import type { CreateRolDto, UpdateRolDto, RolResponseDto } from '@/types/rol';

export const rolesService = {
    create: (dto: CreateRolDto, token?: string | null) =>
        apiClient.post<RolResponseDto, CreateRolDto>('/roles/', dto, { token: token ?? null }),
    getAll: (token?: string | null) =>
        apiClient.get<RolResponseDto[]>('/roles/', { token: token ?? null }),
    findById: (id: number, token?: string | null) =>
        apiClient.get<RolResponseDto>(`/roles/find_by_id/${id}`, { token: token ?? null }),
    update: (rolId: number, dto: UpdateRolDto, token?: string | null) =>
        apiClient.put<RolResponseDto, UpdateRolDto>(`/roles/${rolId}`, dto, { token: token ?? null }),
    deactivate: (id: number, token?: string | null) =>
        apiClient.get<RolResponseDto>(`/roles/deactivate/${id}`, { token: token ?? null }),
};
