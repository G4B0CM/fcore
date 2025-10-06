import { ApiError } from "./errors";
import { buildUrl } from "@/config/api";

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export interface HttpOptions {
    method?: HttpMethod;
    token?: string;               // Pásalo cuando el endpoint requiera Authorization
    body?: unknown;               // Se serializa a JSON automáticamente
    headers?: HeadersInit;
    signal?: AbortSignal;
}

export async function http<T>(path: string, opts: HttpOptions = {}): Promise<T> {
    const { method = "GET", token, body, headers, signal } = opts;

    const finalHeaders: HeadersInit = {
        ...(body ? { "Content-Type": "application/json" } : {}),
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...headers,
    };

    const res = await fetch(buildUrl(path), {
        method,
        headers: finalHeaders,
        body: body ? JSON.stringify(body) : undefined,
        signal,
        cache: "no-store",            // evita cache accidental en app router
        // next: { revalidate: 0 },   // alternativa si prefieres esta API
    });

    // Intenta parsear JSON siempre que sea posible
    let data: any = null;
    const text = await res.text();
    if (text) {
        try { data = JSON.parse(text); } catch { data = text; }
    }

    if (!res.ok) {
        const message =
            (data && (data.detail || data.message)) ||
            `HTTP ${res.status} ${res.statusText}`;
        throw new ApiError(message, res.status, data);
    }

    return data as T;
}
