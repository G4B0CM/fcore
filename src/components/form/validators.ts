export type TextValidator = (value: string) => string | null;

export const required: TextValidator = (v) => (v.trim() === '' ? 'Este campo es obligatorio' : null);
export const minLen = (n: number): TextValidator => (v) => (v.length < n ? `Mínimo ${n} caracteres` : null);
export const email: TextValidator = (v) => (/.+@.+\..+/.test(v) ? null : 'Email inválido');
export const hasLower: TextValidator = (v) => (/[a-z]/.test(v) ? null : 'Debe incluir minúsculas');
export const hasUpper: TextValidator = (v) => (/[A-Z]/.test(v) ? null : 'Debe incluir mayúsculas');
export const hasDigit: TextValidator = (v) => (/\d/.test(v) ? null : 'Debe incluir números');
export const matchField = (otherName: string, otherValue: () => string): TextValidator => (v) =>
    v === otherValue() ? null : `Debe coincidir con ${otherName}`;
