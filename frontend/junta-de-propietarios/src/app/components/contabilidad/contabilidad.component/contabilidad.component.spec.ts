import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContabilidadComponent } from './contabilidad.component';

describe('ContabilidadComponent', () => {
  let component: ContabilidadComponent;
  let fixture: ComponentFixture<ContabilidadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ContabilidadComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ContabilidadComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
