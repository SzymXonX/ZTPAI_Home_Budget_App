import { useState } from "react";
import api from "../api";
import { useNavigate, Link} from "react-router-dom";
import { useLocation } from 'react-router-dom';
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants"; 
import LoadingIndicator from "../components/LoadingIndicator";

import useTimedMessage from "../hooks/useTimedMessage";
import "../styles/LoginRegister.css";
import "../styles/Global.css";

import Logo from '../assets/logo_bez_tla.png';
import { ImEye, ImEyeBlocked } from "react-icons/im";


function Login() {
	const location = useLocation();
	const state = location.state || {};
	const message = state.message || '';
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [loading, setLoading] = useState(false);
	const [passwordVisible, setPasswordVisible] = useState(false);
	const navigate = useNavigate();
	const [formError, setFormError] = useTimedMessage('');
	const [formSuccess, setFormSuccess] = useTimedMessage(message);


	const togglePasswordVisibility = () => {
		setPasswordVisible(!passwordVisible);
	};
	
	document.title = "Login";

	const handleSubmit = async (e) => {
		setLoading(true);
		e.preventDefault();
		setFormError('');
		setFormSuccess('');
		try {
			const res = await api.post("/api/token/", { username, password })
			localStorage.setItem(ACCESS_TOKEN, res.data.access);
			localStorage.setItem(REFRESH_TOKEN, res.data.refresh);

			const userRes = await api.get("/api/user-info/", {});

			const isSuperUser = userRes.data.is_superuser;
			localStorage.setItem("IS_SUPERUSER", JSON.stringify(isSuperUser));

			navigate("/");
		} catch (error) {
			setFormError("Błędne dane logowania. Sprawdź swoje dane i spróbuj ponownie.");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="login-app-page">
			{formError && <p className="error-message login-message">{formError}</p>}
			{formSuccess && <p className="success-message login-message">{formSuccess}</p>}
			<div className="container">
				<div className="left-container">
					<div className="image-container">
						<img src={Logo} alt="Logo" />
					</div>
				</div>
				<div className="right-container">
					<div className="formLogin">
						<form className="login" onSubmit={handleSubmit}>
							<label htmlFor="Username">nazwa użytkownika</label>
							<input
								id="Username"
								type="text"
								name="username"
								value={username}
								onChange={(e) => setUsername(e.target.value)}
								required
								autoComplete="off"
							/>

							<label htmlFor="password">hasło</label>
							<div className="password_image">
								<input 
									id="password" 
									type={passwordVisible ? "text" : "password"} 
									name="password" 
									value={password} 
									onChange={(e) => setPassword(e.target.value)} 
									required
									autoComplete="off"
								/>
								<div className="eye-icon-login" onClick={togglePasswordVisibility}>
									{passwordVisible ? (
										<ImEye id="eye-login"/> 
									) : (
										<ImEyeBlocked id="eye-login"/>
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
		</div>
	);
}

export default Login;
