import { http } from "@/lib/http/client";
import type {
    CreateRolDto,
    UpdateRolDto,
    RolResponseDto,
} from "@/types/role";

const BASE = "/roles";

/** POST /roles/ */
export async function createRol(
    dto: CreateRolDto,
    token: string
): Promise<RolResponseDto> {
    return http<RolResponseDto>(`${BASE}/`, {
        method: "POST",
        token,
        body: dto,
    });
}

/** GET /roles/ */
export async function getAllRoles(token: string): Promise<RolResponseDto[]> {
    return http<RolResponseDto[]>(`${BASE}/`, { token });
}

/** GET /roles/find_by_id/{id} */
export async function findRolById(
    id: number,
    token: string
): Promise<RolResponseDto> {
    return http<RolResponseDto>(`${BASE}/find_by_id/${id}`, { token });
}

/** PUT /roles/{rol_id} */
export async function updateRol(
    rolId: number,
    dto: UpdateRolDto,
    token: string
): Promise<RolResponseDto> {
    return http<RolResponseDto>(`${BASE}/${rolId}`, {
        method: "PUT",
        token,
        body: dto,
    });
}

/** GET /roles/deactivate/{id} */
export async function deactivateRol(
    id: number,
    token: string
): Promise<{ status: string } | RolResponseDto> {
    return http<{ status: string } | RolResponseDto>(`${BASE}/deactivate/${id}`, {
        token,
    });
}
