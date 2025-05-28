# This is a car sale website for Eswatini agents, owners, garages and car sales stores
# They advertise new and second cars of any brand
# They can also sale spare parts when stripping they cars

from flask import Flask,render_template,url_for,redirect,request,flash,session,jsonify
from flask_login import login_user, LoginManager,current_user,logout_user, login_required
from Forms import *
from models import *
from flask_bcrypt import Bcrypt
# import Users_Data
import secrets
import os
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
# from bs4 import BeautifulSoup as bs
# from flask_colorpicker import colorpicker
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
import pyodbc
import sqlite3
import itsdangerous
import time


#Change App
app = Flask(__name__)
app.config['SECRET_KEY'] = "sdkh77sdjfe832j2rj_32j"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle':280}
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOADED"] = 'static/uploads'

# Local
if os.environ.get('EMAIL_INFO') == 'info@techxolutions.com':
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///car_bids_db.db"
else:#Online
    app.config[
    "SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://techtlnf_tmaz:!Tmazst41#@localhost/techtlnf_grace_auto_db" 

application = app

ser = Serializer(app.config['SECRET_KEY']) 

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Log in
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


ALLOWED_EXTENSIONS = {"txt", "xlxs",'docx', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file has an allowed extension
def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class user_class:
    s = None

    def get_reset_token(self, c_user_id):

        s = Serializer(app.config['SECRET_KEY'])

        return s.dumps({'user_id': c_user_id, 'expiration_time': time.time() + 300}).encode('utf-8')

    @staticmethod
    def verify_reset_token(token, expires=1800):

        s = Serializer(app.config['SECRET_KEY'], )

        try:
            user_id = s.loads(token, max_age=300)['user_id']
        except itsdangerous.SignatureExpired:
            flash('Token has expired', 'error')
        except itsdangerous.BadSignature:
            flash('Token is Invalid', 'error')
        except:
            return f'Something Went Wrong'  # f'Token {user_id} not accessed here is the outcome user'

        return user_id


# Function to delete an image from the database
def delete_image(image_name):
    # Check img_1
    result = delete_image_from_column('img_1', image_name)
    if result:
        return f"Image {image_name} deleted."

    # Check img_2
    result = delete_image_from_column('img_2', image_name)
    if result:
        return f"Image {image_name} deleted."

    # Check img_3
    result = delete_image_from_column('img_3', image_name)
    if result:
        return f"Image {image_name} deleted."
    
    # Check img_4
    result = delete_image_from_column('img_4', image_name)
    if result:
        return f"Image {image_name} deleted."
    
    # Check img_5
    result = delete_image_from_column('img_5', image_name)
    if result:
        return f"Image {image_name} deleted."
    
    # Check img_6
    result = delete_image_from_column('img_6', image_name)
    if result:
        return f"Image {image_name} deleted."
    
    # Check img_7
    result = delete_image_from_column('img_7', image_name)
    if result:
        return f"Image {image_name} deleted."
    
    # Check img_8
    result = delete_image_from_column('img_8', image_name)
    if result:
        return f"Image {image_name} deleted."
    
    # Check img_9
    result = delete_image_from_column('img_9', image_name)
    if result:
        return f"Image {image_name} deleted."
    
    # Check img_10
    result = delete_image_from_column('img_10', image_name)
    if result:
        return f"Image {image_name} deleted."

    return f"Image {image_name} not found."

# Function to delete an image from a specific column
def delete_image_from_column(column_name, image_name):
    image = Car_Ads_Images.query.filter(getattr(Car_Ads_Images, column_name) == image_name).first()
    if image:
        file_path = os.path.join(app.root_path, 'static/images', image_name)
        if os.path.exists(file_path):
            os.remove(file_path)

        setattr(image, column_name, None)  # Or set it to an empty string depending on your requirements
        db.session.commit()
        return True
    else:
        return False


# @app.route('/delete_img',methos=['GET'])
def delete_img(column_name,token):
    # Get image row
    token=token
    image = Car_Ads_Images.query.filter_by(token=Car_Details.token).first()
    print("img obj: ",image.__getattribute__(column_name))
    column_value=getattr(image,column_name)
    print("Checking Column VAlue: ",column_value)

    if column_value:
        file_path = os.path.join(app.root_path, 'static/uploads', column_value)
    
    if os.path.exists(file_path):
        print("DEBUG FILE PATH: ",file_path)
        os.remove(file_path)
    
    setattr(image, column_name, None)  # Or set it to an empty string depending on your requirements
    db.session.commit()
    # Flash message required
    return True

class Dont_Update:
    img = ''
    cur_file = ''


def process_profile(file):
        global img_checker
        img_checker = Dont_Update
        if img_checker.img  == file.filename:
            print("File updated")
            return img_checker.cur_file
        else:
        
            filename = secure_filename(file.filename)

            img_checker.img = file.filename

            _img_name, _ext = os.path.splitext(file.filename)
            gen_random = secrets.token_hex(8)
            new_file_name = gen_random + _ext

            print("DEBIG IMAGE: ",new_file_name)

            if file.filename == '':
                return 'No selected file'

            if file.filename:
                file_saved = file.save(os.path.join("static/images/", new_file_name)) #join(app.root_path, 'static/images', new_file_name)
                img_checker.cur_file = new_file_name
                flash(f"File Upload Successful!!", "success")
                return new_file_name

            else:
                return f"Allowed are [ .png, .jpg, .jpeg, .gif] only"


def car_images(images_uploads):

    uploaded_files = images_uploads
    img_names_ls = []
    img_string = ''

    if uploaded_files:
        for file in uploaded_files:
            print("Image: ",file.filename)
            filename = secure_filename(file.filename)
            print("Filename: ",filename)
            _img_name, _ext = os.path.splitext(file.filename)
            gen_random = secrets.token_hex(8)
            new_file_name = gen_random + _ext

            # Append image to img_names
            img_names_ls.append(new_file_name)

            # Save image in the server 
            if file:
                file.save(os.path.join(app.config['UPLOADED'], new_file_name))
                print("File Saved : ",file.filename)

    for image in img_names_ls:
        img_string += '_'+image
        print("Check Images: ",img_string)
    print("Check Images: ",uploaded_files)

    return img_names_ls

encry_pw = Bcrypt()

@app.context_processor
def inject_ser():
    ser = Serializer(app.config['SECRET_KEY'])  # Define or retrieve the value for 'ser'
    return dict(ser=ser,sys=os)


@app.route("/", methods=['POST','GET'])
def home():

    with app.app_context():
        db.create_all()
    

    title = "Car Bids"

    car_ads = Car_Details.query.all()
    agent_usr = User
    images = Car_Images
    images_qry = Car_Images.query.all()

    # print("Query Images: ",images.query.filter_by(token=car_ads[0].token).first())
    # for obj in images:
    #     print("Query: ", obj.token) #[img for img in obj.car_images.split("_") if img])
        # for img in obj.car_images.split("_")[0]:
        #     print("Query: ",img)

    if request.method == ['POST']:
        pass
        # print("Method requested : ",request.form)
        # soup = bs(request.form, "html.parser")

    return render_template("index.html",car_ads=car_ads,agent_usr=agent_usr,images_cls=images)


@app.route("/car_agent_signup", methods=["POST","GET"])
def sign_up():

    register = Register()

    agent_user = '' #car_agent_user.query.get()

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    image_fl = url_for('static', filename='images/image.jpg')

    if request.method == 'POST':

        if register.validate_on_submit():    

            hashd_pwd = encry_pw.generate_password_hash(register.password.data).decode('utf-8')
            user1 = car_agent_user(name=register.name.data, email=register.user_email.data, password=hashd_pwd,
                         confirm_password=hashd_pwd,image="default.jpg",contacts=register.contacts.data,verified=True,
                         )

            # try:
            if not Register().validate_email(register.user_email.data):
                db.session.add(user1)
                db.session.commit()
                flash(f"Account Successfully Created for {register.name.data}", "success")
                return redirect (url_for('login'))
            else:
                flash(f"This email is already registered!", "error")
            
            return redirect(url_for('login'))
            # except: # IntegrityError:
            #     pass

        elif register.errors:
            flash(f"Account Creation Unsuccessful ", "error")
            print(register.errors)

    # from myproject.models import user
    return render_template("signup-form.html",register=register,agent_user=agent_user)
 

# import re

# def password():
#     print ('Enter a password\n\nThe password must be between 6 and 12 characters.\n')

#     while True:
#         password = input('Password: ... ')
#         if 6 <= len(password) < 12:
#             break
#         print ('The password must be between 6 and 12 characters.\n')

#     password_scores = {0:'Horrible', 1:'Weak', 2:'Medium', 3:'Strong'}
#     password_strength = dict.fromkeys(['has_upper', 'has_lower', 'has_num'], False)
#     if re.search(r'[A-Z]', password):
#         password_strength['has_upper'] = True
#     if re.search(r'[a-z]', password):
#         password_strength['has_lower'] = True
#     if re.search(r'[0-9]', password):
#         password_strength['has_num'] = True

#     score = len([b for b in password_strength.values() if b])

#     print ('Password is %s' % password_scores[score])



@app.route("/user_acc", methods=["POST","GET"])
@login_required
def user_acc():

    register = Account()

    agent_user = car_agent_user.query.get(current_user.id)

    
    if current_user.role == 'mechanic_user':
        return redirect(url_for('mechanic_user_acc'))

    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))

    image_fl = url_for('static', filename='images/image.jpg')

    if request.method == 'POST':

        if register.validate_on_submit():
            # hashd_pwd = encry_pw.generate_password_hash(register.password.data).decode('utf-8')
            agent_user.name = register.name.data
            print("IMAGE: ", register.image_pfl.data, request.args.get("image_pfl"))
            if register.image_pfl.data:
                img_new = process_profile(register.image_pfl.data)
                if img_checker:
                    print("Suka: ",img_new)
                    agent_user.image = img_new

            agent_user.contacts = register.contacts.data
            agent_user.whatsapp = register.whatsapp.data
            agent_user.facebook = register.facebook.data
            agent_user.date_of_birth = register.date_of_birth.data
            agent_user.personal_id_no = register.personal_id_no.data
            agent_user.zip_code = register.zip_code.data
            agent_user.address = register.address.data

            db.session.commit()
            print("DOES IT VALIDATE")

        elif register.errors:
            flash(f"Update Unsuccessful ", "error")
            print(register.errors)

    # from myproject.models import user
    return render_template("user_acc.html", register=register, agent_user=agent_user)


