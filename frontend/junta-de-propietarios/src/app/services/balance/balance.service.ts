import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { AuthService } from '../auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class BalanceService {

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {}

  private getHeaders() {
    const token = this.authService.getToken();

    return {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${token}`
      })
    };
  }

  getBalance() {
    return this.http.get(
      `${environment.BASEURL}/balance`,
      this.getHeaders()
    );
  }

  getBalanceByRange(startDate: string, endDate: string) {
    return this.http.get(
      `${environment.BASEURL}/balance/rango?fecha_inicio=${startDate}&fecha_fin=${endDate}`,
      this.getHeaders()
    );
  }

  createBalance(balance: any) {
    return this.http.post(
      `${environment.BASEURL}/balance`,
      balance,
      this.getHeaders()
    );
  }

  updateBalance(id: string, balance: any) {
    return this.http.put(
      `${environment.BASEURL}/balance/${id}`,
      balance,
      this.getHeaders()
    );
  }
}

/**
 * Respuestas:
 * 
 * get balance
 * [
  {
    "resultado": 0,
    "fecha": "2026-05-13",
    "gastos": 0,
    "ingresos": 0,
    "id_balance": 0
  }
]


get balane rango

GET
/balance/rango
Ver Balance Rango


Parameters
Try it out
Name	Description
fecha_inicio *
string($date)
(query)
fecha_inicio
fecha_fin *
string($date)
(query)
fecha_fin
Responses
Code	Description	Links
200	
Successful Response

Media type

application/json
Controls Accept header.
Example Value
Schema
[
  {
    "resultado": 0,
    "fecha": "2026-05-13",
    "gastos": 0,
    "ingresos": 0,
    "id_balance": 0
  }
]
No links
422	
Validation Error

Media type

application/json
Example Value
Schema
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string",
      "input": "string",
      "ctx": {}
    }
  ]
}
 */