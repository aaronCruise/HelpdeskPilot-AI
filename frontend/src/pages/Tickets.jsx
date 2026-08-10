import { useState, useEffect } from 'react';
import '../api/tickets.js';
import { getTickets, getTicket, createTicket, analyzeTicket } from '../api/tickets.js';

const TICKET_TABLE_NUM_COLUMNS = 7;

function AnalyzeTicketForm() {
    return (
        <>
            <h2> Analyze Ticket </h2>
            <form>
                <div>
                    <label htmlFor="ticket_id"> Enter ticket ID: </label>
                    <input type="number" name="ticket_id" id="ticket-id" required />
                </div>
                <div>
                    <input type="submit" value="Submit" />
                </div>
            </form>
            <h3> Recommendation: </h3>
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

    tickets.Array

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
    async function refreshTickets() {
        const result = await getTickets();
        const tickets = result["tickets"];
        setTickets(tickets || []);
        console.log("Tickets loaded:", tickets);
    }
    useEffect(
        () => {
            refreshTickets();
        }, []);

    return (
        <>
            <div>
                <TicketTable tickets={tickets} />
                <CreateTicketForm onTicketCreated={refreshTickets} />
                <AnalyzeTicketForm />
            </div>
        </>
    );
}