@app.route("/mechanics", methods=["POST","GET"])
def mechanics():

    mechanics_qry = Mechanics.query.all()

    return render_template("mechanics_specialists.html",mechanics_qry=mechanics_qry)


@app.route("/mechanic_user_acc", methods=["POST","GET"])
@login_required
def mechanic_user_acc():

    register = Mechanics_Acc()

    mechanic_user = Mechanics.query.get(current_user.id)

    if request.method == 'POST':

        if register.validate_on_submit():
            # hashd_pwd = encry_pw.generate_password_hash(register.password.data).decode('utf-8')
            mechanic_user.name = register.name.data
            print("IMAGE: ", register.image_pfl.data, request.args.get("image_pfl"))
            if register.image_pfl.data:
                img_new = process_profile(register.image_pfl.data)
                if img_checker:
                    mechanic_user.image = img_new

            mechanic_user.contacts = register.contacts.data
            mechanic_user.more_info = request.form['more_info']
            mechanic_user.specialty = register.specialty.data
            mechanic_user.whatsapp = register.whatsapp.data
            mechanic_user.facebook = register.facebook.data
            mechanic_user.personal_id_no = register.personal_id_no.data
            mechanic_user.address = register.address.data

            db.session.commit()
            flash(f"Update Successful", "success")

        elif register.errors:
            flash(f"Update Unsuccessful", "error")
            print(register.errors)

    # from myproject.models import user
    return render_template("mechanic_acc_edit.html",register=register,mechanic_user=mechanic_user)


