import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GastosService } from '../../../services/gastos/gastos.service';
import { AuthService } from '../../../services/auth/auth.service';

@Component({
  selector: 'app-accounting',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './contabilidad.component.html'
})
export class AccountingComponent implements OnInit {

  data: any[] = [];
  //loading = false;

  puerta: string = '';

  constructor(
    private gastosService: GastosService,
    private authService: AuthService
  ) {}

  ngOnInit() {
    const user = this.authService.getUser();
    this.puerta = user?.puerta_usuario;
    if (this.puerta) {
      this.loadData();
    }
  }

  loadData() {
    //this.loading = true;

    this.gastosService.getGastosByPuerta(this.puerta).subscribe({
      next: (res: any) => {
        this.data = [...res];
        //this.loading = false;
      },
      error: (err: any) => {
        console.error(err);
        //this.loading = false;
      }
    });
  }
}