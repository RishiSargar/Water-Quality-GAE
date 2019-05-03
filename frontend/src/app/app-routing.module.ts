import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UserComponent } from './user/user.component'
import { ResearcherComponent } from './researcher/researcher.component';

const routes: Routes = [
  { path: '', component: UserComponent },
  { path: 'researcher', component: ResearcherComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
