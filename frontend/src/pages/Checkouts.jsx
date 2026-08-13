import { useState, useEffect } from 'react';
import { getCheckouts, getActiveCheckouts, getCheckout, createCheckout, patchCheckout, checkIn } from '../api/checkouts.js';
import './Checkouts.css';

const CHECKOUT_STATUSES = ['active', 'returned'];
const CHECKIN_STATUSES = ['returned'];

function CreateCheckoutForm({ onCheckoutCreated }) {
    const [createError, setCreateError] = useState('');

    async function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const device_id = Number(formData.get('device_id'));
        const borrower_name = formData.get('borrower_name');
        const borrower_email = formData.get('borrower_email');
        const from_date = formData.get('from_date');
        const to_date = formData.get('to_date');

        if (!device_id || !borrower_name || !borrower_email || !from_date || !to_date) {
            setCreateError('Please fill in all required fields.');
            return;
        }

        setCreateError('');
        const result = await createCheckout(device_id, borrower_name, borrower_email, from_date, to_date);
        if (result?.detail) {
            setCreateError(result.detail);
            return;
        }

        setCreateError('');
        await onCheckoutCreated();
        event.target.reset();
    }

    return (
        <>
            <h2> Create Checkout </h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="device_id"> Device ID: </label>
                    <input type="number" name="device_id" id="device_id" required />
                </div>
                <div>
                    <label htmlFor="borrower_name"> Borrower name: </label>
                    <input type="text" name="borrower_name" id="borrower_name" required />
                </div>
                <div>
                    <label htmlFor="borrower_email"> Borrower email: </label>
                    <input type="email" name="borrower_email" id="borrower_email" required />
                </div>
                <div>
                    <label htmlFor="from_date"> From date: </label>
                    <input type="datetime-local" name="from_date" id="from_date" required />
                </div>
                <div>
                    <label htmlFor="to_date"> To date: </label>
                    <input type="datetime-local" name="to_date" id="to_date" required />
                </div>
                {createError && <p className="error-message">{createError}</p>}
                <div>
                    <input type="submit" value="Submit" />
                </div>
            </form>
        </>
    );
}

function CheckoutByIdForm({ onFetch, checkout, error }) {
    const [localError, setLocalError] = useState('');

    async function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const checkout_id = formData.get('checkout_id');

        if (!checkout_id) {
            setLocalError('Please enter a checkout ID.');
            return;
        }

        setLocalError('');
        await onFetch(Number(checkout_id));
    }

    return (
        <>
            <h2> Get Checkout by ID </h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="checkout_id"> Enter checkout ID: </label>
                    <input type="number" name="checkout_id" id="checkout_id" required />
                </div>
                <div>
                    <input type="submit" value="Submit" />
                </div>
            </form>
            {(localError || error) && <p className="error-message">{localError || error}</p>}
            {checkout && (
                <div className="checkout-details">
                    <p><strong>ID:</strong> {checkout.cid}</p>
                    <p><strong>Device ID:</strong> {checkout.device_id}</p>
                    <p><strong>Borrower name:</strong> {checkout.borrower_name}</p>
                    <p><strong>Borrower email:</strong> {checkout.borrower_email}</p>
                    <p><strong>From:</strong> {checkout.from_date}</p>
                    <p><strong>To:</strong> {checkout.to_date}</p>
                    <p><strong>Status:</strong> {checkout.status}</p>
                </div>
            )}
        </>
    );
}

function CheckoutUpdateForm({ onUpdate, result, error }) {
    const [localError, setLocalError] = useState('');

    async function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const checkout_id = Number(formData.get('checkout_id'));
        const to_date = formData.get('to_date');
        const status = formData.get('status');

        if (!checkout_id || !to_date || !status) {
            setLocalError('Please fill in all required fields.');
            return;
        }

        setLocalError('');
        await onUpdate(checkout_id, to_date, status);
    }

    return (
        <>
            <h2> Update Checkout </h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="checkout_id"> Checkout ID: </label>
                    <input type="number" name="checkout_id" id="checkout_id" required />
                </div>
                <div>
                    <label htmlFor="to_date"> New to date: </label>
                    <input type="datetime-local" name="to_date" id="to_date" required />
                </div>
                <div>
                    <label htmlFor="status"> Status: </label>
                    <select name="status" id="status" required>
                        <option value="">Select status</option>
                        {CHECKOUT_STATUSES.map(statusOption => (
                            <option key={statusOption} value={statusOption}>{statusOption}</option>
                        ))}
                    </select>
                </div>
                <div>
                    <input type="submit" value="Submit" />
                </div>
            </form>
            {(localError || error) && <p className="error-message">{localError || error}</p>}
            {result && !error && (
                <div className="checkout-details">
                    <p><strong>Updated Checkout ID:</strong> {result.cid}</p>
                    <p><strong>Status:</strong> {result.status}</p>
                    <p><strong>To date:</strong> {result.to_date}</p>
                </div>
            )}
        </>
    );
}

