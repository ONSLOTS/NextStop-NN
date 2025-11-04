export interface Itinerary {
    walking_time: number,
    walking_path: ItineraryPoint[],
    explanation: string[]
}

export interface ItineraryPoint {
    id: number,
    title: string,
    description: string,
    score: number,
    latitude: number,
    longitude: number,
}