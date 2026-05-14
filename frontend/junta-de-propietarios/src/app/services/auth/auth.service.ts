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

  login(email: string, password: string) {
    return this.http.post<any>(
      `${environment.BASEURL}/auth/login`,
      { email, password }
    ).pipe(
      tap(response => {

        localStorage.setItem('token', response.access_token);

        const user = {
        id_usuario: response.id_usuario,
        email: response.email,
        rol: response.rol,
        puerta_usuario: response.puerta_usuario
      };

        localStorage.setItem('user', JSON.stringify(user));
      })
    );
  }

  logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
  }

  getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  getToken() {
  return localStorage.getItem('token');
}

  getRole() {
    return this.getUser()?.role ?? null;
  }

  isLoggedIn() {
    return !!localStorage.getItem('token');
  }

  forgotPassword(email: string) {
    return this.http.post<any>(
      `${environment.BASEURL}/auth/forgot-password`,
      { email }
    );
  }
}