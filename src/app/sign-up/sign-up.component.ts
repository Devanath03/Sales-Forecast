import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import { HttpClient,HttpHeaders } from '@angular/common/http';
import {
  MatSnackBar,
  MatSnackBarHorizontalPosition,
  MatSnackBarVerticalPosition,
} from '@angular/material/snack-bar';
@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit{
  cshow: boolean = false;
  show: boolean = false;
  username: string;
  password: string;
  cpassword: string;
  message: string;
  color: string;
  duration: any;
  expression: RegExp; 
  horizontalPosition: MatSnackBarHorizontalPosition;
  verticalPosition: MatSnackBarVerticalPosition;
  formfile: any;

  constructor(private router: Router,private _snackBar: MatSnackBar,private http: HttpClient,) {
  }

  ngOnInit(): void {
    this.username="";
    this.password="";
    this.expression = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
  }
  ShowPass(){
    this.show = !this.show;
  }
  cShowPass(){
    this.cshow = !this.cshow;
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
  onSubmit(){
    if(this.Validate())
    {
        this.message = "Account created successfully";
        this.color = "primary";
        this.duration = 2*1000;
        this.formfile = new FormData();
        this.formfile.append('username', this.username);
        this.formfile.append('password', this.password);
        let url = "https://devanath03.pythonanywhere.com/api/register-user" //http://192.168.1.2:5000/api/register-user ---> for locl server
        this.http.post(url, this.formfile).subscribe((res) => {
        this.openSnackBar(this.message, this.color, this.duration);
        this.router.navigateByUrl('/');
      },
        (error) => {
        this.openSnackBar(error.message,this.color,this.duration);
        });
    }
  }
  Validate()
  {
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
      if(!(this.password===this.cpassword))
      {
      this.message = "Password mismatching!";
      this.color = "mat-warn";
      this.duration = 4*1000;
      this.openSnackBar(this.message, this.color, this.duration);
      return false;
      }
    return true;
  }
  LogIn()
  {
    this.router.navigateByUrl('/');
  }
}
