from flask import Blueprint, request, make_response
from . import logger, rate_limiter
from .validators import SetLimitsForm
import datetime

api_bp = Blueprint('api', __name__)
middleware_bp = Blueprint('middleware', __name__)


"""
    Middleware Routes
"""
@middleware_bp.route('/set_limits', methods=['POST'])
def set_limits():
    try:
        """
        Define os limites de taxa e a janela de tempo dinamicamente.
        """
        data = request.get_json()
        form = SetLimitsForm(data=data)
        logger.info(f"set_limits request received: {data}")

        if form.validate():
            rate_limit = data.get('rate_limit')
            time_window = data.get('time_window')

            rate_limiter.set_limits(rate_limit, time_window)
            
            logger.info(f"set_limits response: Rate limit set to {rate_limit} requests per {time_window} seconds!")
            return make_response({
                "success": True,
                "message": f"Rate limit set to {rate_limit} requests per {time_window} seconds!"
            }, 200)
            
        else:
            logger.error({
                "message": "Validations errors",
                "errors": form.errors,
            })
            return make_response({
                "success": False,
                "message": "Validations errors",
                "errors": form.errors
            }, 400)
            
    except Exception as e:
        logger.error(e, exc_info=True)
        logger.info(f"error {e} occured on set_limits api")
        return make_response({
            "message": "An unexpected error occurred. Please try again later!",
            "code": 500
        }, 500)
        
        
"""
    Other Routes
"""
@api_bp.route('/get_time', methods=['GET'])
def get_time():
    try:
        """
        Retorna a data e hora de Moçambique e Etiópia.
        """
        logger.info(f"get_time request receive")
        now = datetime.datetime.utcnow()
        mozambique_time = now + datetime.timedelta(hours=2)  # UTC+2
        ethiopia_time = now + datetime.timedelta(hours=3)  # UTC+3

        logger.info("get_time response: {}".format(
            {
                "success": True,
                "data": {
                    "mozambique_time": mozambique_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "ethiopia_time": ethiopia_time.strftime("%Y-%m-%d %H:%M:%S")
                }
            }))
        
        return make_response({
            "success": True,
            "data": {
                "mozambique_time": mozambique_time.strftime("%Y-%m-%d %H:%M:%S"),
                "ethiopia_time": ethiopia_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }, 200)
        
    except Exception as e:
        logger.error(e, exc_info=True)
        logger.info(f"error {e} occured on get_time api")
        return make_response({
            "message": "An unexpected error occurred. Please try again later!",
            "code": 500
        }, 500)
        
