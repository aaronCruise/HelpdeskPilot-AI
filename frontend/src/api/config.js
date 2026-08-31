 // Use environment variable for API base URL, falling back to local for development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';


export const CHECKOUTS_URL = `${API_BASE_URL}/checkouts/`;
export const CHECKOUT_URL = `${API_BASE_URL}/checkout/`;
export const CHECKIN_URL = `${API_BASE_URL}/checkin`;
export const DEVICES_URL = `${API_BASE_URL}/devices/`;
export const TICKETS_URL = `${API_BASE_URL}/tickets/`;