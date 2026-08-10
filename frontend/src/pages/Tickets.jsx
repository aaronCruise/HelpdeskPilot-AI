import { useState, useEffect } from 'react';
import { getTickets, getTicket, createTicket, analyzeTicket } from '../api/tickets.js';

const TICKET_TABLE_NUM_COLUMNS = 7;

function AnalyzeTicketForm({ onAnalyze, result, error }) {
    async function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const ticket_id = formData.get('ticket_id');

        if (!ticket_id) {
            return;
        }

        await onAnalyze(Number(ticket_id));
    }

    return (
        <>
            <h2> Analyze Ticket </h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="ticket_id"> Enter ticket ID: </label>
                    <input type="number" name="ticket_id" id="ticket-id" required />
                </div>
                <div>
                    <input type="submit" value="Submit" />
                </div>
            </form>
            <h3> Recommendation: </h3>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {result && (
                <div>
                    <p><strong>Category:</strong> {result.category}</p>
                    <p><strong>Priority:</strong> {result.priority}</p>
                    <p><strong>Summary:</strong> {result.summary}</p>
                    <p><strong>Recommended step:</strong> {result.recommended_step}</p>
                </div>
            )}
        </>
    );
}

function TicketByIdForm({ onFetch, ticket, error }) {
    async function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const ticket_id = formData.get('ticket_id');

        if (!ticket_id) {
            return;
        }

        await onFetch(Number(ticket_id));
    }

    return (
        <>
            <h2> Get Ticket by ID </h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="ticket_id"> Enter ticket ID: </label>
                    <input type="number" name="ticket_id" id="ticket-id" required />
                </div>
                <div>
                    <input type="submit" value="Submit" />
                </div>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {ticket && (
                <div>
                    <p><strong>ID:</strong> {ticket.tid}</p>
                    <p><strong>Name:</strong> {ticket.requester_name}</p>
                    <p><strong>Email:</strong> {ticket.requester_email}</p>
                    <p><strong>Text:</strong> {ticket.text}</p>
                    <p><strong>Category:</strong> {ticket.category}</p>
                    <p><strong>Priority:</strong> {ticket.priority}</p>
                    <p><strong>Status:</strong> {ticket.status}</p>
                    <p><strong>Created:</strong> {ticket.created_at}</p>
                </div>
            )}
        </>
    );
}

function CreateTicketForm({onTicketCreated}) {
    async function handleSubmit(event) {
        event.preventDefault();
        const form = event.target;
        const formDate = new FormData(form);
        const name = formDate.get("name");
        const email = formDate.get("email");
        const ticket_text = formDate.get("ticket_text");

        console.log(`Creating ticket for ${name} (${email}): ${ticket_text}`);
        const result = await createTicket(name, email, ticket_text);
        console.log("Ticket created:", result['ticket']);
        await onTicketCreated();
    }


    return (
        <>
            <h2> Create Ticket </h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="name"> Enter your name: </label>
                    <input type="text" name="name" id="name" required />
                </div>
                <div>
                    <label htmlFor="email"> Enter your email: </label>
                    <input type="email" name="email" id="email" required />
                </div>
                <div>
                    <label htmlFor="ticket_text"> Please describe your ticket: </label> <br />
                    <textarea name="ticket_text" id="ticket_text" cols="50" rows="10"></textarea>
                </div>
                <div>
                    <input type="submit" value="Submit" />
                </div>
            </form>
        </>
    );
}

function StatusRow({ status }) {
    return (
        <tr>
            <th colSpan={TICKET_TABLE_NUM_COLUMNS}>
                {status}
            </th>
        </tr>
    );
}

function TicketRow({ ticket }) {
    return (
        <tr>
            <td>{ticket.requester_name}</td>
            <td>{ticket.requester_email}</td>
            <td>{ticket.text}</td>
            <td>{ticket.category}</td>
            <td>{ticket.priority}</td>
            <td>{ticket.status}</td>
            <td>{ticket.created_at}</td>
        </tr>
    );
}

function TicketTable({ tickets }) {
    const newRows = [];
    const inProgressRows = [];
    const resolvedRows = [];
    const closedRows = [];
    const safeTickets = Array.isArray(tickets) ? tickets : [];

    safeTickets.forEach(ticket => {
        switch (ticket.status) {
            case 'new':
                newRows.push(<TicketRow key={ticket.tid} ticket={ticket} />);
                break;
            case 'in_progress':
                inProgressRows.push(<TicketRow key={ticket.tid} ticket={ticket} />);
                break;
            case 'resolved':
                resolvedRows.push(<TicketRow key={ticket.tid} ticket={ticket} />);
                break;
            case 'closed':
                closedRows.push(<TicketRow key={ticket.tid} ticket={ticket} />);
                break;
        }
    })

    return (
        <>
            <h2> Ticket Table </h2>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Text</th>
                        <th>Category</th>
                        <th>Priority</th>
                        <th>Status</th>
                        <th>Created</th>
                    </tr>
                </thead>
                <tbody>
                    <StatusRow key="new" status={'new'} />
                    {newRows}
                    <StatusRow key="in_progress" status={'in_progress'} />
                    {inProgressRows}
                    <StatusRow key="resolved" status={'resolved'} />
                    {resolvedRows}
                    <StatusRow key="closed" status={'closed'} />
                    {closedRows}
                </tbody>
            </table>
        </>
    );
}

export function TicketDashboard() {
    const [tickets, setTickets] = useState([]);
    const [recommendation, setRecommendation] = useState(null);
    const [analyzeError, setAnalyzeError] = useState('');
    const [selectedTicket, setSelectedTicket] = useState(null);
    const [ticketError, setTicketError] = useState('');

    async function refreshTickets() {
        const result = await getTickets();
        const tickets = result?.tickets;
        setTickets(tickets || []);
        console.log('Tickets loaded:', tickets);
    }

    async function handleAnalyzeTicket(tid) {
        setAnalyzeError('');
        setRecommendation(null);

        const result = await analyzeTicket(tid);
        if (!result || result.detail) {
            setAnalyzeError(result?.detail || 'Unable to analyze ticket.');
            return;
        }

        setRecommendation(result);
    }

    async function handleFetchTicket(tid) {
        setTicketError('');
        setSelectedTicket(null);

        const result = await getTicket(tid);
        if (!result || result.detail || Array.isArray(result)) {
            setTicketError(result?.detail || 'Unable to fetch ticket.');
            return;
        }

        setSelectedTicket(result);
    }

    useEffect(() => {
        refreshTickets();
    }, []);

    return (
        <>
            <div>
                <TicketTable tickets={tickets} />
                <CreateTicketForm onTicketCreated={refreshTickets} />
                <AnalyzeTicketForm onAnalyze={handleAnalyzeTicket} result={recommendation} error={analyzeError} />
                <TicketByIdForm onFetch={handleFetchTicket} ticket={selectedTicket} error={ticketError} />
            </div>
        </>
    );
}