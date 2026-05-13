import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLink, CommonModule],
  templateUrl: './navbar.component.html'
})
export class NavbarComponent {

  // 👇 MOCK temporal (mañana lo conectas a AuthService)
  user = {
    role: 'admin' // cambia a 'user' para probar
  };

  logout() {
    console.log('logout');
  }
}