@app.route("/login", methods=["POST","GET"])
def login():

    login = Login()

    print(f"Submtion: ")
    if request.method == 'POST':

        if login.validate_on_submit():    

                user_login = User.query.filter_by(email=login.user_email.data).first()
                # flash(f"Hey! {user_login.password} Welcome", "success")
                if user_login and encry_pw.check_password_hash(user_login.password, login.password.data):
                    login_user(user_login)
                    print("Creditantials are ok")
                    if not user_login.verified:
                        return redirect(url_for('verification'))
                    else:
                        # After login required prompt, take me to the page I requested earlier
                        print("No Verification Needed: ", user_login.verified)
                        req_page = request.args.get('next')
                        flash(f"Hey! {user_login.name.title()} You're Logged In!", "success")
                        return redirect(req_page) if req_page else redirect(url_for('home'))
                else:
                    flash(f"Login Unsuccessful, please use correct email or password", "error")
                    # print(login.errors)
        else:
            print("No Validation")
            if login.errors:
                for error in login.errors:
                    print("Errors: ", error)
            else:
                print("No Errors found", login.email.data, login.password.data)

    return render_template("login.html",login=login)


@app.route("/forgot_password", methods=['POST', "GET"])
def reset_request():
    reset_request_form = Reset_Request()

    if current_user.is_authenticated:
        logout_user()

    if request.method == 'POST':
        if reset_request_form.validate_on_submit():
            # Get user details through their email
            usr_email = User.query.filter_by(email=reset_request_form.email.data).first()

            if usr_email is None:
                # print("The email you are request for is not register with T.H.T, please register first, Please Retry")
                flash(
                    "The email you are requesting a password reset for, is not registered with VnE, please register as account first",
                    'error')

                return redirect(url_for("reset_request"))

            def send_link(usr_email):
                app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                app.config["MAIL_PORT"] = 587
                app.config["MAIL_USE_TLS"] = True
                em = app.config["MAIL_USERNAME"] = os.getenv("EMAIL")
                app.config["MAIL_PASSWORD"] = "abng vekb agyv osbw"  # os.getenv("PWD")

                mail = Mail(app)

                token = user_class().get_reset_token(usr_email.id)
                msg = Message("Password Reset Request", sender="noreply@demo.com", recipients=[usr_email.email])
                msg.body = f"""Good day, {usr_email.name}

You have requested a password reset for your The Car Bids Account.
To reset your password, visit the following link:{url_for('reset_request', token=token, _external=True)}

If you did not requested the above message please ignore it, and your password will remain unchanged.
"""

                try:
                    mail.send(msg)
                    flash('An email has been sent with instructions to reset your password', 'success')
                    return "Email Sent"
                except Exception as e:

                    flash('Ooops, Something went wrong Please Retry!!', 'error')
                    return "The mail was not sent"

            # Send the pwd reset request to the above email
            send_link(usr_email)

            return redirect(url_for('login'))

    return render_template("forgot_password.html", reset_request_form=reset_request_form)


