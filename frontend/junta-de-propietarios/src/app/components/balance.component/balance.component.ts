import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BalanceService } from '../../services/balance/balance.service';
import { AuthService } from '../../services/auth/auth.service';

@Component({
  selector: 'app-balance',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './balance.component.html'
})
export class BalanceGeneralComponent {

  balance: any[] = [];
  user = { role: 'admin' }; // ock rol admin para mostrar balance
  // user = this.authService.getUser();

  constructor(
    private balanceService: BalanceService,
    private authService: AuthService
  ) {}

  ngOnInit() {
    this.loadBalance();
  }

  loadBalance() {
    this.balanceService.getBalance().subscribe({
      next: (res: any) => this.balance = res,
      error: (err: any) => console.error(err)
    });
  }

  createMock() {
    console.log('crear balance (pendiente backend)');
  }

  editMock(item: any) {
    console.log('editar balance:', item);
  }
}