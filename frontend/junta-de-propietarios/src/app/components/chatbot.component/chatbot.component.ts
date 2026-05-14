import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatbotService } from '../../services/chatbot/chatbot.service';

interface Mensaje {
  rol: 'user' | 'ia';
  texto: string;
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.scss']
})
export class ChatComponent {

  textoDelActa = '';
  miPregunta = '';
  nombreArchivo = '';
  cargando = false;

  mensajes: Mensaje[] = [];

  constructor(private chatbotService: ChatbotService) {}

  cargarArchivo(event: any) {
    const file = event.target.files[0];

    if (!file) return;

    this.nombreArchivo = file.name;

    const reader = new FileReader();

    reader.onload = () => {
      this.textoDelActa = reader.result as string;

      // 👇 DEBUG CLAVE
      console.log('📄 ARCHIVO CARGADO:');
      console.log('Nombre:', this.nombreArchivo);
      console.log('Contenido:', this.textoDelActa);
      console.log('Longitud:', this.textoDelActa.length);
    };

    reader.readAsText(file);
  }

  preguntar() {
    if (!this.miPregunta.trim() || !this.textoDelActa) return;

    const pregunta = this.miPregunta;

    this.mensajes.push({
      rol: 'user',
      texto: pregunta
    });

    this.miPregunta = '';
    this.cargando = true;

    this.chatbotService.enviarConsulta(this.textoDelActa, pregunta)
      .subscribe({
        next: (res) => {
          debugger
          this.simularTyping(res.respuesta);
          this.cargando = false;
        },
        error: () => {
          this.mensajes.push({
            rol: 'ia',
            texto: 'Error conectando con el servidor.'
          });
          debugger
          this.cargando = false;
        }
      });
  }

  // ✨ EFECTO MÁQUINA DE ESCRIBIR
  simularTyping(texto: string) {
    const mensaje: Mensaje = { rol: 'ia', texto: '' };
    this.mensajes.push(mensaje);

    let i = 0;

    const intervalo = setInterval(() => {
      mensaje.texto += texto[i];
      i++;

      if (i >= texto.length) {
        clearInterval(intervalo);
      }
    }, 15); // velocidad typing
  }
}