// Everything related to ticket API requests

const BACKEND_URL = 'https://special-fortnight-g47q6jr9gvjw2p9pr-8000.app.github.dev/tickets/'; //TODO: Change 

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


//TODO
export function getTicket(tid) {

}

export async function createTicket(requester_name, requester_email, text) {
    try {
        const response = await fetch(BACKEND_URL, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                requester_name: requester_name,
                requester_email: requester_email,
                text: text
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

//TODO
export function analyzeTicket(tid) {

}