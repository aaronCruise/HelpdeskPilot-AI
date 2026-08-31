// Check whether the backend is awake (it sleeps after inactivity on the free tier)
import { HEALTH_URL } from './config';

const HEALTH_CHECK_TIMEOUT_MS = 10000;

export async function pingHealth() {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), HEALTH_CHECK_TIMEOUT_MS);
    try {
        const response = await fetch(HEALTH_URL, { signal: controller.signal });
        return response.ok;
    } catch {
        return false;
    } finally {
        clearTimeout(timeoutId);
    }
}
