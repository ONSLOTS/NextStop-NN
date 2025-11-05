import { Component, inject } from '@angular/core';
import { ItineraryService } from '../../services/itinerary.service';
import { MapComponent } from "../../components/map/map.component";

@Component({
    selector: 'app-itinerary-page',
    imports: [MapComponent, MapComponent],
    templateUrl: './itinerary-page.component.html',
    styleUrl: './itinerary-page.component.scss'
})
export class ItineraryPageComponent {
    itineraryService = inject(ItineraryService);

    itinerary = this.itineraryService.currentItinerary;
}
