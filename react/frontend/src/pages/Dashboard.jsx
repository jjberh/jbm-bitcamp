import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Dashboard.css';
import { supabase } from '../lib/supabase';

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
            // Get the session from Supabase
            const { data: { session }, error: sessionError } = await supabase.auth.getSession();
            
            if (sessionError) {
                console.error('Session error:', sessionError);
                setError('Authentication error');
                return;
            }

            if (!session) {
                console.log('No session found');
                setError('Please log in to view your dashboard');
                return;
            }

            console.log('Session found:', session);

            const response = await axios.get('https://jbm-bitcamp.onrender.com/dashboard', {
                headers: {
                    'Authorization': `Bearer ${session.access_token}`
                }
            });

            console.log('Dashboard response:', response.data);
            setUserData(response.data);
            setFormData({
                username: response.data.username || '',
                email: response.data.email || ''
            });
        } catch (err) {
            console.error('Dashboard error:', err);
            setError('Failed to fetch user data: ' + (err.response?.data?.error || err.message));
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
            const { data: { session }, error: sessionError } = await supabase.auth.getSession();
            
            if (sessionError || !session) {
                setError('Please log in to update your profile');
                return;
            }

            await axios.post('https://jbm-bitcamp.onrender.com/dashboard', formData, {
                headers: {
                    'Authorization': `Bearer ${session.access_token}`
                }
            });
            setIsEditing(false);
            fetchUserData(); // Refresh the data
        } catch (err) {
            setError('Failed to update user data: ' + (err.response?.data?.error || err.message));
            console.error(err);
        }
    };

    if (error) {
        return (
            <div className="dashboard-container">
                <h1>Dashboard</h1>
                <div className="error-message">{error}</div>
                <button 
                    className="edit-btn" 
                    onClick={() => window.location.href = '/login'}
                >
                    Go to Login
                </button>
            </div>
        );
    }

    if (!userData) {
        return (
            <div className="dashboard-container">
                <h1>Dashboard</h1>
                <div className="dashboard-loading">Loading...</div>
            </div>
        );
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
  