function CheckInForm({ onCheckIn, result, error }) {
    const [localError, setLocalError] = useState('');

    async function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const checkout_id = Number(formData.get('checkout_id'));
        const status = formData.get('status');

        if (!checkout_id || !status) {
            setLocalError('Please fill in all required fields.');
            return;
        }

        setLocalError('');
        await onCheckIn(checkout_id, status);
    }

    return (
        <>
            <h2> Check In </h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="checkout_id"> Checkout ID: </label>
                    <input type="number" name="checkout_id" id="checkout_id" required />
                </div>
                <div>
                    <label htmlFor="status"> Status: </label>
                    <select name="status" id="status" required>
                        <option value="">Select status</option>
                        {CHECKIN_STATUSES.map(statusOption => (
                            <option key={statusOption} value={statusOption}>{statusOption}</option>
                        ))}
                    </select>
                </div>
                <div>
                    <input type="submit" value="Submit" />
                </div>
            </form>
            {(localError || error) && <p className="error-message">{localError || error}</p>}
            {result && !error && (
                <div className="checkout-details">
                    <p><strong>Checked in checkout ID:</strong> {result.cid}</p>
                    <p><strong>Status:</strong> {result.status}</p>
                </div>
            )}
        </>
    );
}

function CheckoutRow({ checkout }) {
    return (
        <tr>
            <td>{checkout.cid}</td>
            <td>{checkout.device_id}</td>
            <td>{checkout.borrower_name}</td>
            <td>{checkout.borrower_email}</td>
            <td>{checkout.from_date}</td>
            <td>{checkout.to_date}</td>
            <td>{checkout.status}</td>
        </tr>
    );
}

function CheckoutTable({ checkouts }) {
    const safeCheckouts = Array.isArray(checkouts) ? checkouts : [];

    return (
        <>
            <h2> Checkout Table </h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Device ID</th>
                        <th>Borrower</th>
                        <th>Email</th>
                        <th>From</th>
                        <th>To</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {safeCheckouts.map(checkout => (
                        <CheckoutRow key={checkout.cid} checkout={checkout} />
                    ))}
                </tbody>
            </table>
        </>
    );
}

function ActiveCheckoutList({ checkouts, error }) {
    return (
        <>
            <h2> Active Checkouts </h2>
            {error && <p className="error-message">{error}</p>}
            {Array.isArray(checkouts) && checkouts.length > 0 ? (
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Device ID</th>
                            <th>Borrower</th>
                            <th>Email</th>
                            <th>From</th>
                            <th>To</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {checkouts.map(checkout => (
                            <CheckoutRow key={checkout.cid} checkout={checkout} />
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>No active checkouts found.</p>
            )}
        </>
    );
}

export function CheckoutDashboard() {
    const [checkouts, setCheckouts] = useState([]);
    const [activeCheckouts, setActiveCheckouts] = useState([]);
    const [selectedCheckout, setSelectedCheckout] = useState(null);
    const [checkoutError, setCheckoutError] = useState('');
    const [activeError, setActiveError] = useState('');
    const [updateError, setUpdateError] = useState('');
    const [updateResult, setUpdateResult] = useState(null);
    const [checkInError, setCheckInError] = useState('');
    const [checkInResult, setCheckInResult] = useState(null);

    async function refreshCheckouts() {
        const result = await getCheckouts();
        setCheckouts(result?.checkouts || []);
    }

    async function refreshActiveCheckouts() {
        const result = await getActiveCheckouts();
        if (!result || result.detail || Array.isArray(result)) {
            setActiveError(result?.detail || 'Unable to fetch active checkouts.');
            setActiveCheckouts([]);
            return;
        }
        setActiveError('');
        setActiveCheckouts(result?.checkouts || []);
    }

    async function handleFetchCheckout(cid) {
        setCheckoutError('');
        setSelectedCheckout(null);

        const result = await getCheckout(cid);
        if (!result || result.detail || Array.isArray(result)) {
            setCheckoutError(result?.detail || 'Unable to fetch checkout.');
            return;
        }

        setSelectedCheckout(result);
    }

    async function handleUpdateCheckout(cid, to_date, status) {
        setUpdateError('');
        setUpdateResult(null);

        const result = await patchCheckout(cid, to_date, status);
        if (!result || result.detail || Array.isArray(result)) {
            setUpdateError(result?.detail || 'Unable to update checkout.');
            return;
        }

        setUpdateResult(result);
        await refreshCheckouts();
        await refreshActiveCheckouts();
    }

    async function handleCheckIn(cid, status) {
        setCheckInError('');
        setCheckInResult(null);

        const result = await checkIn(cid, status);
        if (!result || result.detail || Array.isArray(result)) {
            setCheckInError(result?.detail || 'Unable to check in checkout.');
            return;
        }

        setCheckInResult(result);
        await refreshCheckouts();
        await refreshActiveCheckouts();
    }

    useEffect(() => {
        async function fetchData() {
            await refreshCheckouts();
            await refreshActiveCheckouts();
        }
        fetchData();
    }, []);

    return (
        <>
            <div>
                <CheckoutTable checkouts={checkouts} />
                <CreateCheckoutForm onCheckoutCreated={refreshCheckouts} />
                <CheckoutByIdForm onFetch={handleFetchCheckout} checkout={selectedCheckout} error={checkoutError} />
                <CheckoutUpdateForm onUpdate={handleUpdateCheckout} result={updateResult} error={updateError} />
                <CheckInForm onCheckIn={handleCheckIn} result={checkInResult} error={checkInError} />
                <button onClick={refreshActiveCheckouts}>Refresh active checkouts</button>
                <ActiveCheckoutList checkouts={activeCheckouts} error={activeError} />
            </div>
        </>
    );
}
