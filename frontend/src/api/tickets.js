// Everything related to ticket API requests
import { TICKETS_URL } from './config';

function formatApiError(result, status) {
    if (!result) {
        return `Response status: ${status}`;
    }

    if (result.detail) {
        if (Array.isArray(result.detail)) {
            return result.detail.map(item => {
                if (typeof item === 'string') {
                    return item;
                }
                if (item?.loc && item?.msg) {
                    return `${item.loc.join('.')}: ${item.msg}`;
                }
                return JSON.stringify(item);
            }).join(' | ');
        }

        return result.detail;
    }

    if (Array.isArray(result)) {
        return result.map(item => {
            if (typeof item === 'string') {
                return item;
            }
            if (item?.msg) {
                return item.msg;
            }
            return JSON.stringify(item);
        }).join(' | ');
    }

    if (status === 422) {
        return 'Validation failed. Please check required fields.';
    }

    return result.message || result.error || `Response status: ${status}`;
}

async function fetchJson(url, options = {}) {
    try {
        const response = await fetch(url, options);
        const result = await response.json().catch(() => null);

        if (!response.ok) {
            return { detail: formatApiError(result, response.status) };
        }

        console.log(result);
        return result;
    }
    catch (error) {
        console.error(error.message);
        return { detail: error.message };
    }
}

export async function getTickets() {
    return await fetchJson(TICKETS_URL, { method: "GET" });
}

export async function getTicket(tid) {
    return await fetchJson(`${TICKETS_URL}${tid}`, { method: "GET" });
}

export async function createTicket(requester_name, requester_email, text) {
    return await fetchJson(TICKETS_URL, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            requester_name,
            requester_email,
            text
        })
    });
}

export async function analyzeTicket(tid) {
    return await fetchJson(`${TICKETS_URL}${tid}/analyze`, { method: "POST" });
}
