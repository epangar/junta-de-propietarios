import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GastosService } from '../../../services/gastos/gastos.service.py';

@Component({
  selector: 'app-accounting',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './contabilidad.component.html'
})
export class AccountingComponent {

  @Input() puerta: string = '';
  @Input() visible: boolean = false;

  data: any[] = [];
  loading = false;

  constructor(private gastosService: GastosService) {}

  ngOnChanges() {
    if (this.visible && this.puerta) {
      this.loadData();
    }
  }

  loadData() {
    this.loading = true;

    this.gastosService.getGastosByPuerta(this.puerta).subscribe({
      next: (res: any) => {
        this.data = res;
        this.loading = false;
      },
      error: (err: any) => {
        console.error(err);
        this.loading = false;
      }
    });
  }

  close() {
    this.visible = false;
  }
}