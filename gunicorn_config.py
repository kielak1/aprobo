import multiprocessing

#bind = "127.0.0.1:8000"  # IP i port
bind = "unix:/opt/aprobo/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1  # Ilość workerów
accesslog = '/var/log/gunicorn/access-log'  # Logowanie dostępu, '-' oznacza stdout
errorlog = '/var/log/gunicorn/error-log'  # Logowanie błędów, '-' oznacza stdout
