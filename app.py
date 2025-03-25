from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

    if revenue == 0 or assets == 0:
        return jsonify({'score': 0, 'message': 'Revenue and assets must be greater than zero.'})

    # Scoring logic
    profit_margin = max(0, (revenue - expenses) / revenue)
    liquidity = cash / (payables + 1)
    leverage = 1 - (debt / assets)
    efficiency = (receivables - payables) / revenue

    raw_score = (
        profit_margin * 25 +
        min(liquidity / 2, 1) * 25 +
        leverage * 25 +
        max(0, min(efficiency + 0.5, 1)) * 25
    )

    score = int(max(0, min(raw_score, 100)))
    assessment = "Strong" if score >= 75 else "Moderate" if score >= 50 else "Needs Attention"

    return jsonify({
        'score': score,
        'assessment': assessment,
        'cta': "Let’s take your business to the next level.",
        'link': "https://www.zenithcfos.com/contact"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)