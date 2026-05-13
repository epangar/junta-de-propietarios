import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private http: HttpClient) {}

  //  GET usuarios (cuando backend lo active)
  getUsers() {
    return this.http.get(`${environment.BASEURL}/usuarios`);
  }

  //  crear usuario
  createUser(user: any) {
    return this.http.post(`${environment.BASEURL}/usuarios`, user);
  }

  //  actualizar usuario (PATCH /usuarios/{username})
  updateUser(username: string, user: any) {
    return this.http.patch(
      `${environment.BASEURL}/usuarios/${username}`,
      user
    );
  }

  deactivateUser(username: string) {
    console.log('deactivateUser llamado para:', username);

    // Cuando el backend lo implemente:
    // return this.http.delete(`${environment.BASEURL}/usuarios/${username}`);
  }
}