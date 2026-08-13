import { useState, useEffect } from 'react';
import { getTickets, getTicket, createTicket, analyzeTicket, patchTicket } from '../api/tickets.js';
import './Tickets.css';

const TICKET_TABLE_NUM_COLUMNS = 8;
const TICKET_STATUSES = ['new', 'in_progress', 'resolved', 'closed'];
const TICKET_PRIORITIES = ['low', 'medium', 'high'];

function RecommendationCard({ localError, error, ticket }) {
    return (
        <div className="recommendation-card">
            <h3> Recommendation: </h3>
            {(localError || error) && <p className="error-message">{localError || error}</p>}
            {ticket && (
                <div>
                    <p><strong>Category:</strong> {ticket.category}</p>
                    <p><strong>Priority:</strong> {ticket.priority}</p>
                    <p><strong>Summary:</strong> {ticket.summary}</p>
                    <p><strong>Recommended Step:</strong> {ticket.recommended_step}</p>
                </div>
            )}
        </div>
    );

}

function AnalyzeTicketForm({ onAnalyze, result, error }) {
    const [localError, setLocalError] = useState('');

    async function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const ticket_id = formData.get('ticket_id');

        if (!ticket_id) {
            setLocalError('Ticket ID is required.');
            return;
        }

        setLocalError('');
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
            <RecommendationCard localError={localError} error={error} ticket={result} />
        </>
    );
}

function TicketByIdForm({ onFetch, ticket, error }) {
    const [localError, setLocalError] = useState('');

    async function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const ticket_id = formData.get('ticket_id');

        if (!ticket_id) {
            setLocalError('Ticket ID is required.');
            return;
        }

        setLocalError('');
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

        </>
    );
}

function UpdateTicketForm({ onUpdate, result, error }) {
    const [localError, setLocalError] = useState('');

    async function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const ticket_id = Number(formData.get('ticket_id'));
        const status = formData.get('status');
        const priority = formData.get('priority');

        if (!ticket_id || !status || !priority) {
            setLocalError('Please fill in all required fields.');
            return;
        }

        setLocalError('');
        await onUpdate(ticket_id, status, priority);
    }

    return (
        <>
            <h2> Update Ticket </h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="ticket_id"> Ticket ID: </label>
                    <input type="number" name="ticket_id" id="ticket_id" required />
                </div>
                <div>
                    <label htmlFor="status"> New status: </label>
                    <select name="status" id="status" required>
                        <option value="">Select status</option>
                        {TICKET_STATUSES.map(statusOption => (
                            <option key={statusOption} value={statusOption}>{statusOption}</option>
                        ))}
                    </select>
                </div>
                <div>
                    <label htmlFor="priority"> New priority: </label>
                    <select name="priority" id="priority" required>
                        <option value="">Select priority</option>
                        {TICKET_PRIORITIES.map(priorityOption => (
                            <option key={priorityOption} value={priorityOption}>{priorityOption}</option>
                        ))}
                    </select>
                </div>
                <div>
                    <input type="submit" value="Submit" />
                </div>
            </form>
            {(localError || error) && <p className="error-message">{localError || error}</p>}
            {result && !error && (
                <div>
                    <p><strong>Updated Ticket ID:</strong> {result.tid}</p>
                    <p><strong>Status:</strong> {result.status}</p>
                    <p><strong>Priority:</strong> {result.priority}</p>
                </div>
            )}
        </>
    );
}

function CreateTicketForm({ onTicketCreated }) {
    const [createError, setCreateError] = useState('');

    async function handleSubmit(event) {
        event.preventDefault();
        const form = event.target;
        const formDate = new FormData(form);
        const name = formDate.get("name");
        const email = formDate.get("email");
        const ticket_text = formDate.get("ticket_text");

        if (!name || !email || !ticket_text) {
            setCreateError('Please fill in all required fields.');
            return;
        }

        setCreateError('');
        const result = await createTicket(name, email, ticket_text);
        if (result?.detail) {
            setCreateError(result.detail);
            return;
        }

        setCreateError('');
        await onTicketCreated();
        form.reset();
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
                    <textarea name="ticket_text" id="ticket_text" cols="50" rows="10" required></textarea>
                </div>
                {createError && <p className="error-message">{createError}</p>}
                <div>
                    <input type="submit" value="Submit" />
                </div>
            </form>
        </>
    );
}

function StatusRow({ status }) {
    return (
        <tr className="status-row">
            <th colSpan={TICKET_TABLE_NUM_COLUMNS}>
                {status}
            </th>
        </tr>
    );
}

function TicketRow({ ticket }) {
    return (
        <tr>
            <td>{ticket.tid}</td>
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
                        <th>ID</th>
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
    const [updateResult, setUpdateResult] = useState(null);
    const [updateError, setUpdateError] = useState('');

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
        if (!result || result.detail || Array.isArray(result)) {
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

    async function handleUpdateTicket(tid, status, priority) {
        setUpdateError('');
        setUpdateResult(null);

        const result = await patchTicket(tid, status, priority);
        if (!result || result.detail || Array.isArray(result)) {
            setUpdateError(result?.detail || 'Unable to update ticket.');
            return;
        }

        setUpdateResult(result);
        await refreshTickets();
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
                <UpdateTicketForm onUpdate={handleUpdateTicket} result={updateResult} error={updateError} />
                <TicketByIdForm onFetch={handleFetchTicket} ticket={selectedTicket} error={ticketError} />
            </div>
        </>
    );
}