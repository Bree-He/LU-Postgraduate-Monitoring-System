from flask import Blueprint

supervisor_bp = Blueprint('supervisor', __name__, template_folder='templates', static_folder='static')

from main.supervisor import supervisor