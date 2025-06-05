import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

import useTimedMessage from '../hooks/useTimedMessage';
import '../styles/Settings.css'; 

import { ImEye, ImEyeBlocked } from "react-icons/im";


function Settings() {
	const navigate = useNavigate();

  const [userProfileData, setUserProfileData] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: ''
  });

  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmNewPassword, setShowConfirmNewPassword] = useState(false);
  const [formError, setFormError] = useTimedMessage('');
  const [formSuccess, setFormSuccess] = useTimedMessage('');

  const [loading, setLoading] = useState(false);

  document.title = "Settings";

	const handleLogout = () => {
		navigate('/logout');
	};


	const fetchUserData = useCallback(async () => {
    try {
      const response = await api.get("/api/user-info/", {});
      setUserProfileData(response.data);
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
	}, []);

  useEffect(() => {
    fetchUserData();
  }, [fetchUserData]);


	const toggleNewPasswordVisibility = () => {
    setShowNewPassword(prev => !prev);
  };
  const toggleConfirmNewPasswordVisibility = () => {
    setShowConfirmNewPassword(prev => !prev);
  };

  const handleChangeProfileData = async (e) => {
    e.preventDefault();
    setLoading(true);
    setFormError('');
    setFormSuccess('');

    try {
      const response = await api.patch('/api/user-info/', userProfileData);
      setFormSuccess("Dane profilowe zostały pomyślnie zaktualizowane.");
      setUserProfileData(response.data);
    } catch (err) {
      let errorMessage = 'Wystąpił błąd podczas aktualizacji danych profilowych. Spróbuj ponownie.';
      if (err.response?.data) {
        const errorData = err.response.data;
        const detailErrors = Object.entries(errorData).map(([key, value]) => {
          if (Array.isArray(value)) {
            if (key === 'detail' || key === 'non_field_errors') {
              return value.join(', ');
            }
            return `${key}: ${value.join(', ')}`;
          }
          return value;
        }).join('\n');
        errorMessage = detailErrors;
      }
      setFormError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setLoading(true);
    setFormError('');
    setFormSuccess('');

    if (!newPassword || !confirmNewPassword) {
      setFormError('Wszystkie pola hasła są wymagane.');
      setLoading(false);
      return;
    }

    if (newPassword !== confirmNewPassword) {
      setFormError('Nowe hasła nie są zgodne.');
      setLoading(false);
      return;
    }

    try {
      const passwordData = {
          new_password: newPassword,
          confirm_password: confirmNewPassword
      };
      await api.post('/api/user/change-password/', passwordData);
      setFormSuccess('Hasło zostało pomyślnie zmienione.');
      setNewPassword('');
      setConfirmNewPassword('');
    } catch (error) {
      console.error('Błąd podczas zmiany hasła:', error);
      setFormError('Wystąpił błąd podczas zmiany hasła. Spróbuj ponownie.');
    } finally {
      setLoading(false);
    }
  };
  
	return (
		<div className="settings-app-content">
      {formError && <p className="error-message settings-message">{formError}</p>}
      {formSuccess && <p className="success-message settings-message">{formSuccess}</p>}
			<div className="dashboard-container">
				<div className="dashboard-row">
					<div className="settings-container">
						<div className="settings-list" id="settings-list">
							<form className="change-data-form" onSubmit={handleChangeProfileData}>
                <div className='form_group'>
                  <label htmlFor="username">nazwa użytkownika</label>
                  <input
                    id="username"
                    type="text"
                    name="username"
                    value={userProfileData.username}
                    onChange={(e) => setUserProfileData({ ...userProfileData, username: e.target.value })}
                    autoComplete="off"
                    required
                  />
                </div>
								<div className='form_group'>
									<label htmlFor="first_name">imię</label>
									<input
										id="first_name"
										type="text"
										name="first_name"
										value={userProfileData.first_name}
										onChange={(e) => setUserProfileData({ ...userProfileData, first_name: e.target.value })}
                    autoComplete="off"
										required
									/>
								</div>
								<div className='form_group'>
									<label htmlFor="last_name">nazwisko</label>
									<input
										id="last_name"
										type="text"
										name="last_name"
										value={userProfileData.last_name}
										onChange={(e) => setUserProfileData({ ...userProfileData, last_name: e.target.value })}
                    autoComplete="off"
										required
									/>
								</div>
								<div className='form_group'>
									<label htmlFor="email">email</label>
									<input
										id="email"
										type="email"
										name="email"
										value={userProfileData.email}
										onChange={(e) => setUserProfileData({ ...userProfileData, email: e.target.value })}
                    autoComplete="off"
										required
									/>
								</div>
                <div className='form_group'>
                  <button className="form-button" type="submit">zmień dane</button>
                </div>
              </form>

              <form className='change-password-form' onSubmit={handleChangePassword}>
								<div className='form_group'>
									<label htmlFor="password">hasło</label>
									<div className="password_image">
										<input 
                      id="password_settings" 
                      type={showNewPassword ? "text" : "password"} 
                      name="password" 
											value={newPassword} 
                      onChange={(e) => setNewPassword(e.target.value)} 
                      autoComplete="off"
                      required
										/>
										<div className="eye-icon" onClick={toggleNewPasswordVisibility}>
											{showNewPassword ? (
												<ImEye id="eye"/> 
											) : (
												<ImEyeBlocked id="eye"/>
											)}
										</div>
									</div>
								</div>
                <div className='form_group'>
									<label htmlFor="confirm_password">powtórz hasło</label>
									<div className="password_image">
										<input 
                      id="confirm_password_settings" 
                      type={showConfirmNewPassword ? "text" : "password"} 
                      name="confirm_password" 
                      value={confirmNewPassword} 
                      onChange={(e) => setConfirmNewPassword(e.target.value)} 
                      autoComplete="off"
                      required
										/>
										<div className="eye-icon" onClick={toggleConfirmNewPasswordVisibility}>
											{showConfirmNewPassword ? (
												<ImEye id="eye"/> 
											) : (
												<ImEyeBlocked id="eye"/>
											)}
										</div>
									</div>
								</div>
                <div className='form_group'>
                  <button className="form-button" type="submit">zmień hasło</button>
                </div>
              </form>
              
							<form onSubmit={handleLogout} className="logout-form">
                <div className='form_group'>
								  <button type="submit" className="logout_button form-button">wyloguj</button>
                </div>
							</form>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default Settings;