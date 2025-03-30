from flask import request, jsonify
from model import train_model
from redis import fetch_data_from_redis_or_mongodb
import time

def configure_routes(app):

    @app.before_request
    def before_request():
        request.start_time = time.time()

    @app.after_request
    def after_request(response):
        latency = time.time() - request.start_time
        return response

    @app.route('/api/result', methods=['POST'])
    def result():
        stock_symbol = request.get_json().get("stock_symbol")
        stock_data = fetch_data_from_redis_or_mongodb(stock_symbol, app.config['REDIS'], app.config['MONGO'])

        result_html, mse, predicted, actual, dates = train_model(stock_data)

        return jsonify({
            "stock_symbol": stock_symbol,
            "result_html": result_html,
            'dates': dates,
            'actual': actual,
            'predicted': predicted,
            "mse": mse
        })

    @app.route('/api/health', methods=['GET'])
    def health_check():
        status = {"status": "healthy"}
        try:
            app.config['MONGO'].server_info()
        except Exception as e:
            status['mongodb'] = {"status": "unhealthy", "error": str(e)}

        try:
            app.config['REDIS'].ping()
        except Exception as e:
            status['redis'] = {"status": "unhealthy", "error": str(e)}

        return jsonify(status), 200 if 'mongodb' not in status else 500

    @app.route('/api/stocks/all', methods=['GET'])
    def all_stocks():
        return jsonify(app.config['MONGO'].list_collection_names())

