import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HistoryService } from '../../services/history/history.service';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './history.component.html'
})
export class HistoryComponent implements OnInit {

  movements: any[] = [];
  loading = true;
  error: string | null = null;

  constructor(private historyService: HistoryService) {}

  ngOnInit() {
    this.historyService.getHistory().subscribe({
      next: (data: any) => {
        this.movements = data;
        this.loading = false;
      },
      error: (err: Error) => {
        this.error = 'Error cargando movimientos';
        this.loading = false;
        console.error(err);
      }
    });
  }
}