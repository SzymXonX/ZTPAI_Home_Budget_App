import { useEffect, useState } from 'react';
import api from '../api';

import '../styles/Summary.css';


function Summary() {
  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth() + 1);
  const [categories, setCategories] = useState({ expensesCategories: [], incomesCategories: [] });

  document.title = "Summary";

  const handleMonthChange = (direction) => {
    const newDate = new Date(year, month - 1 + direction);
    setMonth(newDate.getMonth() + 1);
    setYear(newDate.getFullYear());
  };

  const fetchCategories = async () => {
    try {
      const response = await api.get(`/api/categories/summary/${year}/${month}/`);
      setCategories({expensesCategories: response.data.expense_by_category, incomesCategories: response.data.income_by_category});
    } catch (error) {
      console.error("Błąd podczas pobierania kategorii:", error);
    }
  }

  useEffect(() => {
    fetchCategories();
  }, [year, month]);

  return (
    <div className="summary-app-content">
      <div className="dashboard-container">
        <div className="dashboard-row">
          <div className="summary-container" id='summary-container'>
            <div className="date-selector" id='summary-date-selector'>
              <button onClick={() => handleMonthChange(-1)}>&lt;</button>
              <span>{`${year} ${new Date(year, month - 1).toLocaleString('pl-PL', { month: 'long' })}`}</span>
              <button onClick={() => handleMonthChange(1)}>&gt;</button>
            </div>
          </div>
        </div>
        <div className="dashboard-row">
            <div className="expenses-category-container">
              <h2 className="section-title" id='expenses-title'>kategorie wydatków</h2>
              <div className="categories-list" id="expenses-list">
                {Object.keys(categories.expensesCategories).length > 0 ? (
                  Object.entries(categories.expensesCategories).map(([categoryName, amount]) => (
                    <div className="categories" key={categoryName}>
                      <div className="categories-summary-row">
                        <span className="categories-category">
                          {categoryName}
                        </span>
                        <span className="categories-amount negative">
                          - {parseFloat(amount).toFixed(2)}
                        </span>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="no-categories">Brak wydatków dla tego miesiąca.</p>
                )}
              </div>
            </div>
            <div className="incomes-category-container">
              <h2 className="section-title" id='incomes-title'>kategorie przychodów</h2>
              <div className="categories-list" id="income-list">
                {Object.keys(categories.incomesCategories).length > 0 ? (
                  Object.entries(categories.incomesCategories).map(([categoryName, amount]) => (
                    <div className="categories" key={categoryName}>
                      <div className="categories-summary-row">
                        <span className="categories-category">
                          {categoryName}
                        </span>
                        <span className="categories-amount positive">
                          + {parseFloat(amount).toFixed(2)}
                        </span>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="no-categories">Brak przychodów dla tego miesiąca.</p>
                )}
              </div>
            </div>
          </div>
      </div>
    </div>
  );
};

export default Summary;