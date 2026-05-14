import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { AuthService } from '../auth/auth.service';
import { Observable } from 'rxjs';

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

  // 🟣 1. SUBIR ARCHIVO (PDF, TXT, EXCEL...)
  uploadFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post(
      `${environment.BASEURL}/upload-file`,
      formData,
      this.getHeaders()
    );
  }

  // 🔵 2. PREGUNTAR (RAG)
  query(question: string): Observable<any> {
    return this.http.post(
      `${environment.BASEURL}/query`,
      { question },
      this.getHeaders()
    );
  }

  // 🟢 3. GENERAR ISSUES JIRA
  generarIssues(texto: string, projectKey: string): Observable<any> {
    return this.http.post(
      `${environment.BASEURL}/issues/ai-generate`,
      {
        text: texto,
        project_key: projectKey
      },
      this.getHeaders()
    );
  }
}