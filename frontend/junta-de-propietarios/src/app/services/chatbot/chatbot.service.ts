import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { AuthService } from '../auth/auth.service';

// Definimos la interfaz para la respuesta de la IA (ajusta según tu back)
export interface ChatResponse {
  respuesta: string;
  timestamp: string;
}

@Injectable({
  providedIn: 'root' // Compatible con standalone components
})
export class ChatbotService {

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {}

  /**
   * Genera los headers incluyendo el token de sesión
   */
  private getHeaders() {
    const token = this.authService.getToken();
    return {
      headers: new HttpHeaders({
        Authorization: `Bearer ${token}`
      })
    };
  }

  /**
   * Envía el texto extraído del acta y la pregunta del usuario
   * @param contenido El texto plano del archivo .txt
   * @param pregunta La consulta del usuario
   */
  enviarConsulta(contenido: string, pregunta: string): Observable<ChatResponse> {
    const body = {
      contexto: contenido,
      prompt: pregunta
    };

    return this.http.post<ChatResponse>(
      `${environment.BASEURL}/chatbot`,
      body,
      this.getHeaders()
    );
  }
}