import { Injectable } from '@angular/core';
import { of, throwError } from 'rxjs';
import { delay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  login(email: string, password: string) {
    if (email === 'test@test.com' && password === '1234') {
      return of(true).pipe(delay(1000));
    } else {
      return throwError(() => 'Credenciales incorrectas');
    }
  }

  forgotPassword(email: string) {
    return of('Email enviado').pipe(delay(1000));
  }
}