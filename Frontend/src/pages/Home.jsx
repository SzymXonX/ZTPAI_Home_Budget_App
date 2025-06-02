import { use, useEffect, useState, useCallback } from 'react';
import api from "../api";

import useTimedMessage from '../hooks/useTimedMessage';
import "../styles/Home.css";


function Home() {
  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth() + 1);
  const [expenses, setExpenses] = useState([]);
  const [incomes, setIncomes] = useState([]);
  const [expandedTransaction, setExpandedTransaction] = useState({ type: null, id: null });
  const [categories, setCategories] = useState({ expenses: [], incomes: [] });
  const [formData, setFormData] = useState({
    date: today.toISOString().split('T')[0],
    amount: '',
    category: '',
    description: '',
    type: 'expense'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formError, setFormError] = useTimedMessage('');
  const [formSuccess, setFormSuccess] = useTimedMessage('');

  const [summary, setSummary] = useState({ total_income: 0, total_expense: 0, balance: 0 });

  document.title = "Home";

  const fetchSummaryData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const API_URL = `/api/categories/summary/${year}/${month}/`;
      const response = await api.get(API_URL);
      setSummary(response.data);
    } catch (err) {
      console.error("Błąd podczas pobierania podsumowania:", err);
      if (err.response && err.response.status === 404) {
        setSummary({ total_income: 0, total_expense: 0, balance: 0 });
      } else {
        setError("Nie udało się załadować podsumowania. Spróbuj ponownie.");
        setSummary({ total_income: 0, total_expense: 0, balance: 0 });
      }
    } finally {
      setLoading(false);
    }
  }, [year, month, setSummary, setLoading, setError]);

  useEffect(() => {
    fetchSummaryData();
  }, [fetchSummaryData]);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response1 = await api.get('/api/expenses/categories/');
        const response2 = await api.get('/api/incomes/categories/');
        setCategories({ expenses: response1.data, incomes: response2.data });
      } catch (err) {
        console.error("Błąd podczas pobierania kategorii:", err);
        setError("Nie udało się załadować kategorii. Spróbuj ponownie.");
      }
    };

    fetchCategories();
  }, []);

  const handleTypeChange = (newType) => {
    setFormData(prevFormData => ({
      ...prevFormData, 
      type: newType,
      category: '',
    }));
  };

  const handleMonthChange = (direction) => {
    const newDate = new Date(year, month - 1 + direction);
    setMonth(newDate.getMonth() + 1);
    setYear(newDate.getFullYear());
  };

  const handleAddTransaction = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setFormError('');
    setFormSuccess('');
    try {
      const transactionData = {
        date: formData.date,
        amount: parseFloat(formData.amount),
        category: formData.category,
        description: formData.description,
      };

      let response;
      if (formData.type === 'expense') {
        response = await api.post('/api/expenses/', transactionData);
      } else if (formData.type === 'income') {
        response = await api.post('/api/incomes/', transactionData);
      } else {
        setFormError("Nieprawidłowy typ transakcji.");
        setLoading(false);
        return;
      }

      setFormData({
        date: today.toISOString().split('T')[0],
        amount: '',
        category: '',
        description: '',
        type: formData.type 
      });

      await fetchSummaryData();
      await fetchTransactionsData();

    } catch (err) {
      setFormError("Błąd podczas dodawania transakcji:", err);
      if (err.response) {
        setFormError(`Błąd: ${err.response.data.detail || JSON.stringify(err.response.data)}`);
      } else if (err.request) {
        setFormError("Brak odpowiedzi z serwera. Sprawdź połączenie.");
      } else {
        setFormError("Wystąpił nieoczekiwany błąd.");
      }
    } finally {
      setLoading(false);
      if (!formError) {
        setFormSuccess("Transakcja została pomyślnie dodana.");
      }
    }
  };

  const fetchTransactionsData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const expensesResponse = await api.get(`/api/expenses/${year}/${month}/`);
      setExpenses(expensesResponse.data);

      const incomesResponse = await api.get(`/api/incomes/${year}/${month}/`);
      setIncomes(incomesResponse.data);

    } catch (err) {
      console.error("Błąd podczas pobierania transakcji:", err);
      if (err.response && err.response.status === 404) {
        setExpenses([]);
        setIncomes([]);
      } else {
        setError("Nie udało się załadować transakcji. Spróbuj ponownie.");
        setExpenses([]);
        setIncomes([]);
      }
    } finally {
      setLoading(false);
    }
  }, [year, month, setExpenses, setIncomes, setLoading, setError]);

  useEffect(() => {
    fetchTransactionsData();
  }, [fetchTransactionsData]);

  const toggleTransactionDetails = (idToToggle, typeOfTransaction) => {
    if (expandedTransaction.type === typeOfTransaction && expandedTransaction.id === idToToggle) {
      setExpandedTransaction({ type: null, id: null });
    } else {
      setExpandedTransaction({ type: typeOfTransaction, id: idToToggle });
    }
  };

  const deleteTransaction = useCallback(async (e, id, type) => {
    e.stopPropagation();

    setLoading(true);
    setError(null);
    setFormError('');
    setFormSuccess('');
    try {
    const API_URL = type === 'expense' 
      ? `/api/expenses/delete/${id}/` 
      : `/api/incomes/delete/${id}/`;
    
    await api.delete(API_URL);
    await fetchTransactionsData();
    await fetchSummaryData();

    } catch (err) {
      console.error("Błąd podczas usuwania transakcji:", err);
      setFormError("Nie udało się usunąć transakcji. Spróbuj ponownie.");
      if (err.response) {
        console.error("Odpowiedź serwera:", err.response.data);
      }
    } finally {
      setLoading(false);
      if (!formError) {
        setFormSuccess("Transakcja została pomyślnie usunięta.");
      }
    }
  }, [fetchTransactionsData, fetchSummaryData, setLoading, setError]);

  return (
    <div className="main-app-content">
      {formError && <p className="error-message">{formError}</p>}
      {formSuccess && <p className="success-message">{formSuccess}</p>}
      <div className="dashboard-container">
        <div className="dashboard-row">
          <div className="summary-container">
            <div className="date-selector">
              <button onClick={() => handleMonthChange(-1)}>&lt;</button>
              <span>{`${year} ${new Date(year, month - 1).toLocaleString('pl-PL', { month: 'long' })}`}</span>
              <button onClick={() => handleMonthChange(1)}>&gt;</button>
            </div>

            <div className="summary-items">
              <div className="summary-item">
                <span id='total_expense'>wydatki</span>
                <input readOnly value={`- ${summary.total_expense} zł`} />
              </div>
              <div className="summary-item">
                <span id='total_income'>przychody</span>
                <input readOnly value={`${summary.total_income} zł`} />
              </div>
              <div className="summary-item">
                <span id='total_balance'>budżet</span>
                <input readOnly value={`${summary.balance} zł`} />
              </div>
            </div>
          </div>

          <form className="add_transaction_form" onSubmit={handleAddTransaction}>
            <div className="add_transaction_content">
              <div className="form_header">
                <button type="button" onClick={() => handleTypeChange('expense')} className={formData.type === 'expense' ? 'active' : ''}>wydatek</button>
                <button type="button" onClick={() => handleTypeChange('income')} className={formData.type === 'income' ? 'active' : ''}>przychód</button>
              </div>
              <div className="form_row">
                <div className="form_group">
                  <label>data</label>
                  <input
                    type="date"
                    name="date"
                    value={formData.date || today.toISOString().split('T')[0]}
                    onChange={e => setFormData({ ...formData, date: e.target.value })}
                    required
                  />
                </div>

                <div className="form_group">
                  <label>kwota</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.amount}
                    onChange={e => setFormData({ ...formData, amount: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="form_group">
                <label>kategoria</label>
                <select
                  value={formData.category}
                  onChange={e => setFormData({ ...formData, category: e.target.value })}
                  required
                >
                  <option value=""></option>
                  {(formData.type === 'expense' ? categories.expenses : categories.incomes).map(cat => (
                    <option key={cat.id} value={cat.id}>{cat.category}</option>
                  ))}
                </select>
              </div>

              <div className="form_group description">
                <label>opis</label>
                <textarea
                  type="text"
                  value={formData.description}
                  onChange={e => setFormData({ ...formData, description: e.target.value })}
                />
              </div>

              <button type="submit">dodaj</button>
            </div>
          </form>
        </div>
        <div className="dashboard-row">
          <div className="expenses-container">
            <h2 className="section-title" id='expenses-title'>wydatki</h2>
            <div className="transactions-list" id="expenses-list">
              {expenses.length > 0 ? (expenses.map(expense => (
                <div className="transaction" key={expense.id} onClick={() => toggleTransactionDetails(expense.id, 'expense')} >
                  <div className="transaction-summary-row">
                    <span className="transaction-category">
                      {expense.category_name}
                    </span>
                    <span className="transaction-amount negative">
                      - {Number(expense.amount).toFixed(2).replace('.', ',')} zł
                    </span>
                  </div>
                  <span className="transaction-date">
                    {new Date(expense.date).toLocaleDateString('pl-PL')}
                  </span>
                  {expandedTransaction.type === 'expense' && expandedTransaction.id === expense.id && (
                    <div className="transaction-details visible"> 
                      <textarea className="transaction-description" disabled value={expense.description}></textarea>
                      <button className="delete-button" onClick={(e) => deleteTransaction(e, expense.id, 'expense')} >
                        Usuń
                      </button>
                    </div>
                  )}
                </div>
              ))) : (<p className="no-transactions">Brak wydatków w tym miesiącu.</p>)
              }
            </div>
          </div>
          <div className="incomes-container">
            <h2 className="section-title" id='incomes-title'>przychody</h2>
            <div className="transactions-list" id="income-list">
              {incomes.length > 0 ? (incomes.map(income => (
                <div className="transaction" key={income.id} onClick={() => toggleTransactionDetails(income.id, 'income')} >
                  <div className="transaction-summary-row">
                    <span className="transaction-category">
                      {income.category_name}
                    </span>
                    <span className="transaction-amount positive">
                      + {Number(income.amount).toFixed(2).replace('.', ',')} zł
                    </span>
                  </div>
                  <span className="transaction-date">
                    {new Date(income.date).toLocaleDateString('pl-PL')}
                  </span>
                  {expandedTransaction.type === 'income' && expandedTransaction.id === income.id && (
                    <div className="transaction-details visible">
                      <textarea className="transaction-description" disabled value={income.description}></textarea>
                      <button className="delete-button" onClick={(e) => deleteTransaction(e, income.id, 'income')}>
                        Usuń
                      </button>
                    </div>
                  )}
                </div>
              ))) : (<p className="no-transactions">Brak przychodów w tym miesiącu.</p>)
              }
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
