from flask import Flask

app = Flask(__name__, template_folder='templates', static_folder='static')
app.debug = True

# for the session
app.secret_key = 'some secret key'

from main import routes
from main.admin import admin_bp
from main.student import student_bp
from main.supervisor import supervisor_bp
from main.convenor import convenor_bp
from main.chair import chair_bp

# Register blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(supervisor_bp, url_prefix='/supervisor')
app.register_blueprint(convenor_bp, url_prefix='/convenor')
app.register_blueprint(chair_bp, url_prefix='/chair')

if __name__ == '__main__':
    app.run(debug=True)