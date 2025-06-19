from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('dashboard.html')

@main_bp.route('/prediction', methods=['POST'])
def predict():
    # Logique de prédiction
    pass