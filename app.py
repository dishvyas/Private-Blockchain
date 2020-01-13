from app import app
import os
# app = Flask(__name__)

# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
if __name__ == '__main__':
    app.run()

# app.run(debug=True)
