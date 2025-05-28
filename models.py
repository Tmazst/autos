
# from alchemy_db import db.Model
from sqlalchemy import  MetaData, ForeignKey
from flask_login import login_user, UserMixin
from sqlalchemy.orm import backref, relationship
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# from app import app

db = SQLAlchemy()


#from app import login_manager

metadata = MetaData()

#Users class, The class table name 'h1t_users_cvs'
class User(db.Model,UserMixin):

    __table_args__ = {'extend_existing': True}

    #Create db.Columns
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    image = db.Column(db.String(30), nullable=True)
    contacts = db.Column(db.String(20))
    whatsapp = db.Column(db.String(50))
    email = db.Column(db.String(120),unique=True)
    password = db.Column(db.String(120), unique=True)
    confirm_password = db.Column(db.String(120), unique=True)
    verified = db.Column(db.Boolean, default=False)
    # timestamp = db.Column(db.DateTime(), default=datetime.now)
    role = db.Column(db.String(120))
    spares_id = relationship("Spares",backref="User",lazy=True)
    # project_briefs = relationship("Project_Brief", backref="Project_Brief", lazy=True)

    __mapper_args__={
        "polymorphic_identity":'user',
        'polymorphic_on':role
    }


class car_agent_user(User):

    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    facebook = db.Column(db.String(50))
    personal_id_no = db.Column(db.Integer())
    date_of_birth = db.Column(db.DateTime())
    address = db.Column(db.String(120))
    free_trial = db.Column(db.Boolean())
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    zip_code =  db.Column(db.Boolean())
    other = db.Column(db.String(120)) #Resume
    # jobs_applied_for = relationship("Applications", backref='Applications.job_title', lazy=True)
    cars = relationship("Car_Details", backref='Car_Details', lazy=True)

    __mapper_args__={
            "polymorphic_identity":'car_agent_user'
        }


class Mechanics(User):

    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    facebook = db.Column(db.String(50))
    personal_id_no = db.Column(db.Integer())
    free_trial = db.Column(db.Boolean())
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    specialty = db.Column(db.String(50))
    address = db.Column(db.String(120))
    more_info = db.Column(db.String(255))

    __mapper_args__={
            "polymorphic_identity":'mechanic_user'
        }


class admin_user(User):

    id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
    # contacts = db.Column(db.String(20))
    date_of_birth = db.Column(db.DateTime())
    address = db.Column(db.String(120))
    other = db.Column(db.String(120)) #Resume
    # jobs_applied_for = relationship("Applications", backref='Applications.job_title', lazy=True)
    # hired_user = relationship("hired", backref='Hired Applicant', lazy=True)

    __mapper_args__={
            "polymorphic_identity":'admin_user'
        }


class Car_Details(db.Model,UserMixin):

    __tablename__= "car_details"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,ForeignKey('user.id'))
    car_make = db.Column(db.String(120))
    car_model = db.Column(db.String(120))
    car_color = db.Column(db.String(120))
    car_images = db.Column(db.String(500))
    car_feature1 = db.Column(db.String(120))
    car_feature2 = db.Column(db.String(120))
    car_feature3 = db.Column(db.String(120))
    car_feature4 = db.Column(db.String(120))#fuel type
    car_defects = db.Column(db.String(200))
    year = db.Column(db.Date())
    mileage = db.Column(db.Integer)
    availability = db.Column(db.Boolean(),default=True)
    date_sold = db.Column(db.Date())
    vehicle_id_number = db.Column(db.String(120))
    sale_price = db.Column(db.Float)
    car_current_defects = db.Column(db.String(200))
    payment_terms = db.Column(db.String(120))
    negotiation_level = db.Column(db.String(120))
    registration_docs_status = db.Column(db.String(120))
    registration_docs_due = db.Column(db.Float)
    additional_comments = db.Column(db.String(200))
    token=db.Column(db.String(120), nullable=False)
    other=db.Column(db.String(120)) # Usage
    other1=db.Column(db.Date()) #Date Posted
    other2=db.Column(db.String(120))# Location
    token = db.Column(db.String(120))
    server_details = relationship("Car_Server_Details", backref='car_details_parent', lazy=True)
    payment_records = relationship("Car_Payment_Records", backref='car_details', lazy=True)
    car_images_rs  = relationship("Car_Images", backref='car_details_images', lazy=True)

