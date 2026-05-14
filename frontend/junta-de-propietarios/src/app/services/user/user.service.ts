import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { AuthService } from '../auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {}

  // HEADERS CENTRALIZADOS
  private getHeaders() {
    const token = this.authService.getToken();

    return {
      headers: new HttpHeaders({
        Authorization: `Bearer ${token}`
      })
    };
  }

  // GET USERS
  getUsers() {
    return this.http.get(
      `${environment.BASEURL}/usuarios/ver_usuarios`,
      this.getHeaders()
    );
  }

  // CREATE USER
  createUser(user: any) {
    return this.http.post(
      `${environment.BASEURL}/usuarios/insertar_usuario`,
      user,
      this.getHeaders()
    );
  }

  // UPDATE USER (PATCH)
  updateUser(username: string, user: any) {
    return this.http.patch(
      `${environment.BASEURL}/usuarios/modificar_usuario/${username}`,
      user,
      this.getHeaders()
    );
  }

  // DELETE / DEACTIVATE
  deactivateUser(username: string) {
    return this.http.delete(
      `${environment.BASEURL}/usuarios/${username}`,
      this.getHeaders()
    );
  }
}