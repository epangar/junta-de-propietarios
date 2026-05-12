import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-main-screen',
  standalone: true,
  templateUrl: './main-screen.html'
})
export class MainScreen {

  constructor(private router: Router) {}

  logout() {
    alert('Sesión cerrada');
    this.router.navigate(['/login']);
  }
}