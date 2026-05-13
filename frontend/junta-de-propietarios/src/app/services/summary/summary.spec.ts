import { TestBed } from '@angular/core/testing';
import  {SummaryService} from './summary.service';
import { environment } from '../../../environments/environment';

describe('Summary', () => {
  let service: SummaryService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SummaryService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
