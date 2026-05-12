import { Component } from '@angular/core';
import { AuthService } from '../../services/auth/auth';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.html',
    imports: [FormsModule],

})
export class ForgotPasswordComponent {

  email = '';

  constructor(private authService: AuthService) {}

  onSubmit() {
    this.authService.forgotPassword(this.email).subscribe({
      next: (msg) => alert(msg)
    });
  }
}