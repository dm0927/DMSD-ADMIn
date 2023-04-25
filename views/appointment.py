from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from sql.db import DB
from flask_bcrypt import Bcrypt

from auth.models import User
from flask_login import login_user, login_required, logout_user, current_user

appointment = Blueprint('appointment', __name__, url_prefix='/appointment')

@appointment.route('/list', methods=['GET','POST'])
@login_required
def list():
    args = {}
    appointmentQuery = """
                            SELECT a.Appoint_Id, a.Date, l.address, a.status, c.name
                            from Appointment as a
                            left join location as l on l.location_id = a.location_id
                            left join Customer as c on c.cust_id = a.Customer_Id
                            where 1 = 1
                        """
    result = DB.selectAll(appointmentQuery, args)

    if result.status and result.rows:
        for r in result.rows:
            r['Date'] = str(r['Date'])
    
    vehicle = DB.selectAll(""" SELECT Vehicle_ID from VEHICLE """)

    location = DB.selectAll(""" SELECT Location_id, Address from Location """)

    return render_template("appointmentlisting.html", appointments=result.rows, vehicles=vehicle.rows, location=location.rows)

@appointment.route('/appointment-view', methods=['GET', 'POST'])
@login_required
def appointmentview():
    customer_id = current_user.get_id()

    if request.method == "POST":
        appointmentid = request.form.get('appointmentid', 0)
        statuschange = request.form.get('statuschange', '')
        result = DB.update("""
                        UPDATE Appointment SET status = %s where Appoint_Id = %s
                    """, statuschange, appointmentid)
        flash("Appointment Status Updated", "success")

    appointment_id = request.args.get('id')
    if appointment_id:

        getCardNumber = DB.selectOne(
                                        """
                                            Select Credit_Card from customer where Cust_id = %s
                                        """
                                    ,customer_id)
        try:
            appointmentResult = DB.selectOne("""
                        SELECT a.Appoint_Id, a.Date, l.address, a.status
                        from Appointment as a
                        left join location as l on l.location_id = a.location_id
                        where Appoint_Id = %s
                    """, appointment_id)
            if appointmentResult.status and appointmentResult.row:
                appointmentResult.row['temp_status'] = appointmentResult.row['status']
                appointmentResult.row['Date'] = str(appointmentResult.row['Date'])
                appointmentResult.row['status'] = appointmentResult.row['status'] if appointmentResult.row['status'] != "Completed" else appointmentResult.row['status'] + " Waiting for Payment"
            
            serviceResult = DB.selectAll("""
                        SELECT i.Amount as grand_total, b.Service_id, s.service_name, b.price 
                        from Invoice as i
                        left join bill as b on b.invoice_id = i.invoice_id
                        left join service as s on s.Service_Id = b.Service_id
                        where b.Appoint_Id = %s
                    """, appointment_id)

            partResult = DB.selectAll("""
                        SELECT bp.Part_ID, bp.Price, p.name
                        from billpart as bp
                        left join part as p on p.part_Id = bp.part_Id
                        where bp.Appoint_Id = %s
                    """, appointment_id)
            if appointmentResult.status and appointmentResult.row:
                appointmentResult.row['Date'] = str(appointmentResult.row['Date'])
        except Exception as e:
            print(str(e))
    else:
        return redirect(url_for('appointment.view'))
    print(appointmentResult.row)
    return render_template("appointmentsingleview.html", appointmentResult=appointmentResult.row, serviceResult=serviceResult.rows, partResult=partResult.rows, cardNumber=getCardNumber.row)

@appointment.route('/services', methods=['GET'])
@login_required
def services():
    result = []
    try:
        result = DB.selectAll("""  SELECT Service_ID, Vehicle_type, Service_name, Labor From Service""")
    except Exception as e:
        print(str(e))
        flash("Something wen't wrong, please try again later", "danger")
    return render_template("services.html", rows=result.rows)

@appointment.route('/services-edit', methods=['GET', 'POST'])
@login_required
def servicesedit():
    id = request.args.get("id",0)
    
    if request.method == "POST":
        service_id = request.form.get('service_id')
        price = request.form.get('price')

        DB.update("""
                        UPDATE Service SET Labor = %s where Service_ID = %s
                  """, price, service_id)
        flash("Service Price Updated", "success")

    if id != 0:
        try:
            result = DB.selectOne("""  SELECT Service_ID, Vehicle_type, Service_name, Labor From Service where Service_id = %s """, id)

        except Exception as e:
            print(str(e))
            flash("Something wen't wrong, please try again later", "danger")
            
    return render_template("servicesview.html", rows=result.row)

@appointment.route('/part', methods=['GET'])
@login_required
def part():
    result = []
    try:
        result = DB.selectAll("""  SELECT s.Service_ID, Service_Name, s.Vehicle_type, so.Part_Id, so.Price, p.Name 
                                   From service_offered as so
                                   left join part as p on p.part_id = so.part_id
                                   left join service as s on s.service_id = so.service_id
                              """)
        print(result.rows)
    except Exception as e:
        print(str(e))
        flash("Something wen't wrong, please try again later", "danger")
    return render_template("part.html", rows=result.rows)

@appointment.route('/part-edit', methods=['GET', 'POST'])
@login_required
def partedit():
    serviceid = request.args.get("serviceid",0)
    vehicletype = request.args.get("vehicletype",0)
    partid = request.args.get("partid",0)
    rows = []
    if request.method == "POST":
        service_id = request.form.get('service_id')
        vehicle_type = request.form.get('Vehicle_type')
        part_id = request.form.get('part_id')
        price = request.form.get('price')

        DB.update("""
                        UPDATE service_offered SET Price = %s where Service_ID = %s and Vehicle_type = %s and Part_id = %s
                  """, price, service_id, vehicle_type, part_id)
        flash("Part Price Updated", "success")

    if id != 0:
        try:
            result = DB.selectOne("""  SELECT s.Service_ID, Service_Name, s.Vehicle_type, so.Part_Id, so.Price, p.Name 
                                        From service_offered as so
                                        left join part as p on p.part_id = so.part_id
                                        left join service as s on s.service_id = so.service_id
                                        where s.Service_ID = %s and s.Vehicle_type = %s and so.Part_Id = %s
                                  """, serviceid, vehicletype, partid)
        except Exception as e:
            print(str(e))
            flash("Something wen't wrong, please try again later", "danger")
    return render_template("partview.html", rows=result.row)