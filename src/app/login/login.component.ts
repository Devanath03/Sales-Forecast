import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import {
  MatSnackBar,
  MatSnackBarHorizontalPosition,
  MatSnackBarVerticalPosition,
} from '@angular/material/snack-bar';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  show: boolean = false;
  username: string;
  password: string;
  message: string;
  color: string;
  duration: any;
  expression: RegExp; 
  horizontalPosition: MatSnackBarHorizontalPosition;
  verticalPosition: MatSnackBarVerticalPosition;
  constructor(private router: Router,private _snackBar: MatSnackBar) {
  }

  ngOnInit(): void {
    this.username="";
    this.password="";
    this.expression = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
  }

  openSnackBar(mgs: string, color: string, duration: any)
  {
    this._snackBar.open(mgs,'',{
      horizontalPosition: "center",
      verticalPosition: "top",
      duration: duration,
      panelClass:["mat-toolbar",color]
    });
  }
  Validate(){
    if(this.username==''){
      this.message = "Username required!";
      this.color = "mat-warn";
      this.duration = 4*1000;
      this.openSnackBar(this.message, this.color, this.duration);
      return false;
    }
    if(!this.expression.test(this.username)){
      this.message = "Invalid username!";
      this.color = "mat-warn";
      this.duration = 4*1000;
      this.openSnackBar(this.message, this.color, this.duration);
      return false;
    }
    if(this.password=='')
      {
      this.message = "Password required!";
      this.color = "mat-warn";
      this.duration = 4*1000;
      this.openSnackBar(this.message, this.color, this.duration);
      return false;
      }
      if(this.password.length < 6)
      {
      this.message = "Password must contain 6 characters!";
      this.color = "mat-warn";
      this.duration = 4*1000;
      this.openSnackBar(this.message, this.color, this.duration);
      return false;
      }
    return true;
  }
  onSubmit(): void {
      if(this.Validate())
      {
        this.message = "Signed in successfully";
        this.color = "primary";
        this.duration = 3*1000;
        this.openSnackBar(this.message, this.color, this.duration);
        this.check(this.username,this.password);
        this.router.navigateByUrl('/dashboard');
      }
  }
  ShowPass(){
    this.show = !this.show;
  }
  SignUp(){
    this.router.navigateByUrl('/sign-up');
  }
  check(username:string,password:string){

  }
}

