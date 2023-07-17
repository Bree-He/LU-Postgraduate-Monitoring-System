# set up gmail smtp
from main import app
from flask_mail import Mail, Message
from threading import Thread

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'comp639grp17@gmail.com'
app.config['MAIL_PASSWORD'] = 'hkqvfwrxisajolrp'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# use flask_mail
mail = Mail(app)

def sendMail(emailTitle, recipientsEmail, bodyContent):
    msg = Message(emailTitle, sender =('Group16 System Message', 'comp639grp17@gmail.com'), recipients = [recipientsEmail])
    msg.body = bodyContent
    thr = Thread(target=send_async_email, args=[app, msg]) 
    # the target parameter is set to the send_async_email function, which is the function that will be executed in the new thread.
    # the args parameter is set to a list that contains two elements: the app object and the msg object. These arguments will be passed to the send_async_email function when it is executed in the new thread.
    thr.start()

# to send an email asynchronously, by running the email sending function in a separate thread, the Flask application can continue processing requests without waiting for the email to be sent.
def send_async_email(app, msg):
    with app.app_context(): # create a new application context. This is necessary because Flask-Mail needs access to the Flask application context in order to send the email.
        mail.send(msg)

# set up upload
import os
# from flask_dropzone import Dropzone
import imghdr
from werkzeug.utils import secure_filename

# config upload
# app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 # file max size = 1 mb
app.config['UPLOAD_EXTENSIONS'] = '.png, .jpg, .jpeg' # allowed file types
app.config['MAX_FILES'] = 1

# use flask_dropzone
# dropzone = Dropzone(app)

def upload_path(role):
    base_path = "./main/" # relative path
    if role == 'Postgraduate Administrator':
        upload_path = os.path.join(base_path, 'admin', 'static', 'uploads')
    elif role == 'Student':
        upload_path = os.path.join(base_path, 'student', 'static', 'uploads')
    elif role == 'Supervisor':
        upload_path = os.path.join(base_path, 'supervisor', 'static', 'uploads')
    elif role == 'Convenor':
        upload_path = os.path.join(base_path, 'convenor', 'static', 'uploads')
    elif role == 'Postgraduate Chair':
        upload_path = os.path.join(base_path, 'chair', 'static', 'uploads')
    return upload_path

def validate_image(stream): # check if the file is real image file
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

def allowed_file(filename): # check if the file is in allowed file extensions
    allowed_extensions = app.config['UPLOAD_EXTENSIONS']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def upload_file(file, role, user_name):
    if file.filename == '':
        msg = 'Please choose the file!'
        return msg
    elif file and allowed_file(file.filename) and validate_image(file.stream):
        extension = os.path.splitext(file.filename)[1] # get the extension of the image that user uploaded(.png, .jpg, or .jpeg)
        new_filename = secure_filename(user_name.lower()) + extension # set user_name into lower case
        file_path = os.path.join(upload_path(role), new_filename).replace('\\', '/') # replace the default path "\" to "/"
        file.save(file_path) # image save into the nominated folder
        relative_path = (f"uploads/" + new_filename) #relative path is going to save in MySQL and use at front-end
        msg = 'Image uploaded!'
        return relative_path, msg
    else:
        msg = 'Allowed png, jpg, and jpeg files only, within 3MB!'
        return msg