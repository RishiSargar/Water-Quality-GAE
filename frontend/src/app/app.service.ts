import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class AppService {

    constructor(private http: HttpClient) {
    }

    regionsDict: any = {
        "Bio Design Building Break Room 1": "controller1",
        "Bio Design Building Break Room 2": "controller2",
        "Bio Design Building Break Room 3": "controller3"
    }

    timeSlabsDict: any = {
        "Current Hour": "data",
        "Hourly": "hourly",
        "Daily": "daily",
        "Weekly": "weekly"
    }

    analytics: any = {
        "Max": "max",
        "Min": "min",
        "Average": "avg"
    }

    getData(region, timeslab) {
        let url = 'https://asu-dot-ninth-tensor-233119.appspot.com/pubsub/' +
            this.timeSlabsDict[timeslab] + '?controller_id=' + this.regionsDict[region];
        return this.http.get(url);
    }

    getDataInRange(region, from, to) {
        debugger;
        let url = 'https://asu-dot-ninth-tensor-233119.appspot.com/pubsub/timestamp?controller_id='
            + this.regionsDict[region] + '&&t1=' + from + '&&t2=' + to;
        return this.http.get(url);
    }

    getAnalytics(region, from, to, analytic) {
        let url = 'https://asu-dot-ninth-tensor-233119.appspot.com/pubsub/timestamp_'
            + this.analytics[analytic] + '?controller_id=' + this.regionsDict[region] + '&&t1='
            + from + '&&t2=' + to;

        return this.http.get(url);
    }
}