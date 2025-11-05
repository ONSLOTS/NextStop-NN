import { Component, ElementRef, inject, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { debounceTime, distinctUntilChanged, Subscription } from 'rxjs';
import { LocationService } from '../../services/location.service';
import { FuseResult } from 'fuse.js';
import { ItineraryPreferences } from '../../interfaces/itinerary-preferences.interface';
import { ItineraryService } from '../../services/itinerary.service';
import { Router } from "@angular/router";

@Component({
    selector: 'app-preferences-page',
    imports: [ReactiveFormsModule],
    templateUrl: './preferences-page.component.html',
    styleUrl: './preferences-page.component.scss'
})
export class PreferencesPageComponent implements OnInit, OnDestroy {
    @ViewChild('locationInput') locationRef!: ElementRef<HTMLInputElement>;

    locationService = inject(LocationService);
    itineraryService = inject(ItineraryService);
    router = inject(Router);

    itineraryPreferences = new FormGroup({
        prompt: new FormControl('', Validators.required),
        time_for_walk: new FormControl('', Validators.required),
        address: new FormControl('', Validators.required),
    });

    locationControl = this.itineraryPreferences.get('address');
    inputSubscription?: Subscription;
    suggestions?: FuseResult<string>[];
    userLocation: { latitude: number, longitude: number } | null = null;

    ngOnInit(): void {
        this.inputSubscription = this.locationControl?.valueChanges.pipe(
            debounceTime(300),
            distinctUntilChanged()
        ).subscribe(userInput => {
            this.suggestions = this.locationService.getSuggestions(userInput || '');
        });
    }

    selectSuggestion(suggestion: string) {
        this.locationService.selectSuggestion(suggestion);
        this.locationControl?.setValue(suggestion);
        this.locationRef.nativeElement.focus();
        this.suggestions = [];
    }

    onSubmit() {
        if (this.itineraryPreferences.valid) {
            this.itineraryService.generateItinerary(this.createRequestData(this.itineraryPreferences.value));
            this.router.navigate(['/itinerary']);
        }
    }

    async getLocation() {
        if ('geolocation' in navigator) {
            this.userLocation = await this.locationService.getUserCoords();
            this.locationControl?.setValue(`Широта: ${this.userLocation.latitude}, Долгота: ${this.userLocation.longitude}`);
        }
    }

    createRequestData(formValue: any): ItineraryPreferences {
        if (this.userLocation) {
            return {
                prompt: formValue.prompt,
                time_for_walk: formValue.time_for_walk,
                address: "",
                latitude: this.userLocation.latitude,
                longitude: this.userLocation.longitude,
            }
        }
        else {
            return {
                prompt: formValue.prompt,
                time_for_walk: formValue.time_for_walk,
                address: formValue.location,
            }
        }
    }

    ngOnDestroy(): void {
        this.inputSubscription?.unsubscribe();
    }
}
