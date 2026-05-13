import { Injectable } from '@angular/core';
import { CanActivate, CanActivateChild , Router } from '@angular/router';
import { AuthService } from '../services/auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate, CanActivateChild {

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(): boolean {

    const user = this.authService.getUser();

    if (!user) {
      this.router.navigate(['/login'], { replaceUrl: true });
      return false;
    }

    return true;
  }
  
  canActivateChild(): boolean {
    return this.canActivate();
  }
}