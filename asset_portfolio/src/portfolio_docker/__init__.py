from portfolio import app

def portfolio_app():
    app.run(
        host='0.0.0.0',
        port='5001',
        debug=False,
    )
