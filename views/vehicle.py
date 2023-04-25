from flask import Blueprint, render_template, redirect, url_for, request, flash
from sql.db import DB
from flask_bcrypt import Bcrypt

from auth.models import User
from flask_login import login_user, login_required, logout_user, current_user

vehicle = Blueprint('vehicle', __name__, url_prefix='/vehicle')

@vehicle.route('/add', methods=['GET','POST'])
@login_required
def add():
    if request.method == "POST":
        try:
            vehiclenumber = request.form.get('vehiclenumber')
            vehicleyear = request.form.get('vehicleyear')
            vehicletype = request.form.get('vehicletype')
            vehiclemfg = request.form.get('vehiclemfg')
            vehiclemodel = request.form.get('vehiclemodel')
            vehiclecolor = request.form.get('vehiclecolor')
            customer_id = current_user.get_id()
            result = DB.insertOne("""
                        INSERT INTO VEHICLE(Vehicle_ID,Year,Type,Mfg,Model,Color,Customer_ID) VALUES(%s,%s,%s,%s,%s,%s,%s) """, 
                        vehiclenumber, vehicleyear, vehicletype, vehiclemfg, vehiclemodel, vehiclecolor, customer_id)
            if result.status:
                flash("New Vechile Added", "success")
        except Exception as e:
            flash("Something wen't wron, please try again later", "danger")
    return render_template("vehicleadd.html")

@vehicle.route("/list", methods=['GET'])
@login_required
def view():
    customer_id = current_user.get_id()
    result = []
    try:
        result = DB.selectAll("""
                    SELECT Vehicle_ID,Year,Type,Mfg,Model,Color
                    from VEHICLE
                    where Customer_ID = %s
                """, customer_id)
    except Exception as e:
        pass
    return render_template("vehiclelist.html", rows=result.rows)

@vehicle.route("/edit", methods=['GET','POST'])
@login_required
def edit():
    try:
        id = request.args['id']
    except:
        id = ""
    customer_id = current_user.get_id()
    if request.method == "POST":
        vehiclenumber = request.form.get('vehiclenumber')
        vehicleyear = request.form.get('vehicleyear')
        vehicletype = request.form.get('vehicletype')
        vehiclemfg = request.form.get('vehiclemfg')
        vehiclemodel = request.form.get('vehiclemodel')
        vehiclecolor = request.form.get('vehiclecolor')
        # Vehicle_ID,Year,Type,Mfg,Model,Color,Customer_ID
        try:
            result = DB.update("""
                    UPDATE VEHICLE
                    SET Year=%s, Type=%s, Mfg=%s, Model=%s, Color=%s where Customer_ID = %s and Vehicle_ID = %s""", 
                    vehicleyear, vehicletype, vehiclemfg, vehiclemodel, vehiclecolor, customer_id, vehiclenumber)
            flash("Record Updated Successfully", "success")
        except:
            flash("Something wen't wrong, please try again later", "danger")
    row = []
    if id != "":
        result = []
        try:
            result = DB.selectOne("""
                        SELECT Vehicle_ID,Year,Type,Mfg,Model,Color
                        from VEHICLE
                        where Customer_ID = %s and Vehicle_ID = %s
                    """, customer_id, id)
            if result.status and result.row:
                row = result.row
        except Exception as e:
            pass
    else:
        return redirect(url_for('vehicle.view'))
    return render_template("vehicleedit.html", row=row)
