import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
1234567
@Component({
  selector: 'app-predict',
  templateUrl: './predict.component.html',
  styleUrls: ['./predict.component.css']
})
export class PredictComponent implements OnInit {
  predictionImageUrl: string | null = null;

  constructor(private route: ActivatedRoute) { }

  ngOnInit(): void {
    const state = window.history.state;
    if (state && state.predictionImageUrl) {
      this.predictionImageUrl = state.predictionImageUrl;
    }
  }
}
