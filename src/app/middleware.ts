// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(req: NextRequest) {
    const { pathname } = req.nextUrl;
    const isLogin = pathname.startsWith('/login');
    const isPublic = isLogin || pathname.startsWith('/acceso-denegado') || pathname.startsWith('/api') || pathname.startsWith('/_next') || pathname === '/';
    if (isPublic) return NextResponse.next();

    const token = req.cookies.get('token')?.value;
    if (!token) {
        const url = req.nextUrl.clone();
        url.pathname = '/login';
        url.searchParams.set('redirectTo', pathname);
        return NextResponse.redirect(url);
    }
    return NextResponse.next();
}

export const config = {
    matcher: ['/((?!_next/static|_next/image|favicon.ico|assets|images|fonts).*)'],
};
