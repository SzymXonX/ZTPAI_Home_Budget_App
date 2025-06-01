import { useState, useEffect } from 'react';

const useTimedMessage = (initialValue = '', duration = 5000) => {
    const [message, setMessage] = useState(initialValue);

    useEffect(() => {
        if (message) {
            const timer = setTimeout(() => {
                setMessage('');
            }, duration);

            return () => clearTimeout(timer);
        }
    }, [message, duration]);

    return [message, setMessage];
};

export default useTimedMessage;