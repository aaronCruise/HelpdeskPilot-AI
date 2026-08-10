import { useState, useEffect } from 'react';
import '../api/tickets.js';
import { getTickets } from '../api/tickets.js';

const TICKET_TABLE_NUM_COLUMNS = 7;

function AnalyzeTicketForm() {
    return (
        <>
            <h2> Analyze Ticket </h2>
            <form>
                <div>
                    <label for="ticket_id"> Enter ticket ID: </label>
                    <input type="number" name="ticket_id" id="ticket-id" required />
                </div>
                <div>
                    <input for="ticket_id" type="submit" value="Submit" />
                </div>
            </form>
            <h3> Recommendation: </h3>
        </>
    );
}

function CreateTicketForm({onTicketCreated}) {
    function handleSubmit(event) {
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
                    <label for="name"> Enter your name: </label>
                    <input type="text" name="name" id="name" required />
                </div>
                <div>
                    <label for="email"> Enter your email: </label>
                    <input type="email" name="email" id="email" required />
                </div>
                <div>
                    <label for="ticket_text"> Please describe your ticket: </label> <br />
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
                newRows.push(<TicketRow key={ticket.id} ticket={ticket} />);
                break;
            case 'in_progress':
                inProgressRows.push(<TicketRow key={ticket.id} ticket={ticket} />);
                break;
            case 'resolved':
                resolvedRows.push(<TicketRow key={ticket.id} ticket={ticket} />);
                break;
            case 'closed':
                closedRows.push(<TicketRow key={ticket.id} ticket={ticket} />);
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
                    <StatusRow key={'new'} status={'new'} />
                    {newRows}
                    <StatusRow key={'in_progress'} status={'in_progress'} />
                    {inProgressRows}
                    <StatusRow key={'resolved'} status={'resolved'} />
                    {resolvedRows}
                    <StatusRow key={'closed'} status={'closed'} />
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

// For testing purposes
const static_tickets = [
    {
        id: 1,
        requesterName: "Sarah Johnson",
        requesterEmail: "sjohnson@rutgers.edu",
        category: "classroom_tech",
        priority: "high",
        status: "new",
        text: "Projector in Room 204 is not detecting HDMI input from instructor laptop.",
        createdAt: "2026-08-05"
    },
    {
        id: 2,
        requesterName: "Michael Chen",
        requesterEmail: "mchen@rutgers.edu",
        category: "account_access",
        priority: "medium",
        status: "in_progress",
        text: "Unable to log into Rutgers email after password reset.",
        createdAt: "2026-08-05"
    },
    {
        id: 3,
        requesterName: "Emily Rodriguez",
        requesterEmail: "erodriguez@rutgers.edu",
        category: "checkout",
        priority: "low",
        status: "resolved",
        text: "Requesting a DSLR camera and tripod for a student media project.",
        createdAt: "2026-08-04"
    },
    {
        id: 4,
        requesterName: "James Patel",
        requesterEmail: "jpatel@rutgers.edu",
        category: "network",
        priority: "high",
        status: "new",
        text: "Faculty desktop repeatedly disconnects from campus network.",
        createdAt: "2026-08-04"
    },
    {
        id: 5,
        requesterName: "Olivia Thompson",
        requesterEmail: "othompson@rutgers.edu",
        category: "hardware",
        priority: "medium",
        status: "closed",
        text: "Office printer displays paper jam error despite no obstruction.",
        createdAt: "2026-08-03"
    },
    {
        id: 6,
        requesterName: "Daniel Kim",
        requesterEmail: "dkim@rutgers.edu",
        category: "classroom_tech",
        priority: "high",
        status: "in_progress",
        text: "Classroom audio system produces static during presentations.",
        createdAt: "2026-08-03"
    },
    {
        id: 7,
        requesterName: "Ava Martinez",
        requesterEmail: "amartinez@rutgers.edu",
        category: "software",
        priority: "low",
        status: "new",
        text: "Adobe Creative Cloud fails to launch after workstation update.",
        createdAt: "2026-08-02"
    },
    {
        id: 8,
        requesterName: "Ethan Walker",
        requesterEmail: "ewalker@rutgers.edu",
        category: "account_access",
        priority: "medium",
        status: "resolved",
        text: "Multi-factor authentication code never arrives on mobile device.",
        createdAt: "2026-08-02"
    },
    {
        id: 9,
        requesterName: "Sophia Lee",
        requesterEmail: "slee@rutgers.edu",
        category: "checkout",
        priority: "high",
        status: "new",
        text: "Need two laptops and a webcam kit for tomorrow's guest lecture.",
        createdAt: "2026-08-01"
    },
    {
        id: 10,
        requesterName: "Noah Garcia",
        requesterEmail: "ngarcia@rutgers.edu",
        category: "network",
        priority: "medium",
        status: "closed",
        text: "Wi-Fi connectivity drops every few minutes in office suite.",
        createdAt: "2026-08-01"
    }
];