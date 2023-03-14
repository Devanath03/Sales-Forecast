import {Component, ViewEncapsulation,OnInit,ElementRef, ViewChild} from '@angular/core';
import {FormControl} from '@angular/forms';
import { MatSnackBar, MatSnackBarHorizontalPosition,MatSnackBarVerticalPosition, } from '@angular/material/snack-bar';
import { HttpClient,HttpHeaders } from '@angular/common/http';
import {Router} from '@angular/router';
import { _isNumberValue } from '@angular/cdk/coercion';
@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
  encapsulation: ViewEncapsulation.None,
})

export class DashboardComponent implements OnInit{

  @ViewChild('fileSelect') myInputVariable?: ElementRef;

  value: string;
  period: string;
  filename: any;
  format: any;
  formfile: any;
  file:any;
  panelColor = new FormControl('');
  selected: any;
  horizontalPosition: MatSnackBarHorizontalPosition;
  verticalPosition: MatSnackBarVerticalPosition;
  duration: any;


  constructor(
    private _snackBar: MatSnackBar,
    private http: HttpClient,
    private router: Router
  ) { }

  ngOnInit(): void{
    this.selected = "";
    this.period = "";
    this.file = null;
    this.duration = 4*1000;
  }

  onFileSelect(event: any) {
    try {
       this.file = event.target.files[0];
      if (this.file) {
        this.filename = this.file.name;
        this.format = this.file.name.split('.');
        if (this.format[1] != 'csv') {
          this._snackBar.open("Please select only CSV file", "X", { duration: 3000 });
          this.deleteFile();
        } else {
          this.formfile = new FormData();
          this.formfile.append('file', this.file);
          this.formfile.append('period', this.period);
          this.formfile.append('select', this.selected);

          console.log("file", this.formfile);
        }
      }
    } catch (error) {
      this.deleteFile();
      console.log('no file was selected...');
    }
  }

  fileUpload(): void{
    if (this.file && this.validate()) {
      let url = "http://localhost:5000/api/file_upload"
      this.http.post(url, this.formfile).subscribe((res) => {
        this.openSnackBar("Predicted successfully", "X", this.duration);
        this.router.navigateByUrl('/predict');
      },
        (error) => {
          this.openSnackBar(error.message, "X",this.duration);
        });
    }
    else{
      this.validate();
    }
  }

  deleteFile(){
    this.file = null;
    this.format = null;
    this.filename = null;
    this.formfile.delete('file');
    // this.fileSelect
  }

  validate(){
    if(this.selected == '')
    {
      this.openSnackBar("Please select periodicity", "X", this.duration);
      return false;
    }
    if(this.period == '')
    {
      this.openSnackBar("Please select time interval","X",this.duration);
      return false;
    }
    if(!(this.period>='1' && this.period<='9'))
    {
      this.openSnackBar("Incorrect time interval","X",this.duration);
      return false;
    }
    if(this.file == null)
    {
      this.openSnackBar("Please select the file", "X", this.duration);
      return false;
    }
    return true;
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
}
