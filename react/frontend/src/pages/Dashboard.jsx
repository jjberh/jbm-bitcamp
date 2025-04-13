import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Dashboard.css';

const Dashboard = () => {
    const [userData, setUserData] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({
        username: '',
        email: ''
    });
    const [error, setError] = useState('');

    useEffect(() => {
        fetchUserData();
    }, []);

    const fetchUserData = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get('http://localhost:5000/dashboard', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            setUserData(response.data);
            setFormData({
                username: response.data.username || '',
                email: response.data.email || ''
            });
        } catch (err) {
            setError('Failed to fetch user data');
            console.error(err);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const token = localStorage.getItem('token');
            await axios.post('http://localhost:5000/dashboard', formData, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            setIsEditing(false);
            fetchUserData(); // Refresh the data
        } catch (err) {
            setError('Failed to update user data');
            console.error(err);
        }
    };

    if (!userData) {
        return <div className="dashboard-loading">Loading...</div>;
    }

    return (
        <div className="dashboard-container">
            <h1>Dashboard</h1>
            {error && <div className="error-message">{error}</div>}
            
            {isEditing ? (
                <form onSubmit={handleSubmit} className="dashboard-form">
                    <div className="form-group">
                        <label htmlFor="username">Username:</label>
                        <input
                            type="text"
                            id="username"
                            name="username"
                            value={formData.username}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="email">Email:</label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            value={formData.email}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className="form-actions">
                        <button type="submit" className="save-btn">Save Changes</button>
                        <button type="button" className="cancel-btn" onClick={() => setIsEditing(false)}>
                            Cancel
                        </button>
                    </div>
                </form>
            ) : (
                <div className="user-info">
                    <p><strong>Username:</strong> {userData.username}</p>
                    <p><strong>Email:</strong> {userData.email}</p>
                    <button className="edit-btn" onClick={() => setIsEditing(true)}>
                        Edit Profile
                    </button>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
  