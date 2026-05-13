import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class UserService {

  constructor(private http: HttpClient) {}

  getUsers() {
    return this.http.get(`${environment.BASEURL}/api/users`);
  }

  createUser(user: any) {
    return this.http.post(`${environment.BASEURL}/api/users`, user);
  }

  updateUser(id: string, user: any) {
    return this.http.put(`${environment.BASEURL}/api/users/${id}`, user);
  }

  deleteUser(id: string) {
    return this.http.delete(`${environment.BASEURL}/api/users/${id}`);
  }

  getUserById(id: string) {
    return this.http.get(`${environment.BASEURL}/api/users/${id}`);
  }
}