// Check whether the backend is awake (it sleeps after inactivity on the free tier)
import { HEALTH_URL } from './config';

export async function pingHealth() {
    try {
        const response = await fetch(HEALTH_URL);
        return response.ok;
    } catch {
        return false;
    }
}
