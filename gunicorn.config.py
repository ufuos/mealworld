import multiprocessing, os
port = os.environ.get('PORT', '8000')
bind = f"0.0.0.0:{port}"
cpu_count = multiprocessing.cpu_count()
workers = int(os.environ.get('GUNICORN_WORKERS', (cpu_count * 2) + 1))
worker_class = os.environ.get('GUNICORN_WORKER_CLASS', 'sync')
timeout = int(os.environ.get('GUNICORN_TIMEOUT', 120))
graceful_timeout = int(os.environ.get('GUNICORN_GRACEFUL_TIMEOUT', 30))
keepalive = int(os.environ.get('GUNICORN_KEEPALIVE', 2))
errorlog = '-'
accesslog = '-'
loglevel = os.environ.get('GUNICORN_LOGLEVEL', 'info')
preload_app = os.environ.get('GUNICORN_PRELOAD', 'False') == 'True'
