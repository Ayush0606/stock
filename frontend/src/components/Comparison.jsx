import React, { useState } from 'react'
import './Comparison.css'

function Comparison({ symbol1, defaultSymbol2 }) {
  const [symbol2, setSymbol2] = useState(defaultSymbol2)
  const [comparison, setComparison] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  const availableSymbols = ['INFY.NS', 'TCS.NS', 'RELIANCE.NS']
  const otherSymbols = availableSymbols.filter(s => s !== symbol1)

  const handleCompare = async () => {
    if (!symbol2) {
      setError('Please select a symbol')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`/api/compare?symbol1=${symbol1}&symbol2=${symbol2}`)
      if (response.ok) {
        const data = await response.json()
        setComparison(data)
      } else {
        setError('Failed to compare stocks')
      }
    } catch (err) {
      setError('Error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="comparison-container">
      <h2>🔄 Compare Stocks</h2>
      
      <div className="comparison-controls">
        <div className="comparison-input">
          <label>vs</label>
          <select
            value={symbol2}
            onChange={(e) => setSymbol2(e.target.value)}
          >
            <option value="">Select a stock</option>
            {otherSymbols.map(symbol => (
              <option key={symbol} value={symbol}>{symbol}</option>
            ))}
          </select>
        </div>
        <button 
          className="compare-button"
          onClick={handleCompare}
          disabled={loading}
        >
          {loading ? 'Comparing...' : 'Compare'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {comparison && (
        <div className="comparison-result">
          <div className="comparison-item">
            <h3>{comparison.symbol1}</h3>
            <div className="metric">
              <span>Total Returns</span>
              <span className={comparison.symbol1_returns > 0 ? 'positive' : 'negative'}>
                {comparison.symbol1_returns > 0 ? '+' : ''}{comparison.symbol1_returns}%
              </span>
            </div>
          </div>

          <div className="comparison-divider">vs</div>

          <div className="comparison-item">
            <h3>{comparison.symbol2}</h3>
            <div className="metric">
              <span>Total Returns</span>
              <span className={comparison.symbol2_returns > 0 ? 'positive' : 'negative'}>
                {comparison.symbol2_returns > 0 ? '+' : ''}{comparison.symbol2_returns}%
              </span>
            </div>
          </div>

          <div className="comparison-stats">
            <div className="stat">
              <span>Correlation</span>
              <span>{comparison.correlation}</span>
            </div>
            <div className="stat">
              <span>Better Performer</span>
              <span>{comparison.better_performer}</span>
            </div>
            <div className="stat">
              <span>Data Points</span>
              <span>{comparison.data_points}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Comparison
