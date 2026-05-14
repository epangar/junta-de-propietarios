import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { UserService } from '../../services/user/user.service';
import { AuthService } from '../../services/auth/auth.service';
import { AccountingComponent } from '../contabilidad/contabilidad.component/contabilidad.component';

@Component({
  selector: 'app-manage-users',
  standalone: true,
  imports: [CommonModule, FormsModule, AccountingComponent],
  templateUrl: './manage-users.component.html'
})
export class ManageUsersComponent implements OnInit {

  users: any[] = [];
  selectedUser: any = null;

  // SOLO UI FORM
  formUser = {
    email: '',
    password: '',
    rol: 'user',
    puerta_usuario: '' as string | null
  };

  user: any = { rol: '' };

  showAccounting = false;
  selectedPuerta = '';

  constructor(
    private userService: UserService,
    private authService: AuthService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.user = this.authService.getUser();
    this.loadUsers();
  }

  loadUsers() {
    this.userService.getUsers().subscribe({
      next: (res: any) => {
        this.users = res;
        this.cdr.detectChanges();
      },
      error: (err: any) => console.error(err)
    });
  }

  selectUser(user: any) {
    this.selectedUser = user;

    this.formUser = {
      email: user.email,
      password: '',
      rol: user.rol,
      puerta_usuario: user.puerta_usuario || null
    };
  }

  resetForm() {
    this.selectedUser = null;

    this.formUser = {
      email: '',
      password: '',
      rol: 'user',
      puerta_usuario: null
    };
  }

  createUser() {
    const payload = {
      email: this.formUser.email,
      rol: this.formUser.rol,
      puerta_usuario: this.formUser.puerta_usuario || null,
      activo: true
    };

    this.userService.createUser(payload).subscribe({
      next: (res: any) => {
        this.users.push(res);
        this.resetForm();
        this.cdr.detectChanges();
      },
      error: (err: any) => console.error(err)
    });
  }

  updateUser() {
    if (!this.selectedUser) return;

    const payload = {
      email: this.formUser.email,
      rol: this.formUser.rol,
      puerta_usuario: this.formUser.puerta_usuario || null,
      activo: this.selectedUser.activo
    };

    this.userService.updateUser(this.selectedUser.email, payload)
      .subscribe({
        next: (res: any) => {

          const index = this.users.findIndex(
            u => u.email === this.selectedUser.email
          );

          if (index !== -1) {
            this.users[index] = res;
          }

          this.resetForm();
          this.cdr.detectChanges();
        },
        error: (err: any) => console.error(err)
      });
  }

  save() {
    this.selectedUser ? this.updateUser() : this.createUser();
  }

  toggleActive(user: any) {
    const payload = {
      ...user,
      activo: !user.activo
    };

    this.userService.updateUser(user.email, payload)
      .subscribe({
        next: (res: any) => {

          const index = this.users.findIndex(
            u => u.email === user.email
          );

          if (index !== -1) {
            this.users[index] = res;
          }

          this.cdr.detectChanges();
        },
        error: (err: any) => console.error(err)
      });
  }

  openAccounting(user: any) {
    this.selectedPuerta = user.puerta_usuario;
    this.showAccounting = true;
  }

  closeAccounting() {
    this.showAccounting = false;
    this.selectedPuerta = '';
  }
}