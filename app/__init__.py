from flask import Flask, request
from dotenv import load_dotenv
import logging
from .middleware import RateLimiter

rate_limiter = RateLimiter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def create_app():
    app = Flask(__name__)
    
    load_dotenv()
    
    app.config.from_object('app.configs.Config')
    app.json.sort_keys = False
    
    from .routes import api_bp, middleware_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(middleware_bp, url_prefix='/middleware')
    
    # Middleware global de limitação de taxa
    @app.before_request
    def apply_rate_limiting():
        if '/api/get_time' in request.path:
            response = rate_limiter.limit()
            if response:
                return response
    
    
    return app