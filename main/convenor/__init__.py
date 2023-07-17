from flask import Blueprint

convenor_bp = Blueprint('convenor', __name__, template_folder='templates', static_folder='static')

from main.convenor import convenor