import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SummaryService } from '../../services/summary/summary.service';
import { ChangeDetectorRef } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-summary',
  standalone: true,
imports: [CommonModule, FormsModule],
  templateUrl: './summary.component.html'
})
export class SummaryComponent implements OnInit {

  summary: any = null;
  loading = true;
  error: string | null = null;

  year: number = 2026;

  constructor(
    private summaryService: SummaryService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.year = new Date().getFullYear();
    this.loadSummary();
  }

  loadSummary() {
    const token = localStorage.getItem('token');

    if (!token) {
      this.error = 'No autenticado';
      this.loading = false; // 👈 AQUÍ
      return;
    }

    this.loading = true;
    this.error = null;

    this.summaryService.getSummary(this.year).subscribe({
      next: (data: any) => {
        this.summary = data;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err: any) => {
        this.error = 'Error cargando resumen';
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }
}