import { useEffect, useState } from 'react';
import api from "../api";

import "../styles/Home.css";

function Home() {
  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth() + 1);
  const [expenses, setExpenses] = useState([]);
  const [incomes, setIncomes] = useState([]);
  const [categories, setCategories] = useState({ expenses: [], incomes: [] });
  const [formData, setFormData] = useState({
    amount: '',
    category: '',
    description: '',
    type: 'expense'
  });
  const [summary, setSummary] = useState({ total_income: 0, total_expense: 0, balance: 0 });

  useEffect(() => {
    fetchData();
  }, [month, year]);

  const fetchData = async () => {
    try {
      const [expensesRes, incomesRes, summaryRes, categoriesRes] = await Promise.all([
        axios.get(`/api/expenses/?month=${month}&year=${year}`),
        axios.get(`/api/incomes/?month=${month}&year=${year}`),
        axios.get(`/api/summary/?month=${month}&year=${year}`),
        axios.get('/api/categories/')
      ]);

      setExpenses(expensesRes.data);
      setIncomes(incomesRes.data);
      setSummary(summaryRes.data);
      setCategories(categoriesRes.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleMonthChange = (direction) => {
    const newDate = new Date(year, month - 1 + direction);
    setMonth(newDate.getMonth() + 1);
    setYear(newDate.getFullYear());
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const endpoint = formData.type === 'expense' ? '/api/expenses/' : '/api/incomes/';
    try {
      await axios.post(endpoint, {
        ...formData,
        date: `${year}-${String(month).padStart(2, '0')}-01T00:00:00Z`
      });
      fetchData();
      setFormData({ amount: '', category: '', description: '', type: formData.type });
    } catch (error) {
      console.error(error);
    }
  };

  const handleDelete = async (id, type) => {
    try {
      await axios.delete(`/api/${type === 'expense' ? 'expenses' : 'incomes'}/${id}/`);
      fetchData();
    } catch (error) {
      console.error(error);
    }
  };

  return (
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
              <span>wydatki</span>
              <input readOnly value={`${summary.total_expense.toFixed(2)} zł`} />
            </div>
            <div className="summary-item">
              <span>przychody</span>
              <input readOnly value={`${summary.total_income.toFixed(2)} zł`} />
            </div>
            <div className="summary-item">
              <span>budżet</span>
              <input readOnly value={`${summary.balance.toFixed(2)} zł`} />
            </div>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="form-container">
          <div className="form-content">
            <div className="form-row">
              <div className="form-header">
                <button type="button" onClick={() => setFormData({ ...formData, type: 'expense' })} className={formData.type === 'expense' ? 'active' : ''}>wydatek</button>
                <button type="button" onClick={() => setFormData({ ...formData, type: 'income' })} className={formData.type === 'income' ? 'active' : ''}>przychód</button>
              </div>

              <div className="form-group">
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

            <div className="form-group">
              <label>Kategoria</label>
              <select
                value={formData.category}
                onChange={e => setFormData({ ...formData, category: e.target.value })}
              >
                {(formData.type === 'expense' ? categories.expenses : categories.incomes).map(cat => (
                  <option key={cat.id} value={cat.id}>{cat.category}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>opis</label>
              <input
                type="text"
                value={formData.description}
                onChange={e => setFormData({ ...formData, description: e.target.value })}
              />
            </div>

            <button type="submit">dodaj</button>
          </div>
        </form>
      </div>

      <div className="transactions-container">
        <div className="expenses-container">
          <h2>Wydatki</h2>
          <div className="transactions-list">
            {expenses.length > 0 ? expenses.map(exp => (
              <div className="transaction" key={exp.id}>
                <span>{exp.category_name || exp.category}</span>
                <span className="negative">-{Number(exp.amount).toFixed(2)} zł</span>
                <span>{new Date(exp.date).toLocaleDateString()}</span>
                <div className="transaction-details">
                  <p>{exp.description}</p>
                  <button onClick={() => handleDelete(exp.id, 'expense')}>Usuń</button>
                </div>
              </div>
            )) : <p>Brak wydatków w tym miesiącu.</p>}
          </div>
        </div>

        <div className="incomes-container">
          <h2>Przychody</h2>
          <div className="transactions-list">
            {incomes.length > 0 ? incomes.map(inc => (
              <div className="transaction" key={inc.id}>
                <span>{inc.category_name || inc.category}</span>
                <span className="positive">+{Number(inc.amount).toFixed(2)} zł</span>
                <span>{new Date(inc.date).toLocaleDateString()}</span>
                <div className="transaction-details">
                  <p>{inc.description}</p>
                  <button onClick={() => handleDelete(inc.id, 'income')}>Usuń</button>
                </div>
              </div>
            )) : <p>Brak przychodów w tym miesiącu.</p>}
          </div>
        </div>
      </div>
    </div>
  );
};


export default Home;
