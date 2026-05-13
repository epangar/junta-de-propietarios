import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login';
import { ForgotPasswordComponent } from './components/forgot-password/forgot-password';
import { MainScreen } from './components/main-screen/main-screen';
import { ManageUsersComponent } from './components/manage-users/manage-users';
import { HistoryComponent } from './components/history/history.component';
import { SummaryComponent } from './components/summary/summary.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'forgot-password', component: ForgotPasswordComponent },
  { path: 'home', component: MainScreen},
  { path: 'manage-users', component: ManageUsersComponent },
  { path: 'summary', component: SummaryComponent },
  { path: 'history', component: HistoryComponent },
  { path: '', redirectTo: 'login', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}