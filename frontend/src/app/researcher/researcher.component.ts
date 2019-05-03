import { Component, OnInit } from '@angular/core';
import { AppService } from '../app.service';

@Component({
  selector: 'app-researcher',
  templateUrl: './researcher.component.html',
  styleUrls: ['./researcher.component.css']
})
export class ResearcherComponent implements OnInit {

  selectedRegion: string;
  selectedAnalytic: string;
  from: string;
  to: string;
  regions: Array<String> = ['Bio Design Building Break Room 1', 'Bio Design Building Break Room 2', 'Bio Design Building Break Room 3'];
  analytics: Array<String> = ['Max', 'Min', 'Average'];
  displayedColumns: string[] = ['controller', 'temperature', 'ec', 'ph', 'timestamp'];
  rows = [];
  tempValue: string;
  ecValue: string;
  phValue: string;
  tempTime: string;
  ecTime: string;
  phTime: string;
  analyticText: string;

  constructor(private appService: AppService) { }

  ngOnInit() {
  }

  changeAnalytic(){
    this.analyticText = "";
  }

  fetchData() {

    this.phValue = "";
    this.ecValue = "";
    this.tempValue = "";
    this.phTime = "";
    this.ecTime = "";
    this.tempTime = "";

    this.from = this.from.trim();
    this.to = this.to.trim();
    this.analyticText = this.selectedAnalytic;
    this.rows = [];

    debugger;
    this.appService.getDataInRange(this.selectedRegion, this.from, this.to).subscribe((res: any) => {
      for (let i = 0; i < res.length; i++) {
        this.rows.push({
          'temp': res[i].temperature, 'controller': res[i].controller_id, 'time': res[i].timestamp, 'ec': res[i].ec,
          'ph': res[i].ph
        });
      }
    });

    this.appService.getAnalytics(this.selectedRegion, this.from, this.to, this.selectedAnalytic)
      .subscribe((res: any) => {
        for (let i = 0; i < res.length; i++) {
          if (this.tempValue == "" && res[i].Column == "Temperature") {
            this.tempValue = parseFloat(res[i].value).toFixed(2);
            if (this.selectedAnalytic != "Average") {
              this.tempTime = res[i].DATE;
              this.tempTime = this.tempTime.replace('T', ' ');
              this.tempTime = '|' + this.tempTime.substring(0, this.tempTime.lastIndexOf('.'));
            }
          }
          else if (this.ecValue == "" && res[i].Column == "EC") {
            this.ecValue = parseFloat(res[i].value).toFixed(2);
            if (this.selectedAnalytic != "Average") {
              this.ecTime = res[i].DATE;
              this.ecTime = this.ecTime.replace('T', ' ');
              this.ecTime = '|' + this.ecTime.substring(0, this.ecTime.lastIndexOf('.'));
            }
          }
          else if (this.phValue == "" && res[i].Column == "Ph") {
            this.phValue = parseFloat(res[i].value).toFixed(2);
            if (this.selectedAnalytic != "Average") {
              this.phTime = res[i].DATE;
              this.phTime = this.phTime.replace('T', ' ');
              this.phTime = '|' + this.phTime.substring(0, this.phTime.lastIndexOf('.'));
            }
          }
        }
      });
  }
}
