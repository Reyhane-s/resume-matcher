import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [skills, setSkills] = useState('');
  const [ageRange, setAgeRange] = useState('25,45');
  const [degree, setDegree] = useState('bachelor');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const [minAge, maxAge] = ageRange.split(',').map(Number);
      const response = await axios.post('http://127.0.0.1:8000/match/', {
        required_skills: skills.split(',').map(skill => skill.trim()),
        required_age_range: [minAge, maxAge],
        required_degree: degree,
        resumes: [] // در واقعیت اینجا رزومه‌هایتان را از دیتابیس فراخوانی کنید
      });
      setResults(response.data.matches);
    } catch (error) {
      console.error("Error fetching matches:", error);
    }
  };

  return (
    <div className="App">
      <h1>Resume Matcher</h1>
      <input
        type="text"
        placeholder="Skills (comma separated)"
        value={skills}
        onChange={e => setSkills(e.target.value)}
      />
      <input
        type="text"
        placeholder="Age Range (e.g., 25,45)"
        value={ageRange}
        onChange={e => setAgeRange(e.target.value)}
      />
      <input
        type="text"
        placeholder="Required Degree"
        value={degree}
        onChange={e => setDegree(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>
      <div>
        <h2>Top Matches</h2>
        <ul>
          {results.map((result, index) => (
            <li key={index}>{result.skills.join(', ')} - Score: {result.score}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
