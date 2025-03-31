import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants"; 
import LoadingIndicator from "../components/LoadingIndicator";
import "../styles/Login.css";

//Zdjęcia
import Logo from '../assets/logo.png';
import OpenEye from '../assets/open_eye_password.png';
import ClosedEye from '../assets/closed_eye_password.png';

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();
        try {
            const res = await api.post("/api/token/", { username, password })
            localStorage.setItem(ACCESS_TOKEN, res.data.access);
            localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
            navigate("/");
        } catch (error) {
            alert("Błędne dane logowania. Sprawdź swoje dane i spróbuj ponownie.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <div className="left-container">
                <div className="image-container">
                    <img src={Logo} alt="Logo" />
                </div>
            </div>
            <div className="right-container">
                <div className="login-container">
                    <form className="login" onSubmit={handleSubmit}>
                        <label htmlFor="Username">Username</label>
                        <input
                            id="Username"
                            type="text"
                            name="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />

                        <label htmlFor="password">hasło</label>
                        <div className="password_image">
                            <input
                                id="password"
                                type="password"
                                name="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                            <img
                                src={ClosedEye}
                                alt="eye"
                                id="eye"
                            />
                        </div>

                        {loading && <LoadingIndicator />}
                        <button id="login-button" type="submit">
                            zaloguj
                        </button>
                    </form>
                    <a id="no-account-link" href="/register">
                        nie masz konta?
                    </a>
                </div>
            </div>
        </div>
    );
}

export default Login;
