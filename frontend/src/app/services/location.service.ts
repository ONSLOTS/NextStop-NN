import { Injectable } from '@angular/core';
import streets from '../../assets/data/streets_nnov.json'
import Fuse from 'fuse.js';

@Injectable({
    providedIn: 'root'
})
export class LocationService {
    selectedStreet = '';
    fuse: Fuse<string>;

    constructor() { 
        this.fuse = new Fuse(streets, {
            threshold: 0.7
        });
    }

    getSuggestions(userInput: string) {
        if (!userInput || userInput.length < 2 || this.containSelectedStreet(userInput)) {
            return [];
        }
        return this.fuse.search(userInput).slice(0, 5);
    }

    getUserCoords(): Promise<{latitude: number, longitude: number}> {
        return new Promise((resolve) => {
            navigator.geolocation.getCurrentPosition((position) => {
                resolve({latitude: position.coords.latitude, longitude: position.coords.longitude});
            })
        });
    }

    selectSuggestion(suggestion: string) {
        this.selectedStreet = suggestion;
    }

    containSelectedStreet(value: string) {
        return this.selectedStreet && value.includes(this.selectedStreet);
    }
}