class Car_Images(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    car_details_id = db.Column(db.Integer, ForeignKey("car_details.id"))
    image_url = db.Column(db.String(120), nullable=False)

#Not used
class Car_Ads_Images(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    car_details_id=db.Column(db.Integer, ForeignKey("car_details.id"))
    token=db.Column(db.String(120), nullable=False)
    img_1 = db.Column(db.String(120))
    img_2 = db.Column(db.String(120))
    img_3= db.Column(db.String(120))
    img_4 = db.Column(db.String(120))
    img_5 = db.Column(db.String(120))
    img_6 = db.Column(db.String(120))
    img_7 = db.Column(db.String(120))
    img_8 = db.Column(db.String(120))
    img_9 = db.Column(db.String(120))
    img_10 = db.Column(db.String(120))


class Car_Server_Details(db.Model,UserMixin):

    __tablename__= "car_server_details"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,ForeignKey('user.id'))
    car_details = db.Column(db.Integer,ForeignKey('car_details.id'))
    sale_token = db.Column(db.String(120))
    car_deal_opened = db.Column(db.String(120))
    car_deal_closed = db.Column(db.String(120))
    car_selling_price_agr = db.Column(db.Float)
    other=db.Column(db.String(120))
    other1=db.Column(db.String(120))
    other2=db.Column(db.String(120))
    payment_records = relationship("Car_Payment_Records", backref='car_server_details', lazy=True)


class Car_Payment_Records(db.Model,UserMixin):

    __tablename__= "car_payment_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    car_details_id = db.Column(db.Integer, ForeignKey('car_details.id'))
    server_details_id = db.Column(db.Integer, ForeignKey('car_server_details.id'))
    buyer_details = db.Column(db.String(120), ForeignKey('user.id'))
    sale_token = db.Column(db.String(120))
    deposit = db.Column(db.Numeric)
    paid_amount = db.Column(db.Float)
    paid_date = db.Column(db.Float)
    paid_balance = db.Column(db.Float)
    other=db.Column(db.String(120))
    other1=db.Column(db.String(120))
    other2=db.Column(db.String(120))


class User_Subscription_Records(db.Model,UserMixin):

    __tablename__= "user_subscription_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('car_server_details.id'))
    subscription_option = db.Column(db.String(120))
    subscription = db.Column(db.Float)
    subscription_date = db.Column(db.Float)
    paid_balance = db.Column(db.Float)
    other=db.Column(db.String(120))
    other1=db.Column(db.String(120))
    other2=db.Column(db.String(120))


# Reference 
class Subscription_Options(db.Model,UserMixin):

    __tablename__= "subscription_options"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    options_1 = db.Column(db.Float)
    options_2 = db.Column(db.Float)
    options_3 = db.Column(db.Float)
    free_trial = db.Column(db.Float)
    other=db.Column(db.String(120))
    other1=db.Column(db.String(120))
    other2=db.Column(db.String(120))


class Spares(db.Model,UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    item_name = db.Column(db.String(120))
    item_caption = db.Column(db.String(120))
    item_description = db.Column(db.String(255))
    item_more_info = db.Column(db.String(255))
    item_price = db.Column(db.Float)
    item_spare_department = db.Column(db.String(120))
    item_other2 = db.Column(db.String(120))#Item condition
    item_other3 = db.Column(db.String(120))#Model
    item_other4 = db.Column(db.String(120))#pn
    item_other5 = db.Column(db.Integer)
    item_other6 = db.Column(db.Float)
    main_img = db.Column(db.String(120))
    images1 = db.Column(db.String(120))
    images2 = db.Column(db.String(120))
    # timestamp = db.Column(db.DateTime(25))



