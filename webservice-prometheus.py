from flask import Flask, request, jsonify
from prometheus_client import Counter, Gauge, Histogram, Summary, start_http_server
import math
import time

app = Flask(__name__)

REQUEST_COUNT = Counter('factorial_requests_total', 'Total de solicitudes recibidas')
REQUEST_IN_PROGRESS = Gauge('factorial_requests_in_progress', 'Solicitudes en progreso')
REQUEST_LATENCY = Histogram('factorial_request_latency_seconds', 'Distribución de latencias')
REQUEST_STATS = Summary('factorial_request_summary_seconds', 'Estadísticas de latencias')

@app.route('/factorial', methods=['GET'])
def factorial():
    REQUEST_COUNT.inc()  # Incrementar contador de solicitudes
    REQUEST_IN_PROGRESS.inc()  # Incrementar gauge de solicitudes en progreso
    
    start_time = time.time()
    try:
        n = int(request.args.get('number', 1))
        result = math.factorial(n)
        return jsonify({'number': n, 'factorial': result})
    finally:
        latency = time.time() - start_time
        REQUEST_LATENCY.observe(latency)  # Registrar latencia en histogram
        REQUEST_STATS.observe(latency)  # Registrar latencia en summary
        REQUEST_IN_PROGRESS.dec()  # Decrementar gauge de solicitudes en progreso

if __name__ == '__main__':
    start_http_server(8001) #metrics
    app.run(host='0.0.0.0', port=5000) #factorial