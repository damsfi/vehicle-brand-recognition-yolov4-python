# Simple local server for testing
# Run this to test your API locally before deploying

from api_server_production import app
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting local API server on http://localhost:{port}")
    print(f"Health check: http://localhost:{port}/health")
    print(f"Test detection: POST http://localhost:{port}/detect")
    print("\nPress Ctrl+C to stop")
    app.run(host='0.0.0.0', port=port, debug=True)

