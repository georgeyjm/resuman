import os
from resuman import create_app

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))

    app = create_app()
    app.run(host=host, port=port, use_reloader=False)
