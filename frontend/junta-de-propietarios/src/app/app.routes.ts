import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login';
import { ForgotPasswordComponent } from './components/forgot-password/forgot-password';
import { MainScreen } from './components/main-screen/main-screen';
import { ManageUsersComponent } from './components/manage-users/manage-users.component';
import { HistoryComponent } from './components/history/history.component';
import { SummaryComponent } from './components/summary/summary.component';
import { AuthGuard } from './guard/auth.guard';
import { BalanceComponent } from './components/balance.component/balance.component';
import { ChatComponent } from './components/chatbot.component/chatbot.component';
import { AccountingComponent } from './components/contabilidad/contabilidad.component/contabilidad.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'forgot-password', component: ForgotPasswordComponent },
  {
    path: 'home',
    component: MainScreen,
    canActivate: [AuthGuard],
    canActivateChild: [AuthGuard],
    children: [
      { path: '', redirectTo: 'summary', pathMatch: 'full' },
      { path: 'summary', component: SummaryComponent },
      { path: 'history', component: HistoryComponent },
      { path: 'manage-users', component: ManageUsersComponent },
      { path: 'balance', component: BalanceComponent },
      { path: 'chatbot', component: ChatComponent },
      {path: 'contabilidad', component: AccountingComponent }
    ]
  },
  { path: '', redirectTo: 'login', pathMatch: 'full' }
  // { path: 'manage-users', component: ManageUsersComponent },
  // { path: 'summary', component: SummaryComponent },
  // { path: 'history', component: HistoryComponent },

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }