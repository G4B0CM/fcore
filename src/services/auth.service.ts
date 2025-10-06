import { http } from "@/lib/http/client";
import type {
    AuthRequestDto,
    LoginWireResponse,
    LoginResponseUnified,
    ValidateResponseOk,
} from "@/types/auth";

const BASE = "/auth";

function normalizeLogin(wire: LoginWireResponse): LoginResponseUnified {
    const result = "Result" in wire ? wire.Result : (wire as any).result;
    return { ...result, token_type: "bearer" };
}

/**
 * POST /auth/login
 * Body: { username, password }
 * Res:  { token, username, status, token_type }
 */
export async function login(
    credentials: AuthRequestDto
): Promise<LoginResponseUnified> {
    const wire = await http<LoginWireResponse>(`${BASE}/login`, {
        method: "POST",
        body: credentials,
    });
    return normalizeLogin(wire);
}

/**
 * POST /auth/validate
 * Header: Authorization: Bearer <token>
 * Res: { status: "ok", payload: {...} }
 */
export async function validateToken(
    token: string
): Promise<ValidateResponseOk> {
    return http<ValidateResponseOk>(`${BASE}/validate`, {
        method: "POST",
        token,
    });
}
