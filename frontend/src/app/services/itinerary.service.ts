import { inject, Injectable, signal } from '@angular/core';
import { Itinerary } from '../interfaces/itinerary';
import { ItineraryPreferences } from '../interfaces/itinerary-preferences.interface';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class ItineraryService {
    http = inject(HttpClient);
    currentItinerary!: Itinerary;

    constructor() { }

    generateItinerary(itineraryPreferences: ItineraryPreferences) {
        return this.http.post<Itinerary>('api/generate_route', itineraryPreferences).pipe(
            tap(itinerary => this.currentItinerary = itinerary)
        );
    }

    getItinerary() {
        return this.currentItinerary;
    }
}
