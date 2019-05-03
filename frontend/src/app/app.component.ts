import { Component } from '@angular/core';
import { UserComponent } from './user/user.component'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  
  userComponent: UserComponent;
  isHide: boolean = false;

  toggle(event){
    if(this.userComponent!=null)
      this.userComponent.sidenav.toggle();
  }

  onActivate(componentRef) {
    if(componentRef instanceof UserComponent)
      this.userComponent = (<UserComponent>componentRef);
    else
      this.isHide = true;
    
  }
}
