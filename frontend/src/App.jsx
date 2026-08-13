import { useState, useEffect } from 'react';
import { getTickets } from './api/tickets.js';
import { getDevices } from './api/devices.js';
import { getActiveCheckouts } from './api/checkouts.js';
import { TicketDashboard } from './pages/Tickets.jsx';
import { DeviceDashboard } from './pages/Devices.jsx';
import { CheckoutDashboard } from './pages/Checkouts.jsx';
import './App.css';

function Dashboard() {
  const [openTickets, setOpenTickets] = useState(0);
  const [availableDevices, setAvailableDevices] = useState(0);
  const [activeCheckouts, setActiveCheckouts] = useState(0);

  useEffect(() => {
    async function refreshCounts() {
      const ticketResult = await getTickets();
      const deviceResult = await getDevices();
      const activeResult = await getActiveCheckouts();

      const tickets = Array.isArray(ticketResult?.tickets) ? ticketResult.tickets : [];
      const devices = Array.isArray(deviceResult?.devices) ? deviceResult.devices : [];
      const checkouts = Array.isArray(activeResult?.checkouts) ? activeResult.checkouts : [];

      setOpenTickets(tickets.filter(ticket => ticket.status !== 'resolved' && ticket.status !== 'closed').length);
      setAvailableDevices(devices.filter(device => device.state === 'available').length);
      setActiveCheckouts(checkouts.length);
    }

    refreshCounts();
  }, []);

  return (
    <>
      <h1>Dashboard Overview</h1>
      <div className="dashboard-grid">
        <div className="stat-card">
          <h2>Open Tickets</h2>
          <p className="stat-value">{openTickets}</p>
        </div>
        <div className="stat-card">
          <h2>Available Devices</h2>
          <p className="stat-value">{availableDevices}</p>
        </div>
        <div className="stat-card">
          <h2>Active Checkouts</h2>
          <p className="stat-value">{activeCheckouts}</p>
        </div>
      </div>
    </>
  );
}

const DASHBOARDS = {
  dashboard: Dashboard,
  tickets: TicketDashboard,
  devices: DeviceDashboard,
  checkouts: CheckoutDashboard,
};

export default function App() {
  const [page, setPage] = useState('dashboard');
  const PageComponent = DASHBOARDS[page];

  return (
    <>
      <div className="app-container">
        <aside className="sidebar">
          <nav>
            <button className={page === 'dashboard' ? 'active' : ''} onClick={() => setPage('dashboard')}>Dashboard</button>
            <button className={page === 'tickets' ? 'active' : ''} onClick={() => setPage('tickets')}>Tickets</button>
            <button className={page === 'devices' ? 'active' : ''} onClick={() => setPage('devices')}>Devices</button>
            <button className={page === 'checkouts' ? 'active' : ''} onClick={() => setPage('checkouts')}>Checkouts</button>
          </nav>
        </aside>
        <main className="main-content">
          <PageComponent />
        </main>
      </div>
    </>
  );
}