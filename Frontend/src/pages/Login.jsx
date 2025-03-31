import { useState } from "react";
import api from "../api";
import { useNavigate, Link } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants"; 
import LoadingIndicator from "../components/LoadingIndicator";
import "../styles/LoginRegister.css";
import "../styles/Global.css";

//Zdjęcia
import Logo from '../assets/logo.png';
import { ImEye, ImEyeBlocked } from "react-icons/im";


function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [passwordVisible, setPasswordVisible] = useState(false);
    const navigate = useNavigate();

    const togglePasswordVisibility = () => {
        setPasswordVisible(!passwordVisible);
    };
    
    document.title = "Login";

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
                <div className="form-container">
                    <form className="login" onSubmit={handleSubmit}>
                        <label htmlFor="Username">nazwa użytkownika</label>
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
                            <input id="password" type={passwordVisible ? "text" : "password"} name="password" 
                                value={password} onChange={(e) => setPassword(e.target.value)} required
                                />
                            <div className="eye-icon" onClick={togglePasswordVisibility}>
                                {passwordVisible ? (
                                    <ImEye id="eye"/> 
                                ) : (
                                    <ImEyeBlocked id="eye"/>
                                )}
                            </div>
                        </div>

                        {loading && <LoadingIndicator />}
                        <button id="login-button" type="submit">
                            zaloguj
                        </button>
                    </form>
                    <Link id="no-account-link" to="/register">
                        nie masz konta?
                    </Link>
                </div>
            </div>
        </div>
    );
}

export default Login;
