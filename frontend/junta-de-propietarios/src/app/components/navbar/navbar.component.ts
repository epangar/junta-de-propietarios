import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
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

   constructor(private router: Router) {}
  
  logout() {
    alert('Sesión cerrada');
    this.router.navigate(['/login'], { replaceUrl: true });
  }
}