@app.route("/verification", methods=["POST", "GET"])
# User email verification @login
# @login the user will register & when the log in the code checks if the user is verified first...
def verification():

    usr_ = User.query.get(current_user.id)

    def send_veri_mail():

        app.config["MAIL_SERVER"] = "smtp.googlemail.com"
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        # Creditentials saved in environmental variables
        em = app.config["MAIL_USERNAME"] = "pro.dignitron@gmail.com"  # os.getenv("MAIL")
        app.config["MAIL_PASSWORD"] = os.getenv("PWD")
        app.config["MAIL_DEFAULT_SENDER"] = 'Car Bids Eswatini <no-reply@gmail.com>'
        app.config["MAIL_DEFAULT_SENDER"] = "noreply@gmail.com"

        mail = Mail(app)

        token = user_class().get_reset_token(current_user.id)
        usr_email = usr_.email

        msg = Message(subject="Email Verification", sender="no-reply@gmail.com", recipients=[usr_email])

        msg.body = f"""Hi, {usr_.name}
            
Please follow the link below to verify your email with The Hustlers Time:
            
Verification link;
{url_for('verified', token=token, _external=True)}
        """
        try:
            mail.send(msg)
            flash(f'An email has been sent with a verification link to your email account', 'success')
            return "Email Sent"
        except Exception as e:
            flash(f'Email not sent here', 'error')
            return "The mail was not sent"

    try:
        if not usr_.verified:
            send_veri_mail()
        else:
            return redirect(url_for("home"))
    except:
        flash(f'Debug {usr_.email}', 'error')
        return redirect(url_for("login"))

    return render_template('verification.html')


