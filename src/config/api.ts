export const API_BASE_URL =
    process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8080";

export const buildUrl = (path: string) =>
    path.startsWith("http") ? path : `${API_BASE_URL}${path}`;
