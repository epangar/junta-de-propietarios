import { Injectable } from '@angular/core';
import { of, throwError } from 'rxjs';
import { delay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

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

  forgotPassword(email: string) {
    return of('Email enviado').pipe(delay(1000));
  }

  getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }
  logout() {
    // limpieza básica de sesión (mock)
    localStorage.removeItem('user');
    return of(true).pipe(delay(500));
  }
  isLoggedIn(): boolean {
    return !!this.getUser();
  }
  // En el futuro, extraeremos el rol dle usuario con this.authService.getUser().role
}