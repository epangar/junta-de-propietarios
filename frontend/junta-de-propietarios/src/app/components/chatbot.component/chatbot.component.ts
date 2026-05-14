import { Component } from '@angular/core';
import { CommonModule } from '@angular/common'; // ¡IMPORTANTE! Para *ngIf y *ngFor
import { FormsModule } from '@angular/forms';
import { ChatbotService } from '../../services/chatbot/chatbot.service';

interface Mensaje {
  rol: 'user' | 'ia';
  texto: string;
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule], // Añadido CommonModule
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.scss']
})
export class ChatComponent {
  textoDelActa: string = '';
  miPregunta: string = '';
  nombreArchivo: string = ''; // La variable que faltaba
  cargando: boolean = false;   // Para el spinner/estado de carga
  mensajes: Mensaje[] = [];    // Para mostrar la conversación

  constructor(private chatbotService: ChatbotService) {}

  cargarArchivo(event: any) {
    const archivo = event.target.files[0];
    if (archivo) {
      this.nombreArchivo = archivo.name; // Guardamos el nombre para el HTML
      const reader = new FileReader();
      reader.onload = () => {
        this.textoDelActa = reader.result as string;
      };
      reader.readAsText(archivo);
    }
  }

  preguntar() {
    if (!this.miPregunta.trim() || !this.textoDelActa) return;

    // 1. Añadimos tu pregunta a la lista de mensajes
    this.mensajes.push({ rol: 'user', texto: this.miPregunta });
    
    const preguntaActual = this.miPregunta;
    this.miPregunta = ''; // Limpiamos el input
    this.cargando = true;  // Activamos estado de carga

    // 2. Llamada al servicio
    this.chatbotService.enviarConsulta(this.textoDelActa, preguntaActual)
      .subscribe({
        next: (res) => {
          // 3. Añadimos la respuesta de la IA
          this.mensajes.push({ rol: 'ia', texto: res.respuesta });
          this.cargando = false;
        },
        error: (err) => {
          console.error('Error en el back:', err);
          this.mensajes.push({ rol: 'ia', texto: 'Lo siento, hubo un error en la conexión.' });
          this.cargando = false;
        }
      });
  }
}