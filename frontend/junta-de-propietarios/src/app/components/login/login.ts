import { Component } from '@angular/core';
import { AuthService } from '../../services/auth/auth';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.html',
  imports: [FormsModule],
  standalone: true
})
export class LoginComponent {

  email = '';
  password = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onSubmit() {
    this.authService.login(this.email, this.password).subscribe({
      next: () => {
        alert('Login correcto');
        this.router.navigate(['/home']); // 👈 AQUÍ la redirección
      },
      error: (err: any) => alert(err)
    });
  }
}