import React, { useEffect, useState, useCallback } from 'react';
import api from '../api';
import useTimedMessage from '../hooks/useTimedMessage';
import '../styles/Admin.css';

function Admin() {
	const [users, setUsers] = useState([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState('');
	const [editingUser, setEditingUser] = useState(null);
	const [expandedUser, setExpandedUser] = useState(null);
	const [editFormData, setEditFormData] = useState({
		username: '',
		first_name: '',
		last_name: '',
		email: '',
		is_staff: false,
		is_superuser: false,
	});
	const [newUserFormData, setNewUserFormData] = useState({
		username: '',
		email: '',
		password: '',
		password2: '',
		is_staff: false,
		is_superuser: false,
	});
	const [formError, setFormError] = useTimedMessage('');
	const [showNewUserForm, setShowNewUserForm] = useState(false);

  document.title = "Admin Panel";

	const getUserRole = (user) => {
		if (user.is_superuser) return 'Super Administrator';
		if (user.is_staff) return 'Administrator';
		return 'Użytkownik';
	};

	const fetchUsers = useCallback(async () => {
		setLoading(true);
		setError('');
		try {
			const response = await api.get('/api/admin/users/');
			let fetchedUsers = [];
			if (response.data && Array.isArray(response.data.results)) {
				fetchedUsers = response.data.results;
			} else if (Array.isArray(response.data)) {
				fetchedUsers = response.data;
			} else {
				setError('Nieoczekiwany format danych z serwera.');
				setUsers([]);
				return;
			}
			const sortedUsers = fetchedUsers.sort((a, b) => a.id - b.id);
			setUsers(sortedUsers);
		} catch (err) {
			setError('Nie udało się załadować listy użytkowników. Sprawdź uprawnienia administratora.');
			setUsers([]);
		} finally {
			setLoading(false);
		}
	}, []);

	useEffect(() => {
		fetchUsers();
	}, [fetchUsers]);

	const handleDelete = async (userId) => {
		const userToDelete = users.find(u => u.id === userId);
		if (userToDelete && (userToDelete.is_superuser || userToDelete.is_staff)) {
			setFormError('Nie możesz usunąć konta administratora.');
			return;
		}
		if (window.confirm('Czy na pewno chcesz usunąć tego użytkownika? Tej operacji nie można cofnąć!')) {
			setFormError('');
			try {
				await api.delete(`/api/admin/users/${userId}/`);
				setUsers((prevUsers) => prevUsers.filter((user) => user.id !== userId));
				setExpandedUser(null);
			} catch (err) {
				setFormError('Błąd podczas usuwania użytkownika. Spróbuj ponownie.');
			}
		}
	};

	const handleEditClick = (user) => {
		if (user.is_superuser) {
			setFormError('Nie możesz edytować konta super administratora.');
			return;
		}
		setEditingUser(user.id);
		setEditFormData({
			username: user.username,
			first_name: user.first_name || '',
			last_name: user.last_name || '',
			email: user.email,
			is_staff: user.is_staff,
			is_superuser: user.is_superuser,
		});
		setFormError('');
	};

	const handleEditFormChange = (e) => {
		const { name, value, type, checked } = e.target;
		setEditFormData((prevData) => ({
			...prevData,
			[name]: type === 'checkbox' ? checked : value,
		}));
	};

	const handleUpdateUser = async (e) => {
		e.preventDefault();
		setFormError('');
		try {
			await api.patch(`/api/admin/users/${editingUser}/`, editFormData);
			fetchUsers();
			setEditingUser(null);
			setExpandedUser(null);
		} catch (err) {
			let errorMessage = 'Błąd podczas aktualizacji użytkownika. Sprawdź wprowadzone dane.';
			if (err.response?.data) {
				const detailErrors = Object.entries(err.response.data)
					.map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
					.join('\n');
				errorMessage += `\n${detailErrors}`;
			}
			setFormError(errorMessage);
		}
	};

	const handleNewUserFormChange = (e) => {
		const { name, value, type, checked } = e.target;
		setNewUserFormData((prevData) => ({
			...prevData,
			[name]: type === 'checkbox' ? checked : value,
		}));
	};

	const handleCreateUser = async (e) => {
		e.preventDefault();
		setFormError('');
		if (newUserFormData.password !== newUserFormData.password2) {
			setFormError('Hasła nie są zgodne.');
			return;
		}
		try {
			await api.post('/api/admin/users/', {
				username: newUserFormData.username,
				email: newUserFormData.email,
				password: newUserFormData.password,
				is_staff: newUserFormData.is_staff,
				is_superuser: newUserFormData.is_superuser,
			});
			setNewUserFormData({ username: '', email: '', password: '', password2: '', is_staff: false, is_superuser: false });
			setShowNewUserForm(false);
			fetchUsers();
		} catch (err) {
			let errorMessage = 'Błąd podczas tworzenia użytkownika. Sprawdź wprowadzone dane.';
			if (err.response?.data) {
				const detailErrors = Object.entries(err.response.data)
					.map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`)
					.join('\n');
				errorMessage += `\n${detailErrors}`;
			}
			setFormError(errorMessage);
		}
	};

	if (loading) {
		return (
			<div className='admin-app-content'>
				<p>Ładowanie panelu administracyjnego...</p>
			</div>
		);
	}

	if (error) {
		return (
			<div className='admin-app-content'>
				<p className="error-message">{error}</p>
			</div>
		);
	}

	return (
		<div className='admin-app-content'>
      {formError && <p className="error-message">{formError}</p>}
			<h1>panel Administracyjny</h1>
			<button
				className="toggle-form-button"
				onClick={() => {
					setShowNewUserForm(!showNewUserForm);
					setFormError('');
				}}>
				{showNewUserForm ? 'ukryj formularz dodawania użytkownika' : 'dodaj nowego użytkownika'}
			</button>
			{showNewUserForm && (
				<div className="new-user-form-container">
					<h3>Dodaj nowego użytkownika</h3>
					<form onSubmit={handleCreateUser}>
						<div>
							<label>Nazwa użytkownika:</label>
							<input
								type="text"
								name="username"
								value={newUserFormData.username}
								onChange={handleNewUserFormChange}
								required
							/>
						</div>
						<div>
							<label>Email:</label>
							<input
								type="email"
								name="email"
								value={newUserFormData.email}
								onChange={handleNewUserFormChange}
								required
							/>
						</div>
						<div>
							<label>Hasło:</label>
							<input
								type="password"
								name="password"
								value={newUserFormData.password}
								onChange={handleNewUserFormChange}
								required
							/>
						</div>
						<div>
							<label>Potwierdź Hasło:</label>
							<input
								type="password"
								name="password2"
								value={newUserFormData.password2}
								onChange={handleNewUserFormChange}
								required
							/>
						</div>
						<div>
							<label>
								<input
									type="checkbox"
									name="is_staff"
									checked={newUserFormData.is_staff}
									onChange={handleNewUserFormChange}
								/>
								Administrator
							</label>
						</div>
						<div>
							<label>
								<input
									type="checkbox"
									name="is_superuser"
									checked={newUserFormData.is_superuser}
									onChange={handleNewUserFormChange}
								/>
								Super Administrator
							</label>
						</div>
						<button type="submit">Utwórz użytkownika</button>
						<button type="button" onClick={() => setShowNewUserForm(false)}>Anuluj</button>
					</form>
				</div>
			)}
			<div className="user-list-section">
				<h3>Lista użytkowników</h3>
				<table className="users-table">
					<thead>
						<tr>
							<th>ID</th>
							<th>Nazwa użytkownika</th>
							<th>Rola</th>
							<th></th>
						</tr>
					</thead>
					<tbody>
						{Array.isArray(users) && users.length > 0 ? (
							users.map((user) => (
								<React.Fragment key={user.id}>
									<tr className="user-summary-row" onClick={() => setExpandedUser(expandedUser === user.id ? null : user.id)}>
										<td>{user.id}</td>
										<td>{user.username}</td>
										<td>{getUserRole(user)}</td>
										<td>
											<button className="expand-button">
												{expandedUser === user.id ? '▲' : '▼'}
											</button>
										</td>
									</tr>
									{expandedUser === user.id && (
										<tr className="user-detail-row">
											<td colSpan="4">
												{editingUser === user.id ? (
													<form onSubmit={handleUpdateUser} className="edit-user-form">
														<p>Edytujesz użytkownika: <strong>{user.username}</strong></p>
														<div>
															<label>Nazwa użytkownika:</label>
															<input
																type="text"
																name="username"
																value={editFormData.username}
																onChange={handleEditFormChange}
																required
															/>
														</div>
														<div>
															<label>Imię:</label>
															<input
																type="text"
																name="first_name"
																value={editFormData.first_name}
																onChange={handleEditFormChange}
															/>
														</div>
														<div>
															<label>Nazwisko:</label>
															<input
																type="text"
																name="last_name"
																value={editFormData.last_name}
																onChange={handleEditFormChange}
															/>
														</div>
														<div>
															<label>Email:</label>
															<input
																type="email"
																name="email"
																value={editFormData.email}
																onChange={handleEditFormChange}
																required
															/>
														</div>
														<div>
															<label>
																<input
																	type="checkbox"
																	name="is_staff"
																	checked={editFormData.is_staff}
																	onChange={handleEditFormChange}
																	disabled={user.is_superuser}
																/>
																Administrator
															</label>
														</div>
														<div>
															<label>
																<input
																	type="checkbox"
																	name="is_superuser"
																	checked={editFormData.is_superuser}
																	onChange={handleEditFormChange}
																	disabled={user.is_superuser}
																/>
																Super Administrator
															</label>
														</div>
														<div className="edit-buttons">
															<button type="submit" className="save-button">Zapisz</button>
															<button type="button" className="cancel-button" onClick={() => setEditingUser(null)}>Anuluj</button>
														</div>
													</form>
												) : (
													<div className="user-details-content">
														<p><strong>ID:</strong> {user.id}</p>
														<p><strong>Nazwa użytkownika:</strong> {user.username}</p>
														<p><strong>Imię:</strong> {user.first_name || 'N/A'}</p>
														<p><strong>Nazwisko:</strong> {user.last_name || 'N/A'}</p>
														<p><strong>Email:</strong> {user.email}</p>
														<p><strong>Rola:</strong> {getUserRole(user)}</p>
														<div className="action-buttons">
															<button
																className="edit-button"
																onClick={() => handleEditClick(user)}
																disabled={user.is_superuser}
															>
																Edytuj
															</button>
															<button
																className="delete-button"
																onClick={() => handleDelete(user.id)}
																disabled={user.is_superuser || user.is_staff}
															>
																Usuń
															</button>
														</div>
													</div>
												)}
											</td>
										</tr>
									)}
								</React.Fragment>
							))
						) : (
							<tr>
								<td colSpan="4">Brak użytkowników do wyświetlenia.</td>
							</tr>
						)}
					</tbody>
				</table>
			</div>
		</div>
	);
}

export default Admin;