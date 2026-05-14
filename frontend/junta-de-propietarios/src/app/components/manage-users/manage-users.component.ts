import { ChangeDetectorRef, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { UserService } from '../../services/user/user.service';
import { AuthService } from '../../services/auth/auth.service';

@Component({
  selector: 'app-manage-users',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './manage-users.component.html'
})
export class ManageUsersComponent {

  users: any[] = [];
  selectedUser: any = null;

  formUser = {
    email: '',
    password: '',
    role: 'user'
  };

  // user = { role: 'admin' }; // ock rol admin para mostrar gestión de usuarios
  user = {role: ''}; // rol real desde localStorage

  constructor(
    private userService: UserService,
    private authService: AuthService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.user = this.authService.getUser();
    this.loadUsers();
  }

  //  GET usuarios (cuando lo tengas en backend)
  loadUsers() {
    // si aún no existe GET, esto se puede mockear
    this.users  = [
  { id: '1', email: 'admin@test.com', role: 'admin', password: '' },
  { id: '2', email: 'user1@test.com', role: 'user', password: '' },
  { id: '3', email: 'user2@test.com', role: 'user', password: '' },
  { id: '4', email: 'manager@test.com', role: 'admin', password: '' },
  { id: '5', email: 'user3@test.com', role: 'user', password: '' },
  { id: '6', email: 'user4@test.com', role: 'user', password: '' },
  { id: '7', email: 'user5@test.com', role: 'user', password: '' },
  { id: '8', email: 'user6@test.com', role: 'user', password: '' },
  { id: '9', email: 'user7@test.com', role: 'user', password: '' },
  { id: '10', email: 'user8@test.com', role: 'admin', password: '' },
  { id: '11', email: 'user9@test.com', role: 'user', password: '' },
  { id: '12', email: 'user10@test.com', role: 'user', password: '' }
];
  }

  //  seleccionar usuario
  selectUser(user: any) {
    this.selectedUser = user;

    this.formUser = {
      email: user.email,
      password: '',
      role: user.role
    };
  }

  //  reset form
  resetForm() {
    this.selectedUser = null;
    this.formUser = {
      email: '',
      password: '',
      role: 'user'
    };
  }

  //  crear usuario (POST /usuarios)
  createUser() {
    this.userService.createUser(this.formUser).subscribe({
      next: (res: any) => {
        this.users.push(res);
        this.resetForm();
      },
      error: (err: any) => console.error(err)
    });
  }

  //  actualizar usuario (PATCH /usuarios/{username})
  updateUser() {
    if (!this.selectedUser) return;

    this.userService.updateUser(
      this.selectedUser.email,
      this.formUser
    ).subscribe({
      next: (res: any) => {

        const index = this.users.findIndex(
          u => u.email === this.selectedUser.email
        );

        if (index !== -1) {
          this.users[index] = res;
        }

        this.resetForm();
      },
      error: (err: any) => console.error(err)
    });
  }

  //  decidir acción
  save() {
    this.selectedUser ? this.updateUser() : this.createUser();
  }

  //  deactivate (temporal frontend)
  deactivateUser(user: any) {
    this.users = this.users.filter(u => u.email !== user.email);
  }

  //  acción contabilidad
  openAccounting(user: any) {
    console.log('Contabilidad del usuario:', user);
  }
}