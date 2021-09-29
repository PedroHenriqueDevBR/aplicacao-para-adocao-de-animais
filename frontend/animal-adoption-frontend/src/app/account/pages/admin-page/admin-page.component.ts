import { Component, OnInit } from '@angular/core';
import { PersonModel } from 'src/app/shared/models/person-model';

@Component({
  templateUrl: './admin-page.component.html',
  styleUrls: ['./admin-page.component.less']
})
export class AdminPageComponent implements OnInit {
  persons: PersonModel[] = [];
  selectedPerson?: PersonModel;

  constructor() { }

  ngOnInit(): void {
    this.getPersons();
  }

  getPersons(): void {
    for (let i = 0; i < 10; i++) {
      const person = new PersonModel();
      person.id = i+1;
      person.name = `Person 0${i+1}`;
      person.contact = '(86) 91234-5678';
      person.image = 'https://images.pexels.com/photos/3569409/pexels-photo-3569409.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940';
      this.persons.push(person);
    }
  }
  
  profileImage() : string {
    if (this.selectedPerson == null) {
      return '/assets/images/avatar.png';
    } else if (this.selectedPerson.image == null || this.selectedPerson.image == '') {
      return '/assets/images/avatar.png';
    }
    return this.selectedPerson.image;
  }

  selectPerson(person: PersonModel) {
    this.selectedPerson = person;
  }

  changeBlockPerson() {
    if (this.selectedPerson != null) {
      this.selectedPerson.isActive = !this.selectedPerson.isActive;
    }
  }

  changeModeratorPerson() {
    if (this.selectedPerson != null) {
      this.selectedPerson.isModerator = !this.selectedPerson.isModerator;
    }
  }

}
