from flask import Flask, render_template, request, redirect, url_for , session
import firebase_admin
import time
from firebase_admin import credentials, firestore
import random
from sendgps import app as gps_app
from sos import main


app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("path to json file..")
firebase_admin.initialize_app(cred)

db = firestore.client()

THRESHOLD_COUNT = 5
TIME_WINDOW = 24 * 60 * 60

def validate_incident(category):
    current_time = int(time.time())
    incidents_ref = db.collection('incidents')
    query = incidents_ref.where('category', '==', category).where('timestamp', '>=', current_time - TIME_WINDOW)
    incident_count = len(query.get())
    return incident_count >= THRESHOLD_COUNT


@app.route('/')
def index():
    return render_template('send_otp.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    phone = request.form['phone']
    
    # Generate a 6-digit OTP
    otp = str(random.randint(100000, 999999))
    
    # Store the OTP in Firebase
    otp_data = {"otp": otp}
    db.collection("otps").document(phone).set(otp_data)
    
    # Simulate sending OTP via SMS (replace this with your own logic)
    print(f"Sent OTP {otp} to {phone}")
    
    return render_template('verify_otp.html', phone=phone)

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    phone = request.form['phone']
    user_otp = request.form['otp']
    
    # Retrieve the stored OTP from Firebase
    otp_ref = db.collection("otps").document(phone)
    stored_otp = otp_ref.get().to_dict()["otp"]
    
    if stored_otp and user_otp == stored_otp:
        # OTP is valid
        # Register user and store data in Firebase
        name = request.form['name']
        
        
        # Store user data in Firebase
        user_data = {"name": name, "phone": phone}
        db.collection("users").add(user_data)
        
        # Delete the OTP after successful verification
        otp_ref.delete()
        
        return redirect(url_for('successful_registration'))
    else:
        return "Invalid OTP. Please try again."
    
@app.route('/successful_registration')
def successful_registration():
        if request.method == 'POST':
            selected_category = request.form.get('selected_category')  # Get the selected category
            
            # if selected_category == 'security and crime':
            #     # Redirect to the send_gps route in the sendgps.py app
            #     return redirect(url_for('send_gps', _external=True)) # send gps cords
            #     main() #send sos message

            if validate_incident(selected_category):
                # Trigger SOS
                return redirect(url_for('send_gps', _external=True))
                main()
                return redirect(url_for('successful_registration'))
            else:
                # Store the incident
                incident_data = {
                    "category": selected_category,
                    "timestamp": int(time.time())
                }
                db.collection('incidents').add(incident_data)
                
                return redirect(url_for('successful_registration'))

        return render_template('successful_registration.html')

if __name__ == '__main__':
    app.run(debug=True)
