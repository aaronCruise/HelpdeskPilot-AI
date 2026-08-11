import { useState, useEffect } from 'react';
import { getTickets } from './api/tickets.js';
import { getDevices } from './api/devices.js';
import { getActiveCheckouts } from './api/checkouts.js';
import { TicketDashboard } from './pages/Tickets.jsx';
import { DeviceDashboard } from './pages/Devices.jsx';
import { CheckoutDashboard } from './pages/Checkouts.jsx';

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
      <h1>Dashboard</h1>
      <div>
        <div>
          <h2>Open Tickets</h2>
          <p>{openTickets}</p>
        </div>
        <div>
          <h2>Available Devices</h2>
          <p>{availableDevices}</p>
        </div>
        <div>
          <h2>Active Checkouts</h2>
          <p>{activeCheckouts}</p>
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
      <div style={{ display: 'flex', minHeight: '100vh' }}>
        <aside style={{ width: '180px', padding: '20px', borderRight: '1px solid #ccc' }}>
          <button onClick={() => setPage('dashboard')}>Dashboard</button>
          <button onClick={() => setPage('tickets')}>Tickets</button>
          <button onClick={() => setPage('devices')}>Devices</button>
          <button onClick={() => setPage('checkouts')}>Checkouts</button>
        </aside>
        <main style={{ flex: 1, padding: '20px' }}>
          <PageComponent />
        </main>
      </div>
    </>
  );
}