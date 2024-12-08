"use client";

import { useState } from 'react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<string[]>([]);
  const [noResults, setNoResults] = useState(false);

  const handleSearch = async () => {
    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const urls: string[] = await response.json();
      setResults(urls);
      setNoResults(urls.length === 0);
    } catch (error) {
      console.error('Error fetching search results:', error);
    }
  };

  return (
    <div style={{
      textAlign: 'center',
      padding: '20px',
      fontFamily: 'Arial, sans-serif',
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
    }}>
      {/* Large logo */}
      <div
        style={{
          fontSize: '80px',
          fontWeight: 'bold',
          background: 'linear-gradient(90deg, red, orange, yellow, green, blue, indigo, violet)',
          WebkitBackgroundClip: 'text',
          color: 'transparent',
          marginBottom: '30px',
          cursor: 'pointer',
        }}
        onClick={() => window.location.reload()}
      >
        Goober
      </div>

      {/* Search bar */}
      <div style={{
        marginBottom: '50px',
        width: '50vw',
        position: 'relative',
      }}>
        <input
          type="text"
          placeholder="Type your search here..."
          style={{
            width: '100%',
            padding: '10px 40px 10px 15px',
            fontSize: '16px',
            color: 'black',
            border: '1px solid black',
            borderRadius: '16px',
          }}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
        />
        <i
          className="fas fa-search"
          onClick={handleSearch}
          style={{
            position: 'absolute',
            right: '15px',
            top: '50%',
            transform: 'translateY(-50%)',
            cursor: 'pointer',
            color: '#555',
          }}
        />
      </div>

      {/* Results */}
      <div>
        {noResults && (
          <div>
            <p style={{ fontSize: '18px', color: '#777' }}>No results found, empathy cookie for you!</p>
            {/* Uncomment if you want to show the cookie image */}
            {/* <img
              src="/static/images/cookie.jpg"
              alt="Empathy Cookie"
              style={{ width: '200px', height: '200px', objectFit: 'contain' }}
            /> */}
          </div>
        )}
        {results.map((url, index) => (
          <div
            key={index}
            style={{
              width: '50vw',
              padding: '10px',
              margin: '10px auto',
              border: '1px solid #ccc',
              borderRadius: '5px',
              backgroundColor: '#f9f9f9',
              textAlign: 'left',
            }}
          >
            <strong>{index + 1}. </strong>
            <a href={url} target="_blank" rel="noopener noreferrer" style={{ color: '#007BFF' }}>
              {url}
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}
