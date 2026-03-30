import React, { useState } from 'react'
import './Prediction.css'

function Prediction({ symbol }) {
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handlePredict = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`/api/predict/${symbol}`)
      if (response.ok) {
        const data = await response.json()
        setPrediction(data)
      } else {
        setError('Failed to generate prediction')
      }
    } catch (err) {
      setError('Error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const getTrendEmoji = (trend) => {
    switch(trend) {
      case 'UP': return '📈'
      case 'DOWN': return '📉'
      default: return '➡️'
    }
  }

  const getTrendColor = (trend) => {
    switch(trend) {
      case 'UP': return '#4caf50'
      case 'DOWN': return '#d32f2f'
      default: return '#ff9800'
    }
  }

  return (
    <div className="prediction-container">
      <h2>🎯 Price Prediction</h2>
      <p className="description">
        Using linear regression to predict the next day's closing price based on historical data.
      </p>

      <button 
        className="predict-button"
        onClick={handlePredict}
        disabled={loading}
      >
        {loading ? 'Generating Prediction...' : 'Get Prediction'}
      </button>

      {error && <div className="error-message">{error}</div>}

      {prediction && (
        <div className="prediction-result">
          <div className="prediction-header">
            <h3>{prediction.symbol}</h3>
            <div className="trend-badge" style={{ borderColor: getTrendColor(prediction.trend) }}>
              <span className="trend-emoji">{getTrendEmoji(prediction.trend)}</span>
              <span className="trend-text">{prediction.trend}</span>
            </div>
          </div>

          <div className="prediction-grid">
            <div className="prediction-item">
              <span className="prediction-label">Base Price (Current)</span>
              <span className="prediction-value">₹{prediction.base_price.toFixed(2)}</span>
            </div>
            <div className="prediction-item">
              <span className="prediction-label">Predicted Price (Next Day)</span>
              <span className="prediction-value">₹{prediction.next_day_prediction.toFixed(2)}</span>
            </div>
            <div className="prediction-item">
              <span className="prediction-label">Confidence Level</span>
              <span className="prediction-value">{(prediction.confidence * 100).toFixed(2)}%</span>
            </div>
            <div className="prediction-item">
              <span className="prediction-label">Predicted Change</span>
              <span className="prediction-value" style={{ color: getTrendColor(prediction.trend) }}>
                {((prediction.next_day_prediction - prediction.base_price) / prediction.base_price * 100).toFixed(2)}%
              </span>
            </div>
          </div>

          <div className="prediction-note">
            <p>💡 Note: This prediction is based on historical trends and linear regression. Use it as a reference, not as financial advice.</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default Prediction
