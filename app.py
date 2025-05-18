from flask import Flask, render_template, request, redirect

app = Flask(__name__)
players = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        buy_in = float(request.form['buy_in'])
        cash_out = float(request.form['cash_out'])
        players.append({'name': name, 'buy_in': buy_in, 'cash_out': cash_out})
        return redirect('/')
    return render_template('index.html', players=players)

@app.route('/calculate')
def calculate():
    balances = []
    for p in players:
        balances.append({
            'name': p['name'],
            'balance': round(p['cash_out'] - p['buy_in'], 2)
        })

    transactions = []
    while True:
        payers = [p for p in balances if p['balance'] < -1]
        receivers = [p for p in balances if p['balance'] > 1]

        if not payers or not receivers:
            break

        payers.sort(key=lambda x: x['balance'])
        receivers.sort(key=lambda x: -x['balance'])

        payer = payers[0]
        receiver = receivers[0]

        amount = min(-payer['balance'], receiver['balance'])

        if amount >= 10:
            rounded = round(amount / 10) * 10
        elif amount >= 5:
            rounded = round(amount / 5) * 5
        else:
            rounded = round(amount)

        rounded = min(rounded, amount)

        transactions.append(f"{payer['name']} משלם ל־{receiver['name']} {int(rounded)} ש\"ח")

        payer['balance'] += rounded
        receiver['balance'] -= rounded

    return render_template('index.html', players=players, transactions=transactions)

@app.route('/reset')
def reset():
    players.clear()
    return redirect('/')

@app.route('/delete/<name>')
def delete_player(name):
    global players
    players = [p for p in players if p['name'] != name]
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)