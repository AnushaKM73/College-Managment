from flask import Blueprint, jsonify
from db import get_connection

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admins')
def get_admins():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM super_admin_view"
    )

    data = cursor.fetchall()

    return jsonify(data)