@app.route("/verified/<token>", methods=["POST", "GET"])
# Email verification link verified with a token
def verified(token):
    # Check to verify the token received from the user email
    # process the user_id for the following script
    user_id = user_class.verify_reset_token(token)

    try:
        usr = User.query.get(user_id)
        usr.verified = True
        db.session.commit()
        if usr.verified:
            qry_usr = User.query.get(user_id)
            if not current_user.is_authenticated:
                login_user(usr)
            flash(f"Welcome, {qry_usr.name}; Please Finish Updating your Profile!!", "success")
            # return redirect(url_for('account'))
    except Exception as e:
        flash(f"Something went wrong, Please try again ", "error")

    return render_template('verified.html')


# Flask route to search for a value in all columns of a table
@app.route('/search', methods=['GET'])
def search_in_table():

    images_qry = Car_Ads_Images

    search_value = request.args.get('search_value')
    table_name = "car_details" #request.args.get('table_name')

    # Get the root directory of the Flask application
    root_dir = os.path.abspath(os.path.dirname(__file__))

    # Construct the path to the SQLite database file inside the instance folder
    db_file_path = os.path.join(root_dir, 'instance', 'car_bids_db.db')

    # conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    query = f"SELECT * FROM {table_name} WHERE (COALESCE(car_make, '') || COALESCE(car_model, '') || COALESCE(vehicle_id_number, '') || COALESCE(year, '')) LIKE ?"
    cursor.execute(query, ('%' + search_value + '%',))
    rows = cursor.fetchall()

    for row in rows:
        print("Car Make: ",row)

    # Convert the results to a list of dictionaries
    results = [{'Column1': row[0], 'Column2': row[1]} for row in rows]

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return render_template('search_results.html',rows=rows,images_qry=images_qry)


# <a class="view_user" href="/user_viewed?id={{ser.dumps({'data6':item.id})}}">View</a>

@app.route('/car_ad_form', methods=["POST","GET"])
@login_required
def car_ad_from():
    print("Car Form Called")
    car_ad_form = Car_Details_Form()
    
    if request.method == "POST":

        # print("Check Images Before: ",request.files.getlist("car_images"))
        if car_ad_form.validate_on_submit():
            car_details = Car_Details(
                    user_id = current_user.id, car_make = car_ad_form.car_make.data,
                    car_model = car_ad_form.car_model.data, car_color = car_ad_form.car_color.data, car_feature1 = car_ad_form.car_feature1.data,
                    car_feature2 = car_ad_form.car_feature2.data, car_feature3 = car_ad_form.car_feature3.data, #,car_images = car_images(request.files.getlist("car_images"))
                    car_feature4 = car_ad_form.car_feature4.data, car_defects = car_ad_form.car_defects.data,
                    year = car_ad_form.year.data, mileage = car_ad_form.mileage.data,token =str(datetime.timestamp(datetime.now())),
                    availability = 1, vehicle_id_number = car_ad_form.vehicle_id_number.data,
                    sale_price = car_ad_form.sale_price.data, payment_terms = car_ad_form.payment_terms.data,
                    negotiation_level = car_ad_form.negotiation_level.data, registration_docs_status = car_ad_form.registration_docs_status.data,
                    registration_docs_due = car_ad_form.registration_docs_due.data,# car_current_defects = car_ad_form.car_current_defects.data,
                    additional_comments = car_ad_form.additional_comments.data,other1 = datetime.now(),other=car_ad_form.usage.data,other2 = car_ad_form.location.data  #location
                    )
            
            #Store image string in Car_Ads_Images db
            
            db.session.add(car_details)
            db.session.commit() 

            car_imgs = []
            for img in car_images(request.files.getlist("car_images")):
                if img:
                    car_img = Car_Images(
                        car_details_id=car_details.id, image_url=img
                    )
                    car_imgs.append(car_img)
            
            if car_imgs:
                db.session.add_all(car_imgs)
                db.session.commit() 
            print("Uploaded Successfully!")
            flash("Uploaded Successfully!","success")
        else:
            if car_ad_form.errors:
                for error in car_ad_form.errors:
                    print("Errors: ", error)

    return render_template("car_ad_form.html",car_ad_form=car_ad_form)

