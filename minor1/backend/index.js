const express = require('express');
const bodyParser = require('body-parser');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const port = 4000; // Backend running on port 5000

// Middleware
app.use(cors({ 
  origin: 'http://localhost:3000', 
  methods: ['GET', 'POST', 'OPTIONS'], 
  credentials: true 
}));

app.use(bodyParser.json()); // To parse incoming JSON requests

// PostgreSQL Connection
const pool = new Pool({
  user: 'postgres',  // Replace with your PostgreSQL username
  host: 'localhost',
  database: 'quickcare',  // Replace with your database name
  password: 'tiger',  // Replace with your password
  port: 5432, // Default PostgreSQL port
});

// Preflight CORS handler
app.options('*', (req, res) => {
  res.set('Access-Control-Allow-Origin', 'http://localhost:3000');
  res.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.set('Access-Control-Allow-Headers', 'Content-Type');
  res.set('Access-Control-Allow-Credentials', 'true');
  res.status(200).send();
});

// Route to save patient data
app.post('/api/patients', async (req, res) => {
  const { name, age, weight, height, bloodPressure, medicalHistory } = req.body;

  if (!name || !age || !weight || !height || !bloodPressure || !medicalHistory) {
    return res.status(400).send({ error: 'All fields are required.' });
  }

  try {
    const query = `
      INSERT INTO patients (name, age, weight, height, blood_pressure, medical_history)
      VALUES ($1, $2, $3, $4, $5, $6)
    `;
    await pool.query(query, [name, age, weight, height, bloodPressure, medicalHistory]);
    res.status(201).send({ message: 'Patient data saved successfully!' });
  } catch (error) {
    console.error('Error saving patient data:', error);
    res.status(500).send({ error: 'Internal Server Error' });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
