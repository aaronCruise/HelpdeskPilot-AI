// Everything related to ticket API requests

const BACKEND_URL = 'https://special-fortnight-g47q6jr9gvjw2p9pr-8000.app.github.dev/tickets/'; //TODO: Change 

async function fetchJson(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const result = await response.json();
        console.log(result);
        return result;
    }
    catch (error) {
        console.error(error.message);
        return [];
    }
}

export async function getTickets() {
    return await fetchJson(BACKEND_URL, { method: "GET" });
}

export async function getTicket(tid) {
    return await fetchJson(`${BACKEND_URL}${tid}`, { method: "GET" });
}

export async function createTicket(requester_name, requester_email, text) {
    return await fetchJson(BACKEND_URL, {
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
    return await fetchJson(`${BACKEND_URL}${tid}/analyze`, { method: "POST" });
}
