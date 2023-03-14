import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { PredictComponent } from './predict/predict.component';
import { SignUpComponent } from './sign-up/sign-up.component';
const routes: Routes = [
  {
    path:'',component: LoginComponent
  },
  {
    path:'dashboard', component:DashboardComponent
  },
  {
    path:'predict', component:PredictComponent
  },
  {
    path:'sign-up',component:SignUpComponent
  },
  {
    path:'**', component: PageNotFoundComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
