import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { BalanceService } from '../../services/balance/balance.service';
import { AuthService } from '../../services/auth/auth.service';

@Component({
  selector: 'app-balance',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './balance.component.html'
})
export class BalanceComponent implements OnInit {

  balance: any[] = [];
  user: any = null;

  selectedItem: any = null;

  formBalance = {
    fecha: '',
    ingresos: 0,
    gastos: 0,
    resultado: 0,
    categoria: ''
  };

  loading = false;
  startDate: string = '';
  endDate: string = '';

  constructor(
    private balanceService: BalanceService,
    private authService: AuthService,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit() {
    this.user = this.authService.getUser();
    this.loadBalance();
  }

  loadBalance() {
    this.loading = true;

    this.balanceService.getBalance().subscribe({
      next: (res: any) => {
        this.balance = res;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err: any) => {
        console.error(err);
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }

  //  seleccionar fila
  selectItem(item: any) {
    this.selectedItem = item;

    this.formBalance = {
      fecha: item.fecha,
      ingresos: item.ingresos,
      gastos: item.gastos,
      resultado: item.resultado,
      categoria: item.categoria
    };
  }

  //  reset
  resetForm() {
    this.selectedItem = null;

    this.formBalance = {
      fecha: '',
      ingresos: 0,
      gastos: 0,
      resultado: 0,
      categoria: ''
    };
    this.cdr.detectChanges(); 
  }

  //  crear
  createBalance() {
    this.balanceService.createBalance(this.formBalance).subscribe({
      next: (res: any) => {
        this.balance.push(res);
        this.resetForm();
      },
      error: (err: any) => console.error(err)
    });
  }

  //  actualizar
  updateBalance() {
    if (!this.selectedItem) return;

    this.balanceService.updateBalance(
      this.selectedItem.id_balance,
      this.formBalance
    ).subscribe({
      next: (res: any) => {

        const index = this.balance.findIndex(
          b => b.id_balance === this.selectedItem.id_balance
        );

        if (index !== -1) {
          this.balance[index] = res;
        }

        this.resetForm();
      },
      error: (err: any) => console.error(err)
    });
  }

  // decisión única
  save() {
    this.selectedItem ? this.updateBalance() : this.createBalance();
  }

  filterByRange() {
    if (!this.startDate || !this.endDate) return;

    this.loading = true;

    this.balanceService
      .getBalanceByRange(this.startDate, this.endDate)
      .subscribe({
        next: (res: any) => {
          this.balance = res;
          this.loading = false;
          this.cdr.detectChanges();
        },
        error: (err: any) => {
          console.error(err);
          this.loading = false;
          this.cdr.detectChanges();
        }
      });
  }

  resetFilter() {
    this.startDate = '';
    this.endDate = '';
    this.loadBalance();
  }
}