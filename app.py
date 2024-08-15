from flask import Flask, jsonify, request, render_template
import requests
import time

app = Flask(__name__)

window_size = 10
numbers_window = []

def fetch_numbers(number_id):
    mock_data = {
        'p': [2, 3, 5, 7, 11],
        'f': [1, 1, 2, 3, 5],
        'e': [2, 4, 6, 8, 10],
        'r': [10, 20, 30, 40, 50]
    }
    return mock_data.get(number_id, [])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/numbers/<string:numberid>', methods=['GET'])
def get_numbers(numberid):
    global numbers_window
    prev_state = numbers_window[:]
    
    try:
        start_time = time.time()
        numbers = fetch_numbers(numberid)
        elapsed_time = time.time() - start_time
        
        if elapsed_time > 0.5:
            raise TimeoutError("API response took longer than 500 ms")
        numbers = list(set(numbers))
        numbers_window.extend(numbers)
        if len(numbers_window) > window_size:
            numbers_window = numbers_window[-window_size:]
        avg = sum(numbers_window) / len(numbers_window) if numbers_window else 0

        return jsonify({
            "windowPrevState": prev_state,
            "windowCurrState": numbers_window,
            "numbers": numbers,
            "avg": round(avg, 2)
        })

    except TimeoutError:
        return jsonify({"error": "Request took too long"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876)
