import { useState } from 'react';
import { TicketDashboard } from './pages/Tickets.jsx';
import { DeviceDashboard } from './pages/Devices.jsx';
import { CheckoutDashboard } from './pages/Checkouts.jsx';

const DASHBOARDS = {
  tickets: TicketDashboard,
  devices: DeviceDashboard,
  checkouts: CheckoutDashboard,
};

export default function App() {
  const [page, setPage] = useState('tickets');
  const PageComponent = DASHBOARDS[page];

  return (
    <>
      <nav>
        <button onClick={() => setPage('tickets')}>Tickets</button>
        <button onClick={() => setPage('devices')}>Devices</button>
        <button onClick={() => setPage('checkouts')}>Checkouts</button>
      </nav>
      <PageComponent />
    </>
  );
}