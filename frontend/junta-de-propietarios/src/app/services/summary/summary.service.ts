import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SummaryService {

  constructor(private http: HttpClient) {}

  getSummaryByYear(year: number): Observable<any> {

    const token = localStorage.getItem('token');

    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token || ''}`
    });

    return this.http.get(
      `${environment.BASEURL}/resumen/anio/${year}`,
      { headers }
    );
  }

  getSummaryByCategory(category: string): Observable<any> {

    const token = localStorage.getItem('token');

    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token || ''}`
    });

    return this.http.get(
      `${environment.BASEURL}/resumen/categoria/${category}`,
      { headers }
    );
  }

  
}