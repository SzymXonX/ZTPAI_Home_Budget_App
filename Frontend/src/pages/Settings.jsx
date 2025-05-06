import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Settings() {
    const navigate = useNavigate();

    const handleLogout = () => {
        navigate('/logout');
    };

    return (
        <div>
            Settings
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
};

export default Settings;