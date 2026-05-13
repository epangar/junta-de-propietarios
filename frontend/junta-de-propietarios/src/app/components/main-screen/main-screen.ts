import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-main-screen',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './main-screen.html'
})
export class MainScreen {

  constructor(private router: Router) {}

  logout() {
    alert('Sesión cerrada');
    this.router.navigate(['/login']);
  }
}