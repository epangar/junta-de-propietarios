import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { AuthService } from '../auth/auth.service';

export interface Gasto {
  id?: number;
  concepto: string;
  importe: number;
  fecha: string;
  puerta: string;
}

@Injectable({
  providedIn: 'root'
})
export class GastosService {

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {}

  private getHeaders() {
    const token = this.authService.getToken();

    return {
      headers: new HttpHeaders({
        Authorization: `Bearer ${token}`
      })
    };
  }

  // GET /gastos/listar_gasto/{puerta}
  getGastosByPuerta(puerta: string): Observable<Gasto[]> {
    return this.http.get<Gasto[]>(
      `${environment.BASEURL}/gastos/listar_gasto/${puerta}`,
      this.getHeaders()
    );
  }

  // GET /gastos/listar_gasto_fecha/{puerta}?fecha_inicio=...&fecha_fin=...
  getGastosByPuertaAndFecha(
    puerta: string,
    fechaInicio: string,
    fechaFin: string
  ): Observable<Gasto[]> {
    return this.http.get<Gasto[]>(
      `${environment.BASEURL}/gastos/listar_gasto_fecha/${puerta}?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`,
      this.getHeaders()
    );
  }
}