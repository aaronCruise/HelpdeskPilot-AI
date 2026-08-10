// Everything related to ticket API requests

const BACKEND_URL = 'https://musical-potato-r4pgwq69jj55fvx5-8000.app.github.dev/tickets/';

export async function getTickets() {

    try {
        const response = await fetch(BACKEND_URL, {method: "GET"});
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

function getTicket(tid) {

}

export async function createTicket(name, email, ticket_text) {
    try {
        const response = await fetch(BACKEND_URL, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                email: email,
                ticket_text: ticket_text
            })
        });
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

function analyzeTicket(tid) {

}