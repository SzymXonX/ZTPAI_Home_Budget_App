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

function Register() {
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [passwordVisible, setPasswordVisible] = useState(false);
    const navigate = useNavigate();

    const togglePasswordVisibility = () => {
        setPasswordVisible(!passwordVisible);
    };

    document.title = "Rejestracja";

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();
        try {
            const res = await api.post("/api/user/register/", { username, password, first_name: firstName, last_name: lastName, email })
            navigate("/login");
        } catch (error) {
            alert("Istnieje użytkownik o podanej nazwie użytkownika");
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
                        <label htmlFor="firstName">imię</label>
                        <input id="firstName" type="text" name="firstName"
                            value={firstName} onChange={(e) => setFirstName(e.target.value)} required
                            />
                        
                        <label htmlFor="lastName">nazwisko</label>
                        <input id="lastName" type="text" name="lastName"
                            value={lastName} onChange={(e) => setLastName(e.target.value)} required
                            />

                        <label htmlFor="email">email</label>
                        <input id="email" type="email" name="email"
                            value={email} onChange={(e) => setEmail(e.target.value)} required
                            />

                        <label htmlFor="Username">nazwa użytkownika</label>
                        <input id="Username" type="text" name="username"
                            value={username} onChange={(e) => setUsername(e.target.value)} required
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
                            zarejestruj
                        </button>
                    </form>
                    <Link id="no-account-link" to="/login">
                        masz konto?
                    </Link>
                </div>
            </div>
        </div>
    );
}

export default Register;
