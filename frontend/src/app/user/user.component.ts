import { Component, OnInit, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
import { AppService } from '../app.service';

declare var System: any;

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {

  selectedRegion: string;
  selectedTimeSlab: string;
  timeSlabText: string;
  timeStampText: string;
  currentTimeStamp: string;
  currentEC: string;
  currentTemperature: string;
  currentpH: string;
  recommended: string;
  timeslabs: Array<String> = ['Current Hour', 'Hourly', 'Daily', 'Weekly'];

  @ViewChild('sidenav') sidenav: MatSidenav;

  constructor(private appService: AppService) { }

  ngOnInit() {
    this.selectedRegion = "Bio Design Building Break Room 1";
    this.selectedTimeSlab = "Current Hour";
    this.drawGraphs(this.selectedRegion, this.selectedTimeSlab);
  }

  drawGraphs(region, timeslab) {

    this.appService.getData(region, 'Current Hour').subscribe((res: any) => {
      debugger;
      this.currentEC = res[0].ec;
      this.currentTemperature = res[0].temperature;
      this.currentpH = res[0].ph;

      if (parseFloat(this.currentEC) < 2500 && parseFloat(this.currentpH) < 8.5) {
        this.recommended = "Drinkable";
      }
      else {
        this.recommended = "Not recommended";
      }

      this.currentEC = parseFloat(this.currentEC).toFixed(2);
      this.currentTemperature = parseFloat(this.currentTemperature).toFixed(2);
    });

    this.appService.getData(region, timeslab).subscribe((res: any) => {
      let ecValues = [];
      let tempValues = [];
      let timeStamps = [];

      for (let i = 0; i < res.length; i++) {
        if (this.selectedTimeSlab != 'Current Hour') {
          ecValues.push(parseFloat(parseFloat(res[i].Average_ec).toFixed(2)));
          tempValues.push(parseFloat(parseFloat(res[i].Average_temp).toFixed(2)));
          timeStamps.push(this.formatXAxis(res[i].hour_number, this.selectedTimeSlab));
        }
        else {
          ecValues.push(parseFloat(parseFloat(res[i].ec).toFixed(2)));
          tempValues.push(parseFloat(parseFloat(res[i].temperature).toFixed(2)));
          timeStamps.push(this.formatXAxis(res[i].timestamp, this.selectedTimeSlab));
        }
      }

      this.currentTimeStamp = this.formatTimeStamp();

      ecValues.reverse();
      tempValues.reverse();
      timeStamps.reverse();

      this.timeStampText = "";
      if (this.selectedTimeSlab == 'Current Hour') {
        this.timeStampText = timeStamps[0] + ' - ' + timeStamps[timeStamps.length - 1];
        this.timeSlabText = "";
      } else {
        this.changeTimeSlabDesc();
      }

      System.import('./ec.js').then(js => {
        js.draw(ecValues, timeStamps);
      });

      System.import('./temp.js').then(js => {
        js.draw(tempValues, timeStamps);
      });

      System.import('./ph.js').then(js => {
        this.currentpH = parseFloat(this.currentpH).toFixed(2);
        js.draw(parseFloat(this.currentpH));
      });

      System.import('./standard.js').then(js => {
        js.draw(parseFloat(this.currentEC), parseFloat(this.currentpH), parseFloat(this.currentTemperature));
      });
    });
  }

  changeRegion(region) {
    this.selectedRegion = region;
    this.drawGraphs(this.selectedRegion, this.selectedTimeSlab);
  }

  changeTimeSlab() {
    this.drawGraphs(this.selectedRegion, this.selectedTimeSlab);
  }

  changeTimeSlabDesc() {
    this.timeStampText = "";
    if (this.selectedTimeSlab == 'Weekly') {
      this.timeSlabText = "last 8 weeks";
    } else if (this.selectedTimeSlab == 'Hourly') {
      this.timeSlabText = "last 24 Hours";
    } else if (this.selectedTimeSlab == "Daily") {
      this.timeSlabText = "last 7 days";
    }
  }

  formatXAxis(timeStamp: string, timeSlab: string) {
    if (timeSlab == 'Current Hour') {
      return timeStamp.substring(10, 15)
    }
    else if (timeSlab == 'Hourly') {
      return timeStamp.substring(3, timeStamp.length - 7);
    }
    else {
      return timeStamp.substring(3, timeStamp.length - 13);
    }
  }

  formatTimeStamp() {

    let hoursStr: string;
    let minutesStr: string;
    let secStr: string;

    let today = new Date();
    let date = today.getFullYear() + '/' + (today.getMonth() + 1) + '/' + today.getDate();

    let hours = today.getHours();
    if (hours < 9) hoursStr = '0' + hours;
    else hoursStr = hours.toString();

    let minutes = today.getMinutes();
    if (minutes < 9) minutesStr = '0' + minutes;
    else minutesStr = minutes.toString();

    let seconds = today.getSeconds();
    if (seconds < 9) secStr = '0' + seconds;
    else secStr = seconds.toString();

    let time = hoursStr + ":" + minutesStr + ":" + secStr;
    let dateTime = date + ' ' + time;

    return dateTime;
  }
}
