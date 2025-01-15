import datetime
from flask import request, make_response
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

class RateLimiter:
    def __init__(self):
        """
        Inicializa o RateLimiter com valores padrão.
        """
        self.rate_limit = 5  # Número máximo de requisições padrão
        self.time_window = 60  # Janela de tempo padrão (em segundos)
        self.clients = {}

    def set_limits(self, rate_limit, time_window):
        self.rate_limit = int(rate_limit)
        self.time_window = int(time_window)

    def is_rate_limited(self, ip):
        """
        Verifica se o IP excedeu o limite de taxa.
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if ip not in self.clients:
            # Novo cliente, inicializa os dados
            self.clients[ip] = {"count": 1, "start_time": current_time}
            logger.info(f"Middleware info: {self.clients}")
            return False

        client_data = self.clients[ip]
        
        # Converte as strings de tempo para objetos datetime
        current_time_dt = datetime.datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
        start_time_dt = datetime.datetime.strptime(client_data["start_time"], "%Y-%m-%d %H:%M:%S")

        # Calcula o tempo decorrido em segundos
        time_elapsed = (current_time_dt - start_time_dt).total_seconds()

        if time_elapsed > self.time_window:
            # Reinicia a contagem após a janela expirar
            self.clients[ip] = {"count": 1, "start_time": current_time}
            logger.info(f"Middleware info: {self.clients}")
            return False

        if client_data["count"] < self.rate_limit:
            # Atualiza a contagem se ainda dentro do limite
            self.clients[ip]["count"] += 1
            logger.info(f"Middleware info: {self.clients}")
            return False

        # Excede o limite
        logger.info(f"Middleware info: {self.clients}")
        return True

    def limit(self):
        ip = request.remote_addr
        if self.is_rate_limited(ip):
            logger.info("Middleware response: {}".format(
                {
                    "success": False,
                    "message": "Too Many Requests. Please try again later."
                }
            ))
            return make_response({
                "success": False,
                "message": "Too Many Requests. Please try again later."
            }, 429)
