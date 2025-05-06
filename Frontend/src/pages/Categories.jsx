import { useEffect, useState } from 'react';
import api from "../api";

function Categories() {
    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
      api.get('/api/incomes/categories/')
        .then((response) => {
          setCategories(response.data);
          setLoading(false);
        })
        .catch((error) => {
          console.error('Błąd przy pobieraniu kategorii:', error);
          setLoading(false);
        });
    }, []);
  
    if (loading) return <p>Ładowanie kategorii...</p>;
  
    return (
      <div>
        <h2>Kategorie przychodów</h2>
        <ul>
          {categories.map((cat) => (
            <li key={cat.id}>{cat.category}</li>
          ))}
        </ul>
      </div>
    );
  }

export default Categories;