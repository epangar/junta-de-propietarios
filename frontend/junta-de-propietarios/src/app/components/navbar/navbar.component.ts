import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { BuildingService } from '../../services/building/building';

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

  name :string = "Comunidad los Olivos";
  address :string = "Calle Falsa 123";

  constructor(private router: Router, private buildingService: BuildingService) {}

  ngOninit() {

  }

  getBuildingData() {
    this.buildingService.getBuilding().subscribe({
      next: (res: any) => {
        this.name = res.nombre;
        this.address = res.direccion;
      },
      error: (err: any) => {
        console.error('Error cargando edificio:', err);
      }
    });
  }     
  
  logout() {
    alert('Sesión cerrada');
    this.router.navigate(['/login'], { replaceUrl: true });
  }
}