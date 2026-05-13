import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { NavbarComponent } from '../navbar/navbar.component';
import { RouterOutlet } from '@angular/router';
@Component({
  selector: 'app-main-screen',
  standalone: true,
  imports: [RouterLink, NavbarComponent, RouterOutlet],
  templateUrl: './main-screen.html'
})
export class MainScreen {

  name :string = "Comunidad los Olivos";
  user = { role: 'admin' };

  constructor(private router: Router) {}

  
}