from flask import request
from app import create_app
from datetime import datetime
import os

a = create_app()

@a.context_processor
def inject_system_info():
    os_name = os.name
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return dict(os_name=os_name, user_agent=user_agent, current_time=current_time)

if __name__ == "__main__":
    a.run(debug=True)