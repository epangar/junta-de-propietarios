import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { BuildingService } from '../../services/building/building.service';
import { UserService } from '../../services/user/user.service';
import { AuthService } from '../../services/auth/auth.service';
import { User } from '../../models/User.model';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLink, CommonModule],
  templateUrl: './navbar.component.html'
})
export class NavbarComponent {

  user: any = null;

  name :string = "Comunidad los Olivos";
  address :string = "Calle Corrales 12";
  puertaUsuario: string = '';

  constructor(
  private router: Router,
  private buildingService: BuildingService,
  private authService: AuthService
) {}

  ngOnInit() {
    this.user = this.authService.getUser();
    //this.loadUser();
    debugger
    this.puertaUsuario = this.user?.puerta_usuario ?? 'Comunidad los Olivos';
    this.address = this.user?.direccion_usuario ?? 'Calle Corrales 12';
}

loadUser() {
  this.authService.getUser().subscribe({
    next: (user: User) => {
      this.user = user;
    },
    error: (err: any) => {
      console.error(err);
      this.user = null;
    }
  });
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