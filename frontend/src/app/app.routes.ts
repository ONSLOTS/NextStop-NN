import { Routes } from '@angular/router';
import { PreferencesPageComponent } from './pages/preferences-page/preferences-page.component';
import { ItineraryPageComponent } from './pages/itinerary-page/itinerary-page.component';

export const routes: Routes = [
    {path: 'preferences', component: PreferencesPageComponent},
    {path: 'itinerary', component: ItineraryPageComponent},
    {path: '**', redirectTo: '/preferences'}
];
