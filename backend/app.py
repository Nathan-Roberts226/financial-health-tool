from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='/frontend')
CORS(app)

@app.route('/')
def redirect_to_frontend():
    return redirect('/frontend/index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    revenue = data.get('revenue', 0)
    expenses = data.get('expenses', 0)
    debt = data.get('debt', 0)
    assets = data.get('assets', 0)
    cash = data.get('cash', 0)
    receivables = data.get('receivables', 0)
    payables = data.get('payables', 0)
    years = data.get('years', 1)

    if revenue <= 0 or assets <= 0:
        return jsonify({'error': 'Revenue and assets must be greater than zero.'}), 400

    profit_margin = max(0, (revenue - expenses) / revenue)
    liquidity = cash / (payables + 1)
    leverage = 1 - (debt / assets)
    efficiency = (receivables - payables) / revenue

    breakdown = {
        'Profitability': round(profit_margin * 25, 2),
        'Liquidity': round(min(liquidity / 2, 1) * 25, 2),
        'Leverage': round(leverage * 25, 2),
        'Efficiency': round(max(0, min(efficiency + 0.5, 1)) * 25, 2)
    }

    suggestions = {
        'Profitability': "Increase revenue or cut costs to improve margins.",
        'Liquidity': "Maintain higher cash reserves to improve liquidity.",
        'Leverage': "Reduce debt or increase asset base to lower leverage.",
        'Efficiency': "Speed up receivables or delay payables to improve efficiency."
    }

    score = int(sum(breakdown.values()))
    assessment = "Strong" if score >= 75 else "Moderate" if score >= 50 else "Needs Attention"

    return jsonify({
        'score': score,
        'assessment': assessment,
        'breakdown': breakdown,
        'suggestions': suggestions,
        'cta': "Let’s take your business to the next level.",
        'link': "https://www.zenithcfos.com/contact"
    })

@app.route('/frontend/<path:filename>')
def serve_static(filename):
    return send_from_directory('../frontend', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)