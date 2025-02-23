import {Component, ViewEncapsulation,OnInit,ElementRef, ViewChild} from '@angular/core';
import {FormControl} from '@angular/forms';
import { MatSnackBar, MatSnackBarHorizontalPosition,MatSnackBarVerticalPosition, } from '@angular/material/snack-bar';
import { HttpClient,HttpHeaders } from '@angular/common/http';
import {Router} from '@angular/router';
import { _isNumberValue } from '@angular/cdk/coercion';
import {ActivatedRoute, RouterModule} from '@angular/router';
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
          this.openSnackBar("Please select only CSV file", "X", this.duration);
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

  fileUpload(): void {
    if (this.file && this.validate()) {
      const formData = new FormData();
      formData.append('file', this.file);
      formData.append('select', this.selected);
      formData.append('period', this.period);

      const headers = new HttpHeaders();
      headers.append('Accept', 'application/json');
      //http://192.168.1.2:5000/api/fileupload ---> for local server
      this.http.post("https://devanath03.pythonanywhere.com/api/fileupload", formData, { headers, responseType: 'blob' })
        .subscribe((response: Blob) => {
          const reader = new FileReader();
          reader.onloadend = () => {
            const imageUrl = reader.result as string;
            this.router.navigate(['/predict'], { state: { predictionImageUrl: imageUrl } });
          };
          reader.readAsDataURL(response);
        }, error => {
          console.error('Error uploading file:', error);
          this.openSnackBar('Error uploading file', 'X',this.duration);
        });
    } else {
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
