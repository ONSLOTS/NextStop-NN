import { Component, inject, Input, OnInit } from '@angular/core';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { Itinerary, ItineraryPoint } from '../../interfaces/itinerary';

@Component({
    selector: 'app-map',
    imports: [],
    templateUrl: './map.component.html',
    styleUrl: './map.component.scss'
})
export class MapComponent implements OnInit{
    @Input() itineraryPoints!: ItineraryPoint[];

    sanitazer = inject(DomSanitizer);
    routeLink = 'https://yandex.ru/map-widget/v1/?ll=43.991374%2C56.327106&mode=routes&rtext=56.337586%2C43.963329~56.326908%2C44.006372&rtt=mt&ruri=ymapsbm1%3A%2F%2Forg%3Foid%3D62660933612~&z=13.98'
    safeLink!: SafeUrl;

    ngOnInit(): void {
        this.safeLink = this.sanitazer.bypassSecurityTrustResourceUrl(`https://yandex.ru/map-widget/v1/?ll=43.991374%2C56.327106&mode=routes&rtext=${this.formatCoords(this.itineraryPoints)}&rtt=mt&ruri=ymapsbm1%3A%2F%2Forg%3Foid%3D62660933612~&z=13.98`);
    }

    formatCoords(itineraryPoints: ItineraryPoint[]) {
        let coords = '';
        
        itineraryPoints.forEach((point) => {
            coords += `${point.longitude}%2C${point.latitude}~`;
        });
        
        return coords.slice(0, -1);
    }
}