@app.route('/delete_entry')
def delete_entry():
    if request.method == "GET":
        if request.args.get("del"):
            uidel = request.args.get("del")
            id_ = ser.loads(uidel)['data']

            #Check if the user is not currently hired somewhere
            item_to_del = Car_Details.query.get(id_)
            if item_to_del:
                db.session.delete(item_to_del)
                db.session.commit()
                print(f"File Deleted: {item_to_del}")
                flash(f"File Deleted Successfully", "success")
                return redirect(url_for("ads_perfomances"))
            
    return  f"File Deleted"               


@app.route('/car_ad_form_edit', methods=["POST","GET"])
@login_required
def car_ad_form_edit():

    car_ad_form = None

    # id_ = request.args.get()
    # cid = request.args.get("id")
    if request.args.get("id"):
        id_ = ser.loads(request.args.get("id"))['data']
        car_details_query = Car_Details.query.filter_by(id=id_).first()
        car_ad_form = Car_Details_Form(obj=car_details_query)
    # else:
    #     return redirect(url_for("ads_perfomances"))

    if request.method == "POST":
        if car_ad_form.validate_on_submit():
            print("USAGE: ",car_ad_form.other.data )
            car_details_query.car_make = car_ad_form.car_make.data
            car_details_query.car_model = car_ad_form.car_model.data 
            car_details_query.car_color = car_ad_form.car_color.data
            # if request.files.getlist("car_images"):
            #     car_details_query.car_images = car_images(request.files.getlist("car_images"))
            car_details_query.car_feature1 = car_ad_form.car_feature1.data
            car_details_query.car_feature2 = car_ad_form.car_feature2.data 
            car_details_query.car_feature3 = car_ad_form.car_feature3.data
            car_details_query.car_feature4 = car_ad_form.car_feature4.data 
            car_details_query.car_defects = car_ad_form.car_defects.data
            car_details_query.year = car_ad_form.year.data 
            car_details_query.mileage = car_ad_form.mileage.data
            car_details_query.mileage = car_ad_form.mileage.data
            car_details_query.other2 = car_ad_form.location.data
            car_details_query.availability = car_ad_form.availability.data 
            car_details_query.vehicle_id_number = car_ad_form.vehicle_id_number.data
            car_details_query.sale_price = car_ad_form.sale_price.data 
            car_details_query.other = car_ad_form.usage.data 
            car_details_query.payment_terms = car_ad_form.payment_terms.data
            car_details_query.negotiation_level = car_ad_form.negotiation_level.data 
            car_details_query.registration_docs_status = car_ad_form.registration_docs_status.data
            car_details_query.registration_docs_due = car_ad_form.registration_docs_due.data 
            car_details_query.car_defects = car_ad_form.car_defects.data
            car_details_query.additional_comments = car_ad_form.additional_comments.data
            
            # car_imgs = []
            # for img in car_images(request.files.getlist("car_images")):
            #     if img:
            #         car_img = Car_Images(
            #             car_details_id=car_details_query.id, image_url=img
            #         )
            #         car_imgs.append(car_img)
            
            # if car_imgs:
            #     db.session.add_all(car_imgs)
            #     db.session.commit() 

            db.session.commit() 

        else:
            for error in car_ad_form.errors:
                print("ERROR: ", error)
    
    elif request.method =='GET':
        print("Get request to delete imge ")
        # car_details_query = Car_Details.query.filter_by(id=id_).first()
        if request.args.get("img"):
            print("DEBUG IMG ENCRY: ",request.args.get("img"))
            img_num = ser.loads(request.args.get("img"))["data"]
            image_col = "img_"+str(img_num)
            token=request.args.get("err")
            print("DEBUG IMG : ",image_col,"Token: ", token)
            delete =delete_img(image_col,token)
            print("DEBUG DELETE: ",delete) 

    return render_template("car_ad_edit.html",car_ad_form=car_ad_form,car_details_query=car_details_query,images=Car_Ads_Images,car_details_form=car_details_form,op=os)


