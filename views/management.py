from flask import Blueprint, render_template, redirect, url_for, request, flash
from sql.db import DB
from flask_login import login_user, login_required, logout_user, current_user

management = Blueprint('management', __name__, url_prefix='/')

# TODO DO NOT EDIT
@management.route('/pending-services')
def pendingservices():

    bookingdate = request.args.get('bookingdate', "")
    location = request.args.get('location', "")
    result = []

    if bookingdate != "" and location != "":
        args = {}
        appointmentQuery = """
                                SELECT a.Appoint_Id, a.Date, l.address, a.status, c.name
                                from Appointment as a
                                left join location as l on l.location_id = a.location_id
                                left join Customer as c on c.cust_id = a.Customer_Id
                                where 1 = 1 and a.status = "Progress" and a.Date = %(bookingdate)s
                            """
        args['bookingdate'] = bookingdate
        result = DB.selectAll(appointmentQuery, args)

        for r in result.rows:
            r['Date'] = str(r['Date'])
        
        result = result.rows

    location = DB.selectAll(""" SELECT Location_id, Address from Location """)

    return render_template("pendingservices.html", location=location.rows, appointments=result)

@management.route('/revenue-computer')
def revenuecomputer():

    args = {}

    startdate = request.args.get('startdate', "")
    enddate = request.args.get('enddate', "")
    location = request.args.get('location', "0")
    result = []
    if startdate != "" and enddate != "": 
        getrevenue = """
                            SELECT a.location_id, l.address, s.service_id, s.service_name, sum(b.price) as total_amount
                            from appointment as a
                            left join bill as b on b.appoint_id = a.appoint_id
                            left join location as l on l.location_id = a.location_id
                            left join service  as s on s.service_id = b.service_id
                            where a.status = "Paid"
                    """
    
        getrevenue += " and a.date between %(startdate)s and %(enddate)s"
        args['startdate'] = startdate
        args['enddate'] = enddate

        if location != "0":
            getrevenue += " and l.address = %(location)s"
            args['location'] = location

        
        getrevenue += " group by a.location_id, s.service_id, s.service_name"
        result = DB.selectAll(getrevenue, args)
        result = result.rows
    
    location = DB.selectAll(""" SELECT Location_id, Address from Location """)

    return render_template("revenuecomputer.html", location=location.rows, rows=result)

@management.route('/top-location')
def toplocation():

    args = {}
    startdate = request.args.get('startdate', "")
    enddate = request.args.get('enddate', "")
    result = []

    if startdate != "" and enddate != "": 
        getrevenue = """
                            SELECT a.location_id, l.address, sum(b.price) as total_amount
                            from appointment as a
                            left join bill as b on b.appoint_id = a.appoint_id
                            left join location as l on l.location_id = a.location_id
                            left join service  as s on s.service_id = b.service_id
                            where a.status = 'Paid'
                    """
    
        getrevenue += " and a.date between %(startdate)s and %(enddate)s"
        args['startdate'] = startdate
        args['enddate'] = enddate

        getrevenue += " group by a.location_id order by total_amount desc limit 3"
        result = DB.selectAll(getrevenue, args)
        result = result.rows

    
    return render_template("toplocation.html", rows=result)