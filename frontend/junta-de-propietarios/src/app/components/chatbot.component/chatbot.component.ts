import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatbotService } from '../../services/chatbot/chatbot.service';

import * as pdfjsLib from 'pdfjs-dist';
import * as XLSX from 'xlsx';

(pdfjsLib as any).GlobalWorkerOptions.workerSrc =
  `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js`;

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

  // =========================
  // 📂 SUBIDA Y LECTURA ARCHIVO
  // =========================
  async cargarArchivo(event: any) {
    const file = event.target.files[0];
    if (!file) return;

    this.nombreArchivo = file.name;

    const extension = file.name.split('.').pop()?.toLowerCase();

    if (extension === 'txt') {
      this.leerTXT(file);
    } else if (extension === 'pdf') {
      await this.leerPDF(file);
    } else if (extension === 'xlsx' || extension === 'xls') {
      this.leerExcel(file);
    } else {
      alert('Formato no soportado');
    }
  }

  // TXT
  leerTXT(file: File) {
    const reader = new FileReader();

    reader.onload = () => {
      this.textoDelActa = reader.result as string;
      this.debugTexto();
    };

    reader.readAsText(file);
  }

  // PDF
  async leerPDF(file: File) {
    const reader = new FileReader();

    reader.onload = async () => {
      const typedArray = new Uint8Array(reader.result as ArrayBuffer);
      const pdf = await pdfjsLib.getDocument(typedArray).promise;

      let texto = '';

      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const content = await page.getTextContent();

        texto += content.items.map((item: any) => item.str).join(' ') + '\n';
      }

      this.textoDelActa = texto;
      this.debugTexto();
    };

    reader.readAsArrayBuffer(file);
  }

  // EXCEL
  leerExcel(file: File) {
    const reader = new FileReader();

    reader.onload = (e: any) => {
      const workbook = XLSX.read(e.target.result, { type: 'binary' });

      let texto = '';

      workbook.SheetNames.forEach(sheetName => {
        const sheet = workbook.Sheets[sheetName];
        const json = XLSX.utils.sheet_to_json(sheet, { header: 1 });

        json.forEach((row: any) => {
          texto += row.join(' ') + '\n';
        });
      });

      this.textoDelActa = texto;
      this.debugTexto();
    };

    reader.readAsBinaryString(file);
  }

  // DEBUG
  debugTexto() {
    console.log('📄 ARCHIVO:', this.nombreArchivo);
    console.log('CONTENIDO:', this.textoDelActa);
    console.log('LONGITUD:', this.textoDelActa.length);
  }

  // =========================
  // 💬 ENVIAR PREGUNTA (RAG)
  // =========================
  preguntar() {
    if (!this.miPregunta.trim()) return;

    const pregunta = this.miPregunta;

    this.mensajes.push({
      rol: 'user',
      texto: pregunta
    });

    this.miPregunta = '';
    this.cargando = true;

    this.chatbotService.generarIssues(pregunta, 'TEST')
      .subscribe({
        next: (res: any) => {

          console.log('RESPUESTA BACK:', res);

          const texto = res.issues?.length
            ? res.issues.map((i: any) => `✔ ${i.summary}`).join('\n')
            : 'No se generaron issues';

          this.simularTyping(texto);
          this.cargando = false;
        },

        error: (err) => {
          console.error(err);
          this.simularTyping('Error al procesar la solicitud');
          this.cargando = false;
        }
      });
  }

  // =========================
  // ✨ EFECTO TYPEWRITER
  // =========================
  simularTyping(texto: string) {
    const mensaje: Mensaje = { rol: 'ia', texto: '' };
    this.mensajes.push(mensaje);

    let i = 0;

    const interval = setInterval(() => {
      mensaje.texto += texto[i];
      i++;

      if (i >= texto.length) {
        clearInterval(interval);
      }
    }, 15);
  }
}