// Request DTO (igual que tu backend)
export interface AuthRequestDto {
    username: string;
    password: string;
}

// Tu backend devuelve {"Result": {...}, "token_type": "bearer"} (ojo "R" mayúscula)
export interface AuthResponseDto {
    username: string;
    token: string;
    status: number;
}

// Soportamos ambas llaves por robustez
export type LoginWireResponse =
    | { Result: AuthResponseDto; token_type: "bearer" }
    | { result: AuthResponseDto; token_type: "bearer" };

export interface LoginResponseUnified extends AuthResponseDto {
    token_type: "bearer";
}

// /auth/validate devuelve { status: "ok", payload: ... }
export interface ValidateResponseOk {
    status: "ok";
    payload: Record<string, unknown>;
}
