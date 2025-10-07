// src/services/oficial.service.ts
import { apiClient } from './apiClient';
import type {
    CreateOficialDto,
    UpdateOficialDto,
    ResponseOficialDto,
    OficialRole,
} from '@/types/oficial';

export const oficialService = {
    create: (dto: CreateOficialDto, token?: string | null) =>
        apiClient.post<ResponseOficialDto, CreateOficialDto>('/oficial/create', dto, { token: token ?? null }),
    list: (token?: string | null) =>
        apiClient.get<ResponseOficialDto[]>('/oficial/list', { token: token ?? null }),
    findById: (id: number, token?: string | null) =>
        apiClient.get<ResponseOficialDto>(`/oficial/find_by_id/${id}`, { token: token ?? null }),
    findByQcode: (qcode: string, token?: string | null) =>
        apiClient.get<ResponseOficialDto>(`/oficial/find_by_qcode/${encodeURIComponent(qcode)}`, { token: token ?? null }),
    update: (dto: UpdateOficialDto, token?: string | null) =>
        apiClient.post<ResponseOficialDto, UpdateOficialDto>('/oficial/update', dto, { token: token ?? null }),
    deactivate: (qcode: string, token?: string | null) =>
        apiClient.get<ResponseOficialDto>(`/oficial/deactivate/${encodeURIComponent(qcode)}`, { token: token ?? null }),
    assignRole: (oficialId: number, rolId: number, token?: string | null) =>
        apiClient.post<ResponseOficialDto, unknown>(`/oficial/${oficialId}/roles/${rolId}`, {}, { token: token ?? null }),
    removeRole: (oficialId: number, rolId: number, token?: string | null) =>
        apiClient.delete<ResponseOficialDto>(`/oficial/${oficialId}/roles/${rolId}`, { token: token ?? null }),
    getRoles: (oficialId: number, token?: string | null) =>
        apiClient.get<OficialRole[]>(`/oficial/${oficialId}/roles`, { token: token ?? null }),
};
