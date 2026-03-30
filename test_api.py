"""
Example usage and testing of the Stock Data Intelligence Dashboard
"""

import requests
from datetime import datetime
import json

# Configuration
BASE_URL = "http://localhost:8000/api"
TEST_SYMBOLS = ["INFY.NS", "TCS.NS", "RELIANCE.NS"]


def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_health():
    """Test health endpoint"""
    print_header("Testing Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_get_companies():
    """Test get companies endpoint"""
    print_header("Testing Get Companies")
    try:
        response = requests.get(f"{BASE_URL}/companies")
        companies = response.json()
        print(f"Found {len(companies)} companies:")
        for company in companies:
            print(f"  - {company['symbol']}: {company['name']} ({company['data_points']} data points)")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_get_stock_data():
    """Test get stock data endpoint"""
    print_header("Testing Get Stock Data")
    try:
        symbol = TEST_SYMBOLS[0]
        response = requests.get(f"{BASE_URL}/data/{symbol}", params={"days": 30})
        data = response.json()
        print(f"Fetched data for {symbol}:")
        print(f"  Total records: {len(data)}")
        if data:
            print(f"  First record: {data[0]}")
            print(f"  Latest record: {data[-1]}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_get_summary():
    """Test get summary endpoint"""
    print_header("Testing Get Summary")
    try:
        for symbol in TEST_SYMBOLS:
            response = requests.get(f"{BASE_URL}/summary/{symbol}")
            summary = response.json()
            print(f"\n{symbol} Summary:")
            print(f"  Current Price: ₹{summary['current_price']:.2f}")
            print(f"  52-Week High: ₹{summary['high_52_week']:.2f}")
            print(f"  52-Week Low: ₹{summary['low_52_week']:.2f}")
            print(f"  Average Close: ₹{summary['average_close']:.2f}")
            print(f"  Volatility: {summary['volatility']:.2f}%")
            print(f"  Last Updated: {summary['last_updated']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_compare_stocks():
    """Test compare stocks endpoint"""
    print_header("Testing Compare Stocks")
    try:
        symbol1, symbol2 = TEST_SYMBOLS[0], TEST_SYMBOLS[1]
        response = requests.get(
            f"{BASE_URL}/compare",
            params={"symbol1": symbol1, "symbol2": symbol2}
        )
        comparison = response.json()
        print(f"Comparing {symbol1} vs {symbol2}:")
        print(f"  {symbol1} Returns: {comparison['symbol1_returns']:.2f}%")
        print(f"  {symbol2} Returns: {comparison['symbol2_returns']:.2f}%")
        print(f"  Correlation: {comparison['correlation']:.4f}")
        print(f"  Better Performer: {comparison['better_performer']}")
        print(f"  Common Data Points: {comparison['data_points']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_predict_price():
    """Test price prediction endpoint"""
    print_header("Testing Price Prediction")
    try:
        for symbol in TEST_SYMBOLS:
            response = requests.get(f"{BASE_URL}/predict/{symbol}")
            if response.status_code == 200:
                prediction = response.json()
                change = ((prediction['next_day_prediction'] - prediction['base_price']) / 
                         prediction['base_price'] * 100)
                print(f"\n{symbol} Prediction:")
                print(f"  Current Price: ₹{prediction['base_price']:.2f}")
                print(f"  Predicted Price: ₹{prediction['next_day_prediction']:.2f}")
                print(f"  Expected Change: {change:+.2f}%")
                print(f"  Trend: {prediction['trend']}")
                print(f"  Confidence: {prediction['confidence']*100:.2f}%")
            else:
                print(f"❌ {symbol}: {response.json()['detail']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_refresh_data():
    """Test refresh stock data endpoint"""
    print_header("Testing Refresh Stock Data")
    try:
        symbol = TEST_SYMBOLS[0]
        response = requests.post(f"{BASE_URL}/refresh/{symbol}")
        result = response.json()
        print(f"Refreshed {symbol}:")
        print(f"  Status: {result['status']}")
        print(f"  Records Updated: {result['records_updated']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_different_date_ranges():
    """Test different date ranges"""
    print_header("Testing Different Date Ranges")
    try:
        symbol = TEST_SYMBOLS[0]
        for days in [7, 30, 90, 365]:
            response = requests.get(f"{BASE_URL}/data/{symbol}", params={"days": days})
            data = response.json()
            print(f"  {days} days: {len(data)} records")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_error_handling():
    """Test error handling"""
    print_header("Testing Error Handling")
    
    # Test invalid symbol
    print("1. Testing invalid symbol:")
    try:
        response = requests.get(f"{BASE_URL}/summary/INVALID.NS")
        print(f"   Status: {response.status_code}")
        print(f"   Error: {response.json()['detail']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test comparing same symbol
    print("\n2. Testing comparing same symbol:")
    try:
        response = requests.get(
            f"{BASE_URL}/compare",
            params={"symbol1": "INFY.NS", "symbol2": "INFY.NS"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Error: {response.json()['detail']}")
    except Exception as e:
        print(f"   Error: {e}")


def analyze_metrics():
    """Analyze calculated metrics"""
    print_header("Analyzing Calculated Metrics")
    try:
        symbol = TEST_SYMBOLS[0]
        response = requests.get(f"{BASE_URL}/data/{symbol}", params={"days": 60})
        data = response.json()
        
        if data:
            # Filter out None values
            daily_returns = [d['daily_return'] for d in data if d['daily_return'] is not None]
            volatilities = [d['volatility_30'] for d in data if d['volatility_30'] is not None]
            
            print(f"Metrics for {symbol} (last 60 days):")
            print(f"  Total records: {len(data)}")
            print(f"  Daily returns - Min: {min(daily_returns):.2f}%, Max: {max(daily_returns):.2f}%")
            print(f"  Average volatility: {sum(volatilities)/len(volatilities):.2f}%")
            
            # Calculate cumulative return
            cumulative = sum(daily_returns)
            print(f"  Cumulative return: {cumulative:+.2f}%")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all tests"""
    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║  Stock Data Intelligence Dashboard - API Test Suite      ║
    ║  Test Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Run tests
    test_health()
    test_get_companies()
    test_get_stock_data()
    test_get_summary()
    test_compare_stocks()
    test_predict_price()
    test_different_date_ranges()
    analyze_metrics()
    test_error_handling()
    test_refresh_data()
    
    print(f"\n{'='*60}")
    print(f"  Test Suite Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
