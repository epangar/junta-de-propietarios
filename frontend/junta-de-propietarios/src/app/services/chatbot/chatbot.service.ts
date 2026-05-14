import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { AuthService } from '../auth/auth.service';
import { Observable } from 'rxjs';

export interface ChatResponse {
  respuesta: string;
  timestamp: string;
}

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {

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

  enviarConsulta(contenido: string, pregunta: string): Observable<ChatResponse> {
    console.log("Dentro del servicio! El texto es:", contenido);
    debugger
    return this.http.post<ChatResponse>(
      `${environment.BASEURL}/chatbot`,
      {
        contexto: contenido,
        prompt: pregunta
      },
      this.getHeaders()
    );
  }
}