import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-predict',
  templateUrl: './predict.component.html',
  styleUrls: ['./predict.component.css']
})
export class PredictComponent implements OnInit {
  predictionImageUrl: string | null = null;

  constructor(private route: ActivatedRoute) { }
12345
  ngOnInit(): void {
    const state = window.history.state;
    if (state && state.predictionImageUrl) {
      this.predictionImageUrl = state.predictionImageUrl;
    }
  }
}
