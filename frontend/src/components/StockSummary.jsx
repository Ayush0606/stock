import React, { useState, useEffect } from 'react'
import './StockSummary.css'

function StockSummary({ symbol }) {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchSummary()
  }, [symbol])

  const fetchSummary = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`/api/summary/${symbol}`)
      if (response.ok) {
        const data = await response.json()
        setSummary(data)
      } else {
        setError('Failed to fetch summary')
      }
    } catch (err) {
      setError('Error loading summary: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="summary-container"><p>Loading...</p></div>
  if (error) return <div className="summary-container error"><p>{error}</p></div>
  if (!summary) return <div className="summary-container"><p>No summary available</p></div>

  const formatNumber = (num) => {
    return typeof num === 'number' ? num.toFixed(2) : num
  }

  return (
    <div className="summary-container">
      <h3>📋 Stock Summary</h3>
      <div className="summary-grid">
        <div className="summary-item">
          <div className="summary-label">Current Price</div>
          <div className="summary-value">₹{formatNumber(summary.current_price)}</div>
        </div>
        <div className="summary-item">
          <div className="summary-label">52-Week High</div>
          <div className="summary-value">₹{formatNumber(summary.high_52_week)}</div>
        </div>
        <div className="summary-item">
          <div className="summary-label">52-Week Low</div>
          <div className="summary-value">₹{formatNumber(summary.low_52_week)}</div>
        </div>
        <div className="summary-item">
          <div className="summary-label">Average Close</div>
          <div className="summary-value">₹{formatNumber(summary.average_close)}</div>
        </div>
        <div className="summary-item">
          <div className="summary-label">Volatility</div>
          <div className="summary-value">{formatNumber(summary.volatility)}%</div>
        </div>
        <div className="summary-item">
          <div className="summary-label">Last Updated</div>
          <div className="summary-value">{new Date(summary.last_updated).toLocaleDateString()}</div>
        </div>
      </div>
    </div>
  )
}

export default StockSummary
