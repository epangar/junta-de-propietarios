import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class BalanceService {

  constructor(private http: HttpClient) {}

  getBalance() {
    return this.http.get(`${environment.BASEURL}/balance`);
  }

  getBalanceByRange(startDate: string, endDate: string) {
    return this.http.get(
      `${environment.BASEURL}/balance/rango?fecha_inicio=${startDate}&fecha_fin=${endDate}`
    );
  }

  createBalance(balance: any) {
    return this.http.post(`${environment.BASEURL}/balance`, balance);
  }

  updateBalance(id: string, balance: any) {
    return this.http.put(`${environment.BASEURL}/balance/${id}`, balance);
  }
}