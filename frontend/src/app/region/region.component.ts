import { Component, OnInit, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-region',
  templateUrl: './region.component.html',
  styleUrls: ['./region.component.css']
})
export class RegionComponent implements OnInit {

  regions: Array<String> = ['Bio Design Building Break Room 1', 'Bio Design Building Break Room 2', 'Bio Design Building Break Room 3'];

  @Output() selectedRegion = new EventEmitter<string>();

  constructor() { }

  ngOnInit() {
  }

  changeRegion(region) {
    this.selectedRegion.emit(region);
  }
}
