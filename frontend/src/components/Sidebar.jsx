import React, { useState } from 'react'
import './Sidebar.css'

function Sidebar({ companies, selectedSymbol, onSelectSymbol, loading, darkMode, onToggleDarkMode }) {
  const [searchTerm, setSearchTerm] = useState('')

  const filteredCompanies = companies.filter(company =>
    company.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (company.name && company.name.toLowerCase().includes(searchTerm.toLowerCase()))
  )

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="header-top">
          <h2>📈 Stock Dashboard</h2>
          <button 
            className="dark-mode-toggle"
            onClick={onToggleDarkMode}
            title={darkMode ? 'Light mode' : 'Dark mode'}
          >
            {darkMode ? '☀️' : '🌙'}
          </button>
        </div>
        <p>v1.0.0</p>
      </div>

      <div className="search-box">
        <input
          type="text"
          placeholder="🔍 Search stocks..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="companies-section">
        <h3>Available Companies</h3>
        {loading ? (
          <p className="loading-text">Loading...</p>
        ) : filteredCompanies.length === 0 ? (
          <p className="no-results">No companies found</p>
        ) : (
          <div className="companies-list">
            {filteredCompanies.map(company => (
              <button
                key={company.symbol}
                className={`company-item ${selectedSymbol === company.symbol ? 'active' : ''}`}
                onClick={() => onSelectSymbol(company.symbol)}
              >
                <div className="company-symbol">{company.symbol}</div>
                <div className="company-name">{company.name}</div>
                <div className="company-count">{company.data_points} points</div>
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="sidebar-footer">
        <p>💡 Click on a company to view details</p>
      </div>
    </aside>
  )
}

export default Sidebar
