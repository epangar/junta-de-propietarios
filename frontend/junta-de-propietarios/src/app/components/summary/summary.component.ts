import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SummaryService } from '../../services/summary/summary.service';

@Component({
  selector: 'app-summary',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './summary.component.html'
})
export class SummaryComponent implements OnInit {

  summary: any = null;
  loading = true;
  error: string | null = null;
  year: number = new Date().getFullYear();

  constructor(private summaryService: SummaryService) {}

  ngOnInit() {
    this.summaryService.getSummary(this.year).subscribe({
      next: (data: any) => {
        this.summary = data;
        this.loading = false;
      },
      error: (err: any) => {
        this.error = 'Error cargando resumen';
        this.loading = false;
        console.error(err);
      }
    });
  }
}