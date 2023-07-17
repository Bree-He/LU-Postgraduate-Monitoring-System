from flask import Blueprint

chair_bp = Blueprint('chair', __name__, template_folder='templates', static_folder='static')

from main.chair import chair