import { http } from "@/lib/http/client";
import type {
    CreateOficialDto,
    UpdateOficialDto,
    ResponseOficialDto,
    OficialFull,
} from "@/types/oficial";
import type { RolResponseDto } from "@/types/role";

const BASE = "/oficial";

/** POST /oficial/create */
export async function createOficial(
    dto: CreateOficialDto,
    token: string
): Promise<ResponseOficialDto> {
    return http<ResponseOficialDto>(`${BASE}/create`, {
        method: "POST",
        token,
        body: dto,
    });
}

/** GET /oficial/list */
export async function listOficiales(
    token: string
): Promise<ResponseOficialDto[] | OficialFull[]> {
    return http<ResponseOficialDto[] | OficialFull[]>(`${BASE}/list`, {
        token,
    });
}

/** GET /oficial/find_by_id/{id} */
export async function findOficialById(
    id: number,
    token: string
): Promise<ResponseOficialDto | OficialFull> {
    return http<ResponseOficialDto | OficialFull>(`${BASE}/find_by_id/${id}`, {
        token,
    });
}

/** GET /oficial/find_by_qcode/{qcode} */
export async function findOficialByQcode(
    qcode: string,
    token: string
): Promise<ResponseOficialDto | OficialFull> {
    return http<ResponseOficialDto | OficialFull>(`${BASE}/find_by_qcode/${qcode}`, {
        token,
    });
}

/** POST /oficial/update */
export async function updateOficial(
    dto: UpdateOficialDto,
    token: string
): Promise<ResponseOficialDto | OficialFull> {
    return http<ResponseOficialDto | OficialFull>(`${BASE}/update`, {
        method: "POST",
        token,
        body: dto,
    });
}

/** GET /oficial/deactivate/{qcode} */
export async function deactivateOficial(
    qcode: string,
    token: string
): Promise<{ status: string } | ResponseOficialDto> {
    return http<{ status: string } | ResponseOficialDto>(`${BASE}/deactivate/${qcode}`, {
        token,
    });
}

/** POST /oficial/{oficial_id}/roles/{rol_id} */
export async function assignRolToOficial(
    oficialId: number,
    rolId: number,
    token: string
): Promise<ResponseOficialDto | OficialFull> {
    return http<ResponseOficialDto | OficialFull>(`${BASE}/${oficialId}/roles/${rolId}`, {
        method: "POST",
        token,
    });
}

/** DELETE /oficial/{oficial_id}/roles/{rol_id} */
export async function removeRolFromOficial(
    oficialId: number,
    rolId: number,
    token: string
): Promise<ResponseOficialDto | OficialFull> {
    return http<ResponseOficialDto | OficialFull>(`${BASE}/${oficialId}/roles/${rolId}`, {
        method: "DELETE",
        token,
    });
}

/** GET /oficial/{oficial_id}/roles */
export async function getRolesForOficial(
    oficialId: number,
    token: string
): Promise<RolResponseDto[]> {
    return http<RolResponseDto[]>(`${BASE}/${oficialId}/roles`, { token });
}