@app.route('/logout')
def log_out():

    logout_user()

    return redirect(url_for('home'))


@app.route("/car_view_details", methods=["POST", "GET"])
def car_view_details():

    id_ = ser.loads(request.args.get("id"))['data']
    print("DEBUG ID: ",id_)
    car_details_query = Car_Details.query.get(id_)
    related_cars = Car_Details.query.filter_by(car_make=car_details_query.car_make).all()
    images = Car_Ads_Images
    usr = User
    car_user = car_agent_user

    return render_template("car_view_details.html",car_details_query=car_details_query,
                           usr=usr,images=images,related_cars=related_cars,car_user=car_user)


@app.route("/search_view_details", methods=["POST", "GET"])
def search_view_details():

    token_ = request.args.get("id") 
    car_details_query = Car_Details.query.filter_by(token=token_).first()
    print("DEBUG QUERY: ",car_details_query)
    related_cars = Car_Details.query.filter_by(car_make=car_details_query.car_make).all()
    images = Car_Ads_Images
    usr = User
    car_user = car_agent_user

    return render_template("car_view_details.html",car_details_query=car_details_query,
                           usr=usr,images=images,related_cars=related_cars,car_user=car_user)


@app.route('/ads_perfomances', methods=["POST", "GET"])
@login_required
def ads_perfomances():

    agent_car_ads = Car_Details.query.filter_by(user_id=current_user.id).all()
    agent_usr = User
    images = Car_Images
    images_qry = Car_Ads_Images.query.all()

    if request.method == 'POST':
        advert_id = request.form["ad_id"]

        agent_car_ad = Car_Details.query.get(advert_id)

        #Edit availabililty and date_sold columns
        if agent_car_ad.availability:
            agent_car_ad.availability= False
            agent_car_ad.date_sold= datetime.now()
        else:
            agent_car_ad.availability= True
            agent_car_ad.date_sold= None

        db.session.commit()
        return redirect(url_for('ads_perfomances'))
    
    elif request.method == "GET":
        # try:
            if request.args.get("img"):
                print("DEBUG IMG: ",request.args.get("img"))
                img_num = ser.loads(request.args.get("img"))["data"]
                image = "img_"+str(img_num)
                token=request.args.get("err")
                print("DEBUG IMG ENCRY: ",image)
                delete =delete_img(image,token)
                print("DEBUG DELETE: ",delete)
        # except:
        #     pass

    
    def count_ads():
        from sqlalchemy import text

        users = []
        all = text(f"SELECT COUNT(*) as total_jobs FROM car_details where user_id={current_user.id}")
        jobs = db.session.execute(all).scalar()

        return jobs

    return render_template('track_ads_perfomances.html',agent_car_ads=agent_car_ads,agent_usr=agent_usr,images_cls=images,images_qry=images_qry,no_of_ads=count_ads())


