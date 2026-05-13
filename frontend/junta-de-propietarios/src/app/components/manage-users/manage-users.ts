import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { User } from '../../models/User.model';

@Component({
  selector: 'app-manage-users',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './manage-users.html'
})
export class ManageUsersComponent {

  users: User[] = [
    { id: '1', email: 'admin@test.com', role: 'admin' },
    { id: '2', email: 'user1@test.com', role: 'user' },
    { id: '3', email: 'user2@test.com', role: 'user' },
    { id: '4', email: 'manager@test.com', role: 'admin' }
  ];

  selectedUser: any = null;

  formUser = {
    email: '',
    password: '',
    role: 'user'
  };

  // seleccionar usuario para editar
  selectUser(user: any) {
    this.selectedUser = user;

    this.formUser = {
      email: user.email,
      password: '',
      role: user.role
    };
  }

  // reset formulario
  resetForm() {
    this.selectedUser = null;
    this.formUser = {
      email: '',
      password: '',
      role: 'user'
    };
  }

  // crear usuario
  createUser() {
    const newUser: User = {
      id: crypto.randomUUID().toString(),
      email: this.formUser.email,
      password: this.formUser.password,
      role: this.formUser.role 
    };

    this.users.push(newUser);
    this.resetForm();
  }

  // actualizar usuario
  updateUser() {
    if (!this.selectedUser) return;

    const index = this.users.findIndex(u => u.id === this.selectedUser.id);

    if (index !== -1) {
      this.users[index] = {
        ...this.selectedUser,
        ...this.formUser
      };
    }

    this.resetForm();
  }

  // borrar usuario
  deleteUser(id: string) {
    this.users = this.users.filter(u => u.id !== id);
  }

  // decidir acción
  save() {
    this.selectedUser ? this.updateUser() : this.createUser();
  }
}