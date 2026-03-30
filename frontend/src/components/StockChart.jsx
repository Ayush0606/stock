import React, { useState, useEffect } from 'react'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import './StockChart.css'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

function StockChart({ symbol, days }) {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchData()
  }, [symbol, days])

  const fetchData = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`/api/data/${symbol}?days=${days}`)
      if (response.ok) {
        const stockData = await response.json()
        prepareChartData(stockData)
      } else {
        setError('Failed to fetch stock data')
      }
    } catch (err) {
      setError('Error loading data: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const prepareChartData = (stockData) => {
    const sortedData = [...stockData].sort((a, b) => new Date(a.date) - new Date(b.date))
    
    const labels = sortedData.map(d => new Date(d.date).toLocaleDateString())
    const closePrices = sortedData.map(d => d.close_price)
    const movingAvg = sortedData.map(d => d.moving_avg_7)

    setData({
      labels,
      datasets: [
        {
          label: 'Close Price',
          data: closePrices,
          borderColor: '#667eea',
          backgroundColor: 'rgba(102, 126, 234, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.4,
          pointRadius: 2,
          pointBackgroundColor: '#667eea',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
        },
        {
          label: '7-Day Moving Average',
          data: movingAvg,
          borderColor: '#764ba2',
          borderWidth: 2,
          borderDash: [5, 5],
          fill: false,
          tension: 0.4,
          pointRadius: 0,
        }
      ]
    })
  }

  if (loading) return <div className="chart-container"><p>Loading chart...</p></div>
  if (error) return <div className="chart-container error"><p>{error}</p></div>
  if (!data) return <div className="chart-container"><p>No data available</p></div>

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 15,
          font: {
            size: 12,
            weight: '500'
          }
        }
      },
      title: {
        display: true,
        text: `${symbol} - Price Trend`,
        font: {
          size: 14,
          weight: '600'
        },
        padding: {
          top: 10,
          bottom: 20
        }
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 12,
        titleFont: {
          size: 12,
          weight: '600'
        },
        bodyFont: {
          size: 11
        },
        borderColor: '#ddd',
        borderWidth: 1
      }
    },
    scales: {
      y: {
        title: {
          display: true,
          text: 'Price (INR)',
          font: {
            weight: '600'
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Date',
          font: {
            weight: '600'
          }
        },
        grid: {
          display: false
        }
      }
    }
  }

  return (
    <div className="chart-wrapper">
      <Line data={data} options={options} />
    </div>
  )
}

export default StockChart
