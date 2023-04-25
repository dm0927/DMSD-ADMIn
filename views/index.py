from flask import Blueprint, render_template, redirect, url_for, request, flash
from sql.db import DB
from flask_bcrypt import Bcrypt

from auth.models import User
from flask_login import login_user, login_required, logout_user, current_user

home = Blueprint('home', __name__, url_prefix='/')

bcrypt = Bcrypt()

# TODO DO NOT EDIT
@home.route('/')
def index():
    if current_user.is_active != False:
        return redirect(url_for('home.dashboard'))
    return render_template("login.html")

@home.route('/authentication', methods=['POST'])
def authentication():
    if current_user.is_active != False:
        return redirect(url_for('home.dashboard'))
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        result = DB.selectOne("SELECT Cust_ID as id, Name as name, Phone as phone, Email as email, Address as address, password FROM CUSTOMER WHERE email = %s", email)
        if result.status and result.row:
            if bcrypt.check_password_hash(result.row["password"], password):
                del result.row["password"] # don't carry password/hash beyond here
                user = User(**result.row)
                success = login_user(user) # login the user via flask_login
                if success:
                    return redirect(url_for("home.dashboard"))
                else:
                    flash("Error logging in", "danger")
            else:
                flash("The password you typed isn't correct.", "warning")
        else:
            flash("We weren't able to find the user.", "warning")
    except Exception as e:
        flash("Something wen't wrong, please try again later", "danger")
    return redirect(url_for("home.index"))

@home.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_active != False:
        return redirect(url_for('home.dashboard'))
    if request.method == "POST":
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirmpassword = request.form.get('confirmpassword')
        if password == confirmpassword:
            hash = bcrypt.generate_password_hash(password)
            result = DB.insertOne("""
                    INSERT INTO CUSTOMER(Name,Email,Phone,Password)
                    VALUES(%s,%s,%s,%s)
                    """, fullname, email, phone, hash)
            if result.status:
                flash("User Created.", "success")    
                return redirect(url_for("home.index"))
        else:
            flash("Password and Confirm Password aren't same.", "warning")
    return render_template("register.html")

@home.route('/dashboard')
@login_required
def dashboard():
    return render_template("home.html")


@home.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    if request.method == "POST":
        try:
            id = current_user.get_id()
            fullname = request.form.get('fullname')
            email = request.form.get('email')
            address = request.form.get('address')
            phone = request.form.get('phone')
            result = DB.update("""UPDATE CUSTOMER SET Name=%s, Address=%s, Phone=%s, Email=%s where Cust_ID=%s""", fullname, address, phone, email, id)
            if result.status:
                try:
                    flash("Profile Updated of the User", "success")
                    result = DB.selectOne("SELECT Cust_ID as id, Name as name, Phone as phone, Email as email, Address as address FROM CUSTOMER WHERE Cust_ID = %s", id)
                    if result.status and result.row:
                        user = User(**result.row)
                        current_user.name = user.name
                        current_user.email = user.email
                        current_user.address = user.address
                        current_user.phone = user.phone
                except Exception as e:
                    print(str(e))
        except Exception as e:
            flash("Something wen't wrong, please try again later", "danger")    
    return render_template('profile.html')

@home.route('/changepassword', methods=["POST"])
@login_required
def changepassword():
    if request.method == "POST":
        id = current_user.get_id()
        oldpassword = request.form.get('oldpassword')
        newpassword = request.form.get('newpassword')
        confirmnewpassword = request.form.get('confirmnewpassword')
        if newpassword == confirmnewpassword:
            result = DB.selectOne('''SELECT password from CUSTOMER where cust_id = %s''', id)
            if result.status:
                if bcrypt.check_password_hash(result.row["password"], oldpassword):
                    hash = bcrypt.generate_password_hash(newpassword)
                    result = DB.update("UPDATE CUSTOMER SET password = %s WHERE cust_id = %s", hash, id)
                    flash("Password updated", "success")
                    # logout_user()
                    # return redirect(url_for("home.index"))
            else:
                flash("Old Password is Incorrect", "warning")    
        else:
            flash("New Password and Confirmn New Password should be same", "warning")
    return redirect(url_for("home.profile"))


@home.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home.index"))