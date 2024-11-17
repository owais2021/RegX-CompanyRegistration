import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [companyName, setCompanyName] = useState('');

  const handleRegister = async () => {
    if (companyName) {
      try {
        await axios.post('http://localhost:5000/register', {
          name: companyName,
          industry: 'Tech',
          services: 'Software Development',
          certifications: 'ISO 9001',
        });
        alert('Company registered successfully');
      } catch (error) {
        console.error('Error registering company:', error);
      }
    } else {
      alert('Please enter a company name.');
    }
  };

  return (
    <div>
      <h1>Company Registration</h1>
      <input
        type="text"
        value={companyName}
        onChange={(e) => setCompanyName(e.target.value)}
        placeholder="Enter company name"
      />
      <button onClick={handleRegister}>Register Company</button>
    </div>
  );
}

export default App;
