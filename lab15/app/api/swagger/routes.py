from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  
API_URL = '/swagger'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  
    API_URL,
    config={ 
        'app_name': "My app"
    },
)