// Everything related to checkout API requests
import { CHECKOUTS_URL, CHECKOUT_URL, CHECKIN_URL } from './config';

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

export async function getCheckouts() {
    return await fetchJson(CHECKOUTS_URL, { method: "GET" });
}

export async function getActiveCheckouts() {
    return await fetchJson(`${CHECKOUTS_URL}active`, { method: "GET" });
}

export async function getCheckout(cid) {
    return await fetchJson(`${CHECKOUTS_URL}${cid}`, { method: "GET" });
}

export async function createCheckout(device_id, borrower_name, borrower_email, from_date, to_date) {
    return await fetchJson(CHECKOUTS_URL, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            device_id,
            borrower_name,
            borrower_email,
            from_date,
            to_date
        })
    });
}

export async function patchCheckout(cid, to_date, status) {
    return await fetchJson(`${CHECKOUT_URL}${cid}`, {
        method: "PATCH",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            to_date,
            status
        })
    });
}

export async function checkIn(cid, status) {
    return await fetchJson(CHECKIN_URL, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cid,
            status
        })
    });
}
