import React, { useEffect, useState } from 'react';
import '../../styles/style.css'; // Adjust path as needed
import config from '../env-config';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

const ForgotPassword: React.FC = () => {
    const navigate = useNavigate();
    const [isTokenValid, setIstokenValid] = useState<boolean | null>(null);

    // check if login token has expired
    useEffect(() => {
        const validateToken = () => {
            const token = localStorage.getItem("userToken");
            if (!token){
                setIstokenValid(false);
                return;
            }

            try {
                const decodedToken = jwtDecode(token);
                const currentTime = Date.now() / 1000; // convert to seconds
                if (decodedToken.exp < currentTime) {
                    localStorage.removeItem("userToken");
                    setIstokenValid(false);
                } else {
                    setIstokenValid(true);
                }
            } catch (error) {
                console.error("Error deccoding token:", error);
                localStorage.removeItem("userToken");
                setIstokenValid(false);
            }
        };

        validateToken();
    }, []);

    useEffect(() => {
        if (isTokenValid === false) {
            navigate("/login")
        }
    }, [isTokenValid, navigate]);

    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [message, setMessage] = useState('');

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setMessage(''); // Clear previous message

        // Prompt for confirmation
        const confirmed = window.confirm('Are you sure you want to change your password?');
        if (!confirmed) {
            setIsLoading(false); // Set isLoading to false when canceled
            // Blur the button to remove focus
            const resetBtn = document.getElementById('resetBtn');
            if (resetBtn) {
                resetBtn.blur();
            }
            return;
        }

        setIsLoading(true);

        try {
            const token = localStorage.getItem('userToken');
            const response = await fetch(`${config.userBackend}/change_password`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ password, repeatPassword })
            });
            const data = await response.json();
            if (response.ok) {
                setMessage(data.message);
            } else {
                setMessage(data.message);
            }
        } catch (error) {
            setMessage("Failed to connect to the server.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleCancel = () => {
        navigate('/profile'); 
    };

    return (
        <div className="container" id="change-password">
            <button className="btn-cancel" onClick={handleCancel}>Back</button>
            <form onSubmit={handleSubmit}>
                <h1 className="form-title">
                    Change your password
                    <span className="form-subtitle">Enter a new password and submit to change your password</span>
                </h1>
                <div className="input-group">
                    <label htmlFor="password">Enter your new password<span className="required">*</span></label>
                    <input type="password" name="password" id="password" placeholder="Password" required
                        value={password} onChange={(e) => setPassword(e.target.value)} />
                    <i className="fas fa-lock"></i>
                </div>
                <ul className="password-requirements">
                    <li><i className="fas fa-info-circle"></i> Must be at least 8 characters long</li>
                    <li><i className="fas fa-info-circle"></i> Must contain an uppercase and a lowercase letter</li>
                </ul>
                <div className="input-group">
                    <label htmlFor="repeat-password">Repeat your new password<span className="required">*</span></label>
                    <input type="password" name="repeat-password" id="repeat-password" placeholder="Repeat password" required
                        value={repeatPassword} onChange={(e) => setRepeatPassword(e.target.value)} />
                    <i className="fas fa-lock"></i>
                </div>
                {message && <p className="error-message">{message}</p>}
                {isLoading && <p className="loading-message">Please wait...</p>}
                <input type="submit" className="btn" value="Change Password" id="resetBtn" disabled={isLoading}/>
            </form>
        </div>
    );
};

export default ForgotPassword;
