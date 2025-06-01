import { use, useEffect, useState } from 'react';
import api from "../api";

import useTimedMessage from '../hooks/useTimedMessage';
import '../styles/Categories.css'; 

function Categories() {
    const [categories, setCategories] = useState({ expensesCategories: [], incomesCategories: [] });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [formError, setFormError] = useTimedMessage('');
    const [formSuccess, setFormSuccess] = useTimedMessage('');
    const [formData, setFormData] = useState({
      type: 'expense', 
      category: '',
    });

    document.title = "Categories";
  
    useEffect(() => {
      const fetchCategories = async () => {
        try {
          const response1 = await api.get('/api/expenses/categories/');
          const response2 = await api.get('/api/incomes/categories/');
          setCategories({ expensesCategories: response1.data, incomesCategories: response2.data });
        } catch (err) {
          console.error("Błąd podczas pobierania kategorii:", err);
          setError("Nie udało się załadować kategorii. Spróbuj ponownie.");
        } finally {
          setLoading(false);
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

    const addCategory = async (e) => {
      e.preventDefault();
      const { type, category } = formData;

      setFormError('');
      setFormSuccess('');

      if (!category.trim()) {
        setFormError("Nazwa kategorii nie może być pusta.");
        return;
      }

      try {
        const response = await api.post(`/api/${type}s/categories/`, { category });
        setCategories(prevCategories => ({
          ...prevCategories,
          [`${type}sCategories`]: [...prevCategories[`${type}sCategories`], response.data],
        }));
        setFormData({ ...formData, category: '' });
        setFormSuccess(`Kategoria ${category} została dodana.`);
      } catch (err) {
        console.error("Błąd podczas dodawania kategorii:", err);
        setFormError("Nie udało się dodać kategorii. Spróbuj ponownie.");
      }
    }

    const deleteCategory = async (e, id, type) => {
      e.preventDefault();
      setFormError('');
      setFormSuccess('');
      if (!window.confirm("Czy na pewno chcesz usunąć tę kategorię?\nWszystkie transakcje przypisane do tej kategorii zostaną usunięte!!!!!")) {
        return;
      }

      try {
        await api.delete(`/api/${type}s/categories/delete/${id}/`);
        setCategories(prevCategories => ({
          ...prevCategories,
          [`${type}sCategories`]: prevCategories[`${type}sCategories`].filter(category => category.id !== id),
        }));
        setFormSuccess(`Kategoria została usunięta.`);
      } catch (err) {
        console.error("Błąd podczas usuwania kategorii:", err);
        setFormError("Nie udało się usunąć kategorii. Spróbuj ponownie.");
      }
    }


    
    return (
      <div className='categories-app-content'>
        {formError && <p className="error-message">{formError}</p>}
        {formSuccess && <p className="success-message">{formSuccess}</p>}
        <div className="dashboard-container">
          <div className="dashboard-row">
            <form className="add_category_form" onSubmit={addCategory}>
              <div className="add_category_content">
                <div className="form_header">
                  <button type="button" onClick={() => handleTypeChange('expense')} className={formData.type === 'expense' ? 'active' : ''}>wydatek</button>
                  <button type="button" onClick={() => handleTypeChange('income')} className={formData.type === 'income' ? 'active' : ''}>przychód</button>
                </div>
                <div className="form_group">
                  <label>nazwa kategorii</label>
                  <input
                    type="text"
                    value={formData.category}
                    onChange={e => setFormData({ ...formData, category: e.target.value })}
                    required
                    maxLength={30}
                  />
                </div>
                <button type="submit">dodaj</button>
              </div>
            </form>
          </div>

          <div className="dashboard-row">
            <div className="expenses-category-container">
              <h2 className="section-title" id='expenses-title'>kategorie wydatków</h2>
              <div className="categories-list" id="expenses-list">
                {categories.expensesCategories.length > 0 ? (categories.expensesCategories.map(expense => (
                  <div className="categories" key={expense.id} >
                    <div className="categories-summary-row">
                      <span className="categories-category">
                        {expense.category}
                      </span>
                      <button className="delete-button" onClick={(e) => deleteCategory(e, expense.id, 'expense')} >
                        Usuń
                      </button>
                    </div>
                  </div>
                ))) : (<p className="no-categories">Brak kategorii wydatków.</p>)
                }
              </div>
            </div>
            <div className="incomes-category-container">
              <h2 className="section-title" id='incomes-title'>kategorie przychodów</h2>
              <div className="categories-list" id="income-list">
                {categories.incomesCategories.length > 0 ? (categories.incomesCategories.map(income => (
                  <div className="categories" key={income.id}  >
                    <div className="categories-summary-row">
                      <span className="categories-category">
                        {income.category}
                      </span>
                      <button className="delete-button" onClick={(e) => deleteCategory(e, income.id, 'income')} >
                        Usuń
                      </button>
                    </div>
                  </div>
                ))) : (<p className="no-categories">Brak kategorii przychodów.</p>)
                }
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

export default Categories;