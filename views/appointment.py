from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from sql.db import DB
from flask_bcrypt import Bcrypt

from auth.models import User
from flask_login import login_user, login_required, logout_user, current_user

appointment = Blueprint('appointment', __name__, url_prefix='/appointment')

@appointment.route('/book', methods=['GET','POST'])
@login_required
def book():
    customer_id = current_user.get_id()
    vehicle = []
    location = []
    # if request.method == "POST":
    #     print(request.form.getlist('services[]'))
    try:
        vehicle = DB.selectAll("""
                    SELECT Vehicle_ID
                    from VEHICLE
                    where Customer_ID = %s
                """, customer_id)

        location = DB.selectAll("""
                    SELECT Location_id, Address
                    from Location
                """)
    except Exception as e:
        pass
    return render_template("appointmentbooking.html", vehicles=vehicle.rows, location=location.rows)

@appointment.route('/view')
@login_required
def view():
    customer_id = current_user.get_id()
    appointment = []
    try:
        appointment = DB.selectAll("""
                    SELECT Appoint_Id, Date
                    from Appointment
                    where Customer_ID = %s
                """, customer_id)
    except Exception as e:
        pass
    return render_template("appointmentview.html", appointment=appointment.rows)

@appointment.route('/getVehicleServices', methods=['POST'])
@login_required
def getVehicleServices():
    try:
        id = request.form.get('vehicleId')
        getData = DB.selectAll("""
                                    Select s.service_name as service_name, s.service_id as service_id
                                    from service as s
                                    left join vehicle as v on v.type = s.vehicle_type
                                    where v.vehicle_id = %s
                                """, id)
        if getData.status and getData.rows:
            return jsonify({
                'success':True,
                'data':getData.rows
            })
        else:
            return jsonify({
                'success':False,
                'data':{}
            })
    except:
        return jsonify({
            'success':False,
            'data':{}
        })