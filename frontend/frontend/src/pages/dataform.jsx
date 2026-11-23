import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/app.jsx';

export default function DataForm() {
  const [formData, setFormData] = useState({ title: '', description: '' });
  const [status, setStatus] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {,ṁ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('Submitting...');

    try {
      // Update '/items' to match your backend POST endpoint
      await api.post('/items', formData);
      setStatus('Saved successfully!');
      setFormData({ title: '', description: '' }); // Reset form
    } catch (err) {
      setStatus(err.response?.data?.message || 'Error saving data.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', fontFamily: 'sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Submit Data</h2>
        <button onClick={handleLogout} style={{ padding: '5px 10px' }}>Logout</button>
      </div>

      {status && <p>{status}</p>}

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <input
          type="text"
          name="title"
          placeholder="Title"
          value={formData.title}
          onChange={handleChange}
          required
          style={{ padding: '8px' }}
        />
        <textarea
          name="description"
          placeholder="Description"
          value={formData.description}
          onChange={handleChange}
          rows="4"
          required
          style={{ padding: '8px' }}
        />
        <button type="submit" style={{ padding: '10px', cursor: 'pointer' }}>
          Submit
        </button>
      </form>
    </div>
  );
}
