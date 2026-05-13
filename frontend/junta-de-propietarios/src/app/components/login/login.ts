import { Component } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';


@Component({
  selector: 'app-login',
  templateUrl: './login.html',
  imports: [FormsModule, RouterLink],
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
        this.router.navigate(['/home']); 
      },
      error: (err: any) => alert(err)
    });
  }
}