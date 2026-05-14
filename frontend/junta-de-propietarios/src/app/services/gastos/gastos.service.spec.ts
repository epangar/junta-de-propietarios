import { TestBed } from '@angular/core/testing';

import { GastosServicePy } from './gastos.service.py';

describe('GastosServicePy', () => {
  let service: GastosServicePy;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GastosServicePy);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
