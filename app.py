from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Single-page HTML/CSS/JS frontend
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Docker Calculator</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f6f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .calc-card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 320px; text-align: center; }
        h2 { color: #333; margin-top: 0; }
        input, select, button { width: 100%; padding: 10px; margin: 8px 0; border-radius: 6px; border: 1px solid #ccc; box-sizing: border-box; font-size: 16px; }
        button { background-color: #007bff; color: white; border: none; cursor: pointer; font-weight: bold; transition: background 0.2s; }
        button:hover { background-color: #0056b3; }
        .result-box { margin-top: 15px; padding: 12px; background: #e9ecef; border-radius: 6px; font-weight: bold; color: #495057; font-size: 18px; min-height: 22px; }
    </style>
</head>
<body>

<div class="calc-card">
    <h2>🐳 Docker Calculator</h2>
    <input type="number" id="num1" placeholder="Enter first number" step="any">
    
    <select id="operation">
        <option value="add">Add (+)</option>
        <option value="subtract">Subtract (-)</option>
        <option value="multiply">Multiply (×)</option>
        <option value="divide">Divide (÷)</option>
    </select>
    
    <input type="number" id="num2" placeholder="Enter second number" step="any">
    <button onclick="calculate()">Calculate</button>
    
    <div class="result-box" id="result">Result will appear here</div>
</div>

<script>
    async function calculate() {
        const num1 = document.getElementById('num1').value;
        const num2 = document.getElementById('num2').value;
        const op = document.getElementById('operation').value;
        const resultBox = document.getElementById('result');

        if (!num1 || !num2) {
            resultBox.innerText = "Please enter both numbers";
            resultBox.style.color = "#dc3545";
            return;
        }

        try {
            // Fetch dynamically from our Docker Flask API endpoints
            const response = await fetch(`/${op}/${num1}/${num2}`);
            const data = await response.json();
            
            if (response.ok) {
                resultBox.innerText = `Result: ${data.result}`;
                resultBox.style.color = "#28a745";
            } else {
                resultBox.innerText = data.error || "An error occurred";
                resultBox.style.color = "#dc3545";
            }
        } catch (error) {
            resultBox.innerText = "Error connecting to server";
            resultBox.style.color = "#dc3545";
        }
    }
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/add/<float:num1>/<float:num2>')
def add(num1, num2):
    return jsonify({"operation": "addition", "result": num1 + num2})

@app.route('/subtract/<float:num1>/<float:num2>')
def subtract(num1, num2):
    return jsonify({"operation": "subtraction", "result": num1 - num2})

@app.route('/multiply/<float:num1>/<float:num2>')
def multiply(num1, num2):
    return jsonify({"operation": "multiplication", "result": num1 * num2})

@app.route('/divide/<float:num1>/<float:num2>')
def divide(num1, num2):
    if num2 == 0:
        return jsonify({"error": "Cannot divide by zero"}), 400
    return jsonify({"operation": "division", "result": num1 / num2})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
