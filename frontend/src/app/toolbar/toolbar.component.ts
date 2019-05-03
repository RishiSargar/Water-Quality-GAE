import { Component, OnInit, Output, Input, EventEmitter} from '@angular/core';

@Component({
  selector: 'app-toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.css']
})
export class ToolbarComponent implements OnInit {

  @Output() toggleValue = new EventEmitter<String>();
  @Input() hide: boolean;

  constructor() { }

  ngOnInit() {
  }

  toggle(){
    this.toggleValue.emit();
  }

}
