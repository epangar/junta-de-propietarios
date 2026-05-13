import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { of, throwError, tap } from 'rxjs';
import { delay } from 'rxjs/operators';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) {}

  // =========================
  // LOGIN (BACKEND REAL)
  // =========================
  login(email: string, password: string) {

    const body = {
      email: email,
      password: password
    };

    return this.http.post<any>(
      `${environment.BASEURL}/auth/login`,
      body
    ).pipe(
      tap(response => {

        // Guardamos token y datos de usuario
        localStorage.setItem('token', response.access_token);

        const user = {
          username: response.username,
          role: response.rol
        };

        localStorage.setItem('user', JSON.stringify(user));
      })
    );
  }

  // =========================
  // LOGOUT (BACKEND REAL)
  // =========================
  logout() {
    return this.http.post(
      `${environment.BASEURL}/auth/logout`,
      {}
    ).pipe(
      tap(() => {
        localStorage.removeItem('user');
        localStorage.removeItem('token');
      })
    );
  }

  // =========================
  // FORGOT PASSWORD (SI EXISTE BACK MÁS TARDE)
  // =========================
  forgotPassword(email: string) {
    return of('Email enviado').pipe(delay(1000));
  }

  // =========================
  // USER HELPERS
  // =========================
  getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  getToken() {
    return localStorage.getItem('token');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  getRole(): string | null {
    const user = this.getUser();
    return user?.role ?? null;
  }

  // =====================================================
  // DUMMY ANTIGUO (NO BORRAR - SOLO PARA REFERENCIA)
  // =====================================================

  /*
  login(email: string, password: string) {
    if (email === 'test@test.com' && password === '1234') {

      const user = {
        email,
        role: email === 'test@test.com' ? 'admin' : 'user'
      };

      localStorage.setItem('user', JSON.stringify(user));

      return of(user).pipe(delay(1000));
    }

    return throwError(() => 'Credenciales incorrectas');
  }

  logout() {
    localStorage.removeItem('user');
    return of(true).pipe(delay(500));
  }
  */
}