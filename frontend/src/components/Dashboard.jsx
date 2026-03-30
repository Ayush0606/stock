import React, { useState, useEffect } from 'react'
import StockChart from './StockChart'
import StockSummary from './StockSummary'
import Comparison from './Comparison'
import Prediction from './Prediction'
import './Dashboard.css'

function Dashboard({ selectedSymbol }) {
  const [days, setDays] = useState(30)
  const [compare, setCompare] = useState({ symbol1: 'INFY.NS', symbol2: 'TCS.NS', show: false })
  const [activeTab, setActiveTab] = useState('overview')

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>📊 {selectedSymbol}</h1>
        <div className="controls">
          <div className="control-group">
            <label htmlFor="days">Days:</label>
            <select 
              id="days"
              value={days} 
              onChange={(e) => setDays(Number(e.target.value))}
            >
              <option value={30}>30 days</option>
              <option value={90}>90 days</option>
              <option value={180}>180 days</option>
              <option value={365}>1 year</option>
            </select>
          </div>
        </div>
      </div>

      <div className="tabs">
        <button 
          className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📈 Overview
        </button>
        <button 
          className={`tab-button ${activeTab === 'compare' ? 'active' : ''}`}
          onClick={() => setActiveTab('compare')}
        >
          🔄 Compare
        </button>
        <button 
          className={`tab-button ${activeTab === 'predict' ? 'active' : ''}`}
          onClick={() => setActiveTab('predict')}
        >
          🎯 Predict
        </button>
      </div>

      {activeTab === 'overview' && (
        <div className="tab-content">
          <div className="content-row">
            <div className="content-col">
              <StockChart symbol={selectedSymbol} days={days} />
            </div>
          </div>
          <div className="content-row">
            <div className="content-col">
              <StockSummary symbol={selectedSymbol} />
            </div>
          </div>
        </div>
      )}

      {activeTab === 'compare' && (
        <div className="tab-content">
          <Comparison symbol1={selectedSymbol} defaultSymbol2="TCS.NS" />
        </div>
      )}

      {activeTab === 'predict' && (
        <div className="tab-content">
          <Prediction symbol={selectedSymbol} />
        </div>
      )}
    </div>
  )
}

export default Dashboard
