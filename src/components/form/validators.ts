export type TextValidator = (v: any) => string | null;

export const required: TextValidator = (v: any) => {
    if (v === null || v === undefined) return 'Este campo es obligatorio';
    if (typeof v === 'string') return v.trim() === '' ? 'Este campo es obligatorio' : null;
    if (Array.isArray(v)) return v.length === 0 ? 'Este campo es obligatorio' : null;
    return v ? null : 'Este campo es obligatorio';
};

export const minLen = (n: number): TextValidator => (v: any) => {
    const s = typeof v === 'string' ? v : v == null ? '' : String(v);
    return s.trim().length < n ? `Mínimo ${n} caracteres` : null;
};

export type NumberValidator = (value: number | null) => string | null;
export type BoolValidator = (value: boolean) => string | null;

export const numberRequired: NumberValidator = (v) => (v === null || Number.isNaN(v) ? 'Valor requerido' : null);
export const numberMin = (n: number): NumberValidator => (v) => (v === null ? 'Valor requerido' : v < n ? `Mínimo ${n}` : null);
export const numberMax = (n: number): NumberValidator => (v) => (v === null ? 'Valor requerido' : v > n ? `Máximo ${n}` : null);
export const numberBetween = (a: number, b: number): NumberValidator => (v) =>
    v === null ? 'Valor requerido' : v < a || v > b ? `Entre ${a} y ${b}` : null;

export const mustBeTrue: BoolValidator = (v) => (v ? null : 'Debe estar activado');

export const dateRequired = (d: Date | null) => (d ? null : 'Fecha requerida');
export const minDate = (m: Date) => (d: Date | null) => (!d ? 'Fecha requerida' : d < m ? `Mínimo ${m.toLocaleDateString()}` : null);
export const maxDate = (m: Date) => (d: Date | null) => (!d ? 'Fecha requerida' : d > m ? `Máximo ${m.toLocaleDateString()}` : null);

export const chipsRequired = (arr: string[]) => (arr.length ? null : 'Agrega al menos un valor');
export const chipsMax = (n: number) => (arr: string[]) => (arr.length > n ? `Máximo ${n} elementos` : null);

export const multiRequired = <T,>(arr: T[]) => (arr.length ? null : 'Selecciona al menos uno');

export const radioRequired = <T,>(val: T | null) => (val ? null : 'Selecciona una opción');

export const filesRequired = (fs: File[]) => (fs.length ? null : 'Selecciona archivos');
export const filesMax = (n: number) => (fs: File[]) => (fs.length > n ? `Máximo ${n} archivos` : null);
export const filesTotalSizeMax = (bytes: number) => (fs: File[]) =>
    fs.reduce((a, f) => a + (f.size || 0), 0) > bytes ? `Tamaño total supera ${Math.round(bytes / 1024 / 1024)}MB` : null;
