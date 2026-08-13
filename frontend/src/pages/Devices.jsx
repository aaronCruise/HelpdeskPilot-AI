import { useState, useEffect } from 'react';
import { getDevices, getDevice, createDevice, patchDevice } from '../api/devices.js';
import './Devices.css';

const DEVICE_TYPES = ['computer', 'phone', 'tablet', 'accessory'];
const DEVICE_STATES = ['available', 'checked_out', 'maintenance', 'retired'];

function CreateDeviceForm({ onDeviceCreated }) {
    const [createError, setCreateError] = useState('');

    async function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const asset_tag = formData.get('asset_tag');
        const name = formData.get('name');
        const type = formData.get('type');

        if (!asset_tag || !name || !type) {
            setCreateError('Please fill in all required fields.');
            return;
        }

        setCreateError('');
        const result = await createDevice(asset_tag, name, type);
        if (result?.detail) {
            setCreateError(result.detail);
            return;
        }

        setCreateError('');
        await onDeviceCreated();
        event.target.reset();
    }

    return (
        <>
            <h2> Create Device </h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="asset_tag"> Asset tag: </label>
                    <input type="text" name="asset_tag" id="asset_tag" required />
                </div>
                <div>
                    <label htmlFor="name"> Device name: </label>
                    <input type="text" name="name" id="name" required />
                </div>
                <div>
                    <label htmlFor="type"> Type: </label>
                    <select name="type" id="type" required>
                        <option value="">Select type</option>
                        {DEVICE_TYPES.map(typeOption => (
                            <option key={typeOption} value={typeOption}>{typeOption}</option>
                        ))}
                    </select>
                </div>
                {createError && <p className="error-message">{createError}</p>}
                <div>
                    <input type="submit" value="Submit" />
                </div>
            </form>
        </>
    );
}

function DeviceByIdForm({ onFetch, device, error }) {
    async function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const device_id = formData.get('device_id');

        if (!device_id) {
            return;
        }

        await onFetch(Number(device_id));
    }

    return (
        <>
            <h2> Get Device by ID </h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="device_id"> Enter device ID: </label>
                    <input type="number" name="device_id" id="device_id" required />
                </div>
                <div>
                    <input type="submit" value="Submit" />
                </div>
            </form>
            {error && <p className="error-message">{error}</p>}
            {device && (
                <div className="device-details">
                    <p><strong>ID:</strong> {device.did}</p>
                    <p><strong>Asset tag:</strong> {device.asset_tag}</p>
                    <p><strong>Name:</strong> {device.name}</p>
                    <p><strong>Type:</strong> {device.type}</p>
                    <p><strong>State:</strong> {device.state}</p>
                    <p><strong>Created:</strong> {device.created_at}</p>
                </div>
            )}
        </>
    );
}

function UpdateDeviceStateForm({ onUpdate, result, error }) {
    const [localError, setLocalError] = useState('');

    async function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const device_id = formData.get('device_id');
        const state = formData.get('state');

        if (!device_id || !state) {
            setLocalError('Please fill in all required fields.');
            return;
        }

        setLocalError('');
        await onUpdate(Number(device_id), state);
    }

    return (
        <>
            <h2> Update Device State </h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="device_id"> Device ID: </label>
                    <input type="number" name="device_id" id="device_id" required />
                </div>
                <div>
                    <label htmlFor="state"> New state: </label>
                    <select name="state" id="state" required>
                        <option value="">Select state</option>
                        {DEVICE_STATES.map(stateOption => (
                            <option key={stateOption} value={stateOption}>{stateOption}</option>
                        ))}
                    </select>
                </div>
                <div>
                    <input type="submit" value="Submit" />
                </div>
            </form>
            {(localError || error) && <p className="error-message">{localError || error}</p>}
            {result && !error && (
                <div className="device-details">
                    <p><strong>Updated Device ID:</strong> {result.did}</p>
                    <p><strong>State:</strong> {result.state}</p>
                </div>
            )}
        </>
    );
}

function DeviceRow({ device }) {
    return (
        <tr>
            <td>{device.did}</td>
            <td>{device.asset_tag}</td>
            <td>{device.name}</td>
            <td>{device.type}</td>
            <td>{device.state}</td>
            <td>{device.created_at}</td>
        </tr>
    );
}

function DeviceTable({ devices }) {
    const safeDevices = Array.isArray(devices) ? devices : [];

    return (
        <>
            <h2> Device Table </h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Asset Tag</th>
                        <th>Name</th>
                        <th>Type</th>
                        <th>State</th>
                        <th>Created</th>
                    </tr>
                </thead>
                <tbody>
                    {safeDevices.map(device => (
                        <DeviceRow key={device.did} device={device} />
                    ))}
                </tbody>
            </table>
        </>
    );
}

export function DeviceDashboard() {
    const [devices, setDevices] = useState([]);
    const [selectedDevice, setSelectedDevice] = useState(null);
    const [deviceError, setDeviceError] = useState('');
    const [updateResult, setUpdateResult] = useState(null);
    const [updateError, setUpdateError] = useState('');

    async function refreshDevices() {
        const result = await getDevices();
        setDevices(result?.devices || []);
    }

    async function handleFetchDevice(did) {
        setDeviceError('');
        setSelectedDevice(null);

        const result = await getDevice(did);
        if (!result || result.detail || Array.isArray(result)) {
            setDeviceError(result?.detail || 'Unable to fetch device.');
            return;
        }

        setSelectedDevice(result);
    }

    async function handleUpdateDevice(did, state) {
        setUpdateError('');
        setUpdateResult(null);

        const result = await patchDevice(did, state);
        if (!result || result.detail || Array.isArray(result)) {
            setUpdateError(result?.detail || 'Unable to update device.');
            return;
        }

        setUpdateResult(result);
        await refreshDevices();
    }

    useEffect(() => {
        async function fetchDevices() {
            await refreshDevices();
        }
        fetchDevices();
    }, []);

    return (
        <>
            <div>
                <DeviceTable devices={devices} />
                <CreateDeviceForm onDeviceCreated={refreshDevices} />
                <DeviceByIdForm onFetch={handleFetchDevice} device={selectedDevice} error={deviceError} />
                <UpdateDeviceStateForm onUpdate={handleUpdateDevice} result={updateResult} error={updateError} />
            </div>
        </>
    );
}
