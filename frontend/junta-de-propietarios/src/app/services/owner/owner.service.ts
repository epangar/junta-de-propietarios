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

/**
 * [
  {
    "id_apto": 3,
    "puerta": "3",
    "propietario": "Carlos Pérez",
    "telefono": "600111111",
    "email": "carlos@email.com",
    "cuota_mes": 120,
    "derrama": 30,
    "deuda": 0,
    "estado": "Al día"
  },
  {
    "id_apto": 4,
    "puerta": "4",
    "propietario": "Laura Gómez",
    "telefono": "600222222",
    "email": "laura@email.com",
    "cuota_mes": 120,
    "derrama": 30,
    "deuda": 250,
    "estado": "En mora"
  },
  {
    "id_apto": 5,
    "puerta": "5",
    "propietario": "Miguel Torres",
    "telefono": "600333333",
    "email": "miguel@email.com",
    "cuota_mes": 120,
    "derrama": 30,
    "deuda": 0,
    "estado": "Al día"
  },
  {
    "id_apto": 6,
    "puerta": "6",
    "propietario": "Ana Ruiz",
    "telefono": "600444444",
    "email": "ana@email.com",
    "cuota_mes": 120,
    "derrama": 30,
    "deuda": 80,
    "estado": "En mora"
  },
  {
    "id_apto": 7,
    "puerta": "7",
    "propietario": "Javier León",
    "telefono": "600555555",
    "email": "javier@email.com",
    "cuota_mes": 120,
    "derrama": 30,
    "deuda": 0,
    "estado": "Al día"
  }
]
 */