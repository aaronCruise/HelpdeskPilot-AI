// Everything related to device API requests
const BACKEND_URL = 'http://127.0.0.1:8000/devices/';

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

export async function getDevices() {
    return await fetchJson(BACKEND_URL, { method: "GET" });
}

export async function getDevice(did) {
    return await fetchJson(`${BACKEND_URL}${did}`, { method: "GET" });
}

export async function createDevice(asset_tag, name, type) {
    return await fetchJson(BACKEND_URL, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            asset_tag,
            name,
            type
        })
    });
}

export async function patchDevice(did, state) {
    return await fetchJson(`${BACKEND_URL}${did}`, {
        method: "PATCH",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            state
        })
    });
}
