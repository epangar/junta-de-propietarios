import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SummaryService {

  constructor(private http: HttpClient) {}

  getSummary(year: number) {
    return this.http.get(`${environment.BASEURL}/resumen/${year}`);
  }

  getSummaryCategories(year: number) {
    return this.http.get(`${environment.BASEURL}/resumen/${year}/categorias`);
  }
}