import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class OwnerService {

  constructor(private http: HttpClient) {}

  getAll() {
    return this.http.get(`${environment.BASEURL}/propietarios`);
  }

  getByFecha() {
    return this.http.get(`${environment.BASEURL}/propietarios/fecha`);
  }

  getByPuerta(puerta: string) {
    return this.http.get(`${environment.BASEURL}/propietarios/puerta/${puerta}`);
  }

  create(propietario: any) {
    return this.http.post(`${environment.BASEURL}/propietarios`, propietario);
  }

  update(puerta: string, propietario: any) {
    return this.http.patch(`${environment.BASEURL}/propietarios/${puerta}`, propietario);
  }
}