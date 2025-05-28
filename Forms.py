from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, TextAreaField,BooleanField, SelectField,DateField, \
                        URLField,IntegerField,FloatField,MultipleFileField,TelField
from wtforms.validators import DataRequired,Length,Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from flask_login import current_user
from flask_wtf.file import FileField , FileAllowed
# from wtforms.fields.html5 import DateField,DateTimeField


class Register(FlaskForm):

    name = StringField('name', validators=[DataRequired(),Length(min=2,max=20)])
    user_email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=64)])
    confirm = PasswordField('confirm', validators=[DataRequired(),EqualTo('password'), Length(min=8, max=64)])
    contacts = TelField('Contact(s)', validators=[Length(min=8, max=64)])
    mechanic_bool = BooleanField('Register as a Mechanic?')

    Submit = SubmitField('Create Account!')

    def validate_email(self,email):
        from app import db, User,app
        # with db.init_app(app):
        user_email = User.query.filter_by(email = self.user_email.data).first()
        if user_email:
            return ValidationError(f"Email already registered in this platform")


class Mechanics(FlaskForm):

    image_pfl = FileField('Profile Image', validators=[FileAllowed(["jpeg",'jpg','png'])])
    facebook = URLField('Facebook Link')
    personal_id_no = StringField('Physical Address')
    specialty = StringField('Field of specialization')
    address = StringField('Field of specialization')
    more_info = TextAreaField("Message",validators=[Length(min=0, max=500)])
    Update = SubmitField('Create Account!')


class Mechanics_Acc(FlaskForm):

    name = StringField('name', validators=[DataRequired(),Length(min=2,max=20)])
    image_pfl = FileField('Profile Image', validators=[FileAllowed(["jpeg",'jpg','png'])])
    facebook = URLField('Facebook Link')
    personal_id_no = StringField('Physical Address')
    specialty = StringField('Field of specialization')
    address = StringField('Physical')
    contacts = TelField('Contact(s)', validators=[Length(min=8, max=64)])
    more_info = TextAreaField("Message",validators=[Length(min=0, max=500)])
    Update = SubmitField('Update')
 

class Account(FlaskForm):

    name = StringField('name', validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('email', validators=[DataRequired(),Email()])
    zip_code = StringField('Zip Code / Postal Code', validators=[Length(min=0, max=64)])
    date_of_birth = DateField('Date of Birth:', format="%Y-%m-%d")
    contacts = TelField('Contact(s)', validators=[Length(min=8, max=64)])
    personal_id_no = IntegerField("ID No.")
    image_pfl = FileField('Profile Image', validators=[FileAllowed(["jpeg",'jpg','png'])])
    address = StringField('Physical Address', validators=[DataRequired(), Length(min=4, max=30)])
    whatsapp = TelField('Whatsapp')
    facebook = URLField('Facebook Link')
    Update = SubmitField('Create Account!')


class Login(FlaskForm):

    user_email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=64)])
    Submit = SubmitField('Login')


class Reset(FlaskForm):

    old_password = PasswordField('old password', validators=[DataRequired(), Length(min=8, max=64)])
    new_password = PasswordField('new password', validators=[DataRequired(), Length(min=8, max=64)])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('new_password'), Length(min=8, max=64)])
    reset = SubmitField('Reset')


class Reset_Request(FlaskForm):

    email = StringField('email', validators=[DataRequired(), Email()])
    reset = SubmitField('Submit')


class Contact_Form(FlaskForm):

    name = StringField('name')
    email = StringField('email', validators=[DataRequired(),Email()])
    subject = StringField("subject")
    message = TextAreaField("Message",validators=[Length(min=8, max=2000)])
    submit = SubmitField("Send")


