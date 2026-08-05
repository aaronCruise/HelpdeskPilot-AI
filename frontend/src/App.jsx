import { useState } from 'react'

function AnalyzeTicketForm() {
    return (
    <>
    <h2> Analyze Ticket </h2>
    <p> This is where you /POST/analyze tickets. </p>
    </>
  );
}

function CreateTicketForm() {
    return (
    <>
    <h2> Create Ticket </h2>
    <p> This is where you /POST tickets. </p>
    </>
  );
}

function TicketTable() {
  return (
    <>
    <h2> Ticket Table </h2>
    <p> This is where you /GET tickets. </p>
    </>
  );
}

function Dashboard() {
  return (
    <>
    <div>
      <TicketTable />
      <CreateTicketForm />
      <AnalyzeTicketForm />
    </div>
    </>
  );
}

export default function App() {
  return (<Dashboard />);
}