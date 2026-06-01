from flask import Flask, render_template, request, jsonify
from analyzer import run_analysis

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        
        stocks = data.get('stocks', [])
        
        if not stocks:
            return jsonify({"error": "No stocks provided"}), 400
        
        if len(stocks) < 2:
            return jsonify({"error": "Please enter at least 2 stocks"}), 400
        
        tickers = [s['ticker'].upper().strip() for s in stocks]
        amounts = [float(s['amount']) for s in stocks]
        
        total = sum(amounts)
        weights = [a / total for a in amounts]
        
        result = run_analysis(tickers, weights)
        
        if "error" in result:
            return jsonify(result), 400
            
        return jsonify(result)
    
    except ValueError:
        return jsonify({"error": "Invalid amount entered"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)