class Car_Details_Form(FlaskForm):

    car_make = SelectField('Car Brand', validators=[DataRequired()], choices=[
        ('audi', 'Audi'),('bmw', 'BMW'),('ford', 'Ford'),
        ('honda', 'Honda'),('toyota', 'Toyota'),('mercedes', 'Mercedes-Benz'),
        ('volkswagen', 'Volkswagen'),('nissan', 'Nissan'),('chevrolet', 'Chevrolet'),
        ('kia', 'Kia'),('hyundai', 'Hyundai'),('subaru', 'Subaru'),
        ('tesla', 'Tesla'),('lexus', 'Lexus'),('infiniti', 'Infiniti'),
        ('fiat', 'Fiat'),('jeep', 'Jeep'),('mazda', 'Mazda'),
        ('volvo', 'Volvo'),('porsche', 'Porsche'),('dodge', 'Dodge'),
        ('cadillac', 'Cadillac'),('buick', 'Buick'),('gmc', 'GMC'),
        ('chrysler', 'Chrysler'),('acura', 'Acura'),('land_rover', 'Land Rover'),
        ('jaguar', 'Jaguar'),('mitsubishi', 'Mitsubishi'),('mini', 'Mini'),
        ('alfa_romeo', 'Alfa Romeo'),('write', 'Write-In Option')
    ])
    car_model = StringField('Car Model', validators=[DataRequired(), Length(min=4, max=50)])
    car_color = StringField('Car Color(s)', validators=[DataRequired(), Length(min=4, max=50)])
    year = DateField('Date of Birth:', format="%Y-%m-%d")
    mileage = IntegerField("Mileage")
    usage = StringField("Usage") #Change to string
    car_images = MultipleFileField("Upload Car Images", validators=[FileAllowed(['webm', 'png', 'jpg', 'jpeg', 'gif'])]) #widget= _Widget[MultipleFileField] ,file_allowed=".webm,.png, .jpg, .jpeg, .gif"
    availability = BooleanField("Availability Status")
    date_sold = DateField('Date Sold:', format="%Y-%m-%d")
    vehicle_id_number = StringField('VIN', validators=[DataRequired(), Length(min=8, max=100)])
    sale_price = FloatField("Sale Price")
    payment_terms = SelectField('Payment Terms',
                                  choices=[("Full Amount", "Full Amount"), ("Full Amount after Evaluation", "Full Amount after Evaluation"),
                                           ("Full Amount if Negotiations", "Full Amount if Negotiations"),("2 Months", "2 Months"),("3 Months", "3 Months"),("Deposit + 6 Months", "Deposit + 6 Months"),
                                           ("Deposit + 3 Months", "Deposit + 3 Months"),("Deposit + 2 Months", "Deposit + 2 Months"),
                                           ("Deposit + 1 Months", "Deposit + 1 Months"),("6 Months", "6 Months"),("12 Months", "12 Months")
                                           ,("24 Months", "24 Months"),("3 Years", "3 Years"),("5 Years", "5 Years")])
    car_feature1 = StringField('Car Feature')
    car_feature2 = StringField('Body Type')
    car_feature3 = StringField('Car Feature')
    car_feature4 = StringField('Fuel Type')
    negotiation_level = SelectField('Negotiation Level',
                                  choices=[("Non Negotiable", "Non Negotiable"), ("Partially Negotiable", "Partially Negotiable"),
                                           ("Negotiable", "Negotiable"),("Negotiable after Evaluation", "Negotiable after Evaluation"),
                                           ("Negotiable if Pay in Full", "Negotiable if Pay in Full"),])
    registration_docs_status = SelectField('Vehicle Documents Status',
                                  choices=[("All Documents Ready", "All Documents Ready"), ("Only Not Licenced", "Only Not Licenced"),("Only Not Licenced", "Only Not Licenced"),
                                           ("Clean but Foreign Registered(SA)", "Clean but Foreign Registered(SA)"),("Clean but Foreign Registered", "Clean but Foreign Registered"),
                                           ("Clean but Foreign Registered(SA)", "Clean but Foreign Registered(SA)")])
    registration_docs_due = FloatField('Vehicle Documents Owed')
    additional_comments =  TextAreaField("Comments")
    location = StringField(validators=[DataRequired(), Length(min=4, max=50)])
    car_defects = TextAreaField("Current Car Faults")
    Submit = SubmitField('Submit')
    other=StringField()
    other1=StringField()
    other2=StringField()
    main_image = FileField('Replace Image', validators=[FileAllowed(["jpeg",'jpg','png'])])


class SpareItemForm(FlaskForm):
    
    item_name = StringField('Item Name', validators=[Length(max=50)])
    item_caption = StringField('Caption', validators=[Length(max=50)])
    item_description = TextAreaField('Describe', validators=[Length(max=255)])
    item_more_info = TextAreaField('More Info', validators=[Length(max=255)])
    item_price = FloatField('Price')
    item_spare_department = StringField('Spare Family', validators=[Length(max=255)])
    item_other2 = SelectField('Condition', choices=[("New","New"),("Second Hand","Second Hand")], validators=[Length(max=255)])
    item_other3 = StringField('Model', validators=[Length(max=50)])
    item_other4 = StringField('Part No.', validators=[Length(max=50)])
    main_img = FileField('Upload Main Pic:', validators=[FileAllowed(['jpg','png',"jpeg","gif","webp","svg","bmp","tiff","tif","heic"])])
    images1 = FileField('Other Picture:', validators=[FileAllowed(['jpg','png',"jpeg","gif","webp","svg","bmp","tiff","tif","heic"])])
    images2 = FileField('Other Picture:', validators=[FileAllowed(['jpg','png',"jpeg","gif","webp","svg","bmp","tiff","tif","heic"])])
    submit = SubmitField('Submit')