@app.route("/spare_item_form", methods=["POST", "GET"])
@login_required
def spare_item_form():

    spares_form = SpareItemForm()

    if request. method == "POST":

        spare_item = Spares(
            item_name=spares_form.item_name.data, item_caption=spares_form.item_caption.data,user_id=current_user.id,
            item_description=spares_form.item_description.data, item_more_info=spares_form.item_more_info.data,
            item_price=spares_form.item_price.data, item_spare_department=spares_form.item_spare_department.data 
            )

        if spares_form.main_img.data:
            spare_item.main_img = process_profile(spares_form.main_img.data)
     
        if spares_form.images1.data:
            spare_item.images1 =  process_profile(spares_form.images1.data)

        if spares_form.images2.data:
            spare_item.images2 = process_profile(spares_form.images2.data)

        db.session.add(spare_item)
        db.session.commit()

        flash("The activity performed was successful!")

    return render_template('spare_item_form.html', spares_item=spares_form, usr=User)


@app.route("/spares_adverts", methods=["POST", "GET"])
def spares_adverts():

    spares = Spares.query.all()
    spares_departments = {depart.item_spare_department for depart in spares}
    print("DEBUG SPARES: ", spares_departments)
    for item in spares:
        print("DEBUG SPARES: ", item.item_name, item.user_id)

    return render_template('spares_adverts.html', spares=spares, agent_user=User,spares_departments = spares_departments )


@app.route("/spare_details_view", methods=["POST", "GET"])
def spare_details_view():

    spare_qry = Spares.query.get(ser.loads(request.args.get('sid'))['data'])
    print("DEBUG SID: ", request.args.get('sid'))
    # spares_departments = {depart.item_spare_department for depart in spares}
    # print("DEBUG SPARES: ", spares_departments)
    # for item in spares:
    #     print("DEBUG SPARES: ", item.item_name, item.user_id)

    return render_template('spare_details_view.html', spare_qry=spare_qry, agent_user=User )


@app.route("/need_spares_manage", methods=["POST", "GET"])
def need_spares_manage():
    pass


@app.route("/need_spares_edit", methods=["POST", "GET"])
def need_spares_edit():

    spares_form = SpareItemForm()

    spare_item_qry = Spares.qury.get(ser.loads(request.args.get("sid"))['data'])

    if request.method == 'POST':

        spare_item_qry.item_name = spares_form.item_name.data
        spare_item_qry.item_caption= spares_form.item_caption.data
        spare_item_qry.item_description = spares_form.item_descrption.data
        spare_item_qry.item_more_info = spares_form.item_more_info.data
        spare_item_qry.item_price = spares_form.item_price.data
        spare_item_qry.item_spare_department = spares_form.item_spare_department.data
        spare_item_qry.main_img = spares_form.main_img.data
        spare_item_qry.image1 = spares_form.image1.data
        spare_item_qry.image2 = spares_form.image2.data

        db.session.commit()

    return render_template('spare_item_edit.html',spares_item = spares_form,spare_item_qry =spare_item_qry)


@app.route("/contact", methods=["POST", "GET"])
def contact_us(user_sentto_mail=None):

    contact_form = Contact_Form()
    if request.method == "POST":
        if contact_form.validate_on_submit():
            def send_link():
                app.config["MAIL_SERVER"] = "smtp.googlemail.com"
                app.config["MAIL_PORT"] = 587
                app.config["MAIL_USE_TLS"] = True
                em = app.config["MAIL_USERNAME"] = os.environ.get("EMAIL")
                if not user_sentto_mail:
                    user_sentto_mail = em
                app.config["MAIL_PASSWORD"] = os.environ.get("PWD")

                mail = Mail(app)

                msg = Message(contact_form.subject.data, sender=em, recipients=[user_sentto_mail])
                msg.body = f"""{contact_form.message.data}\n
{contact_form.email.data}
                    """

                try:
                    mail.send(msg)
                    flash("Your Message has been Successfully Sent!!", "success")
                    return "Email Sent"
                except Exception as e:
                    # print(e)
                    flash(f'Ooops Something went wrong!! Please Retry', 'error')
                    return "The mail was not sent"

                # Send the pwd reset request to the above email
            send_link()

            #print("Posted")
        else:
            flash("Ooops!! Please be sure to fill both email & message fields, correctly","error")

    return render_template("contact.html",contact_form=contact_form)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
