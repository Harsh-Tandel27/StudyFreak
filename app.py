import os
import datetime
import cv2
from flask import Flask, jsonify, request, render_template
import face_recognition
import json
from groq import Groq


app = Flask(__name__)

REGISTERED_DATA_FILE = "registered_data.txt"

def load_registered_data():
    if os.path.exists(REGISTERED_DATA_FILE):
        with open(REGISTERED_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def save_registered_data(data):
    with open(REGISTERED_DATA_FILE, "w") as file:
        json.dump(data, file)

registered_data = load_registered_data()

@app.route("/face")
def face():
    return render_template("face.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/loginpage")
def loginpage():
    return render_template("login.html")
@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/firstyr")
def firstyr():
    return render_template("first_yr.html")

@app.route("/secyr")
def secyr():
    return render_template("second_yr.html")

@app.route("/thirdyr")
def thirdyr():
    return render_template("third_yr.html")


@app.route("/register", methods=["POST"])
def register():
    try:
        name = request.form.get("name")
        photo = request.files['photo']

        uploads_folder = os.path.join(os.getcwd(), "static", "uploads","registered")

        if not os.path.exists(uploads_folder):
            os.makedirs(uploads_folder)

        photo_path = os.path.join(uploads_folder, f'{datetime.date.today()}_{name}.jpg')
        photo.save(photo_path)

        registered_data[name] = {"photo_path": photo_path, "date_registered": str(datetime.date.today())}
        save_registered_data(registered_data)

        response = {"success": True, 'name': name}
        return jsonify(response)
    except Exception as e:
        # Log the exception for debugging
        print(f"Exception in register route: {e}")
        response = {"success": False, "error": "Internal Server Error"}
        return jsonify(response)

@app.route("/login", methods=["POST"])
def login():
    try:
        photo = request.files['photo']
        uploads_folder = os.path.join(os.getcwd(), "static", "uploads","logins")

        if not os.path.exists(uploads_folder):
            os.makedirs(uploads_folder)

        login_filename = os.path.join(uploads_folder, "login_face.jpg")
        photo.save(login_filename)

        login_image = cv2.imread(login_filename)
        gray_image = cv2.cvtColor(login_image, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            response = {"success": False, "error": "No face detected in the login photo"}
            return jsonify(response)

        login_image = face_recognition.load_image_file(login_filename)
        login_face_encodings = face_recognition.face_encodings(login_image)

        for name, data in registered_data.items():
            registered_photo = data["photo_path"]
            registered_image = face_recognition.load_image_file(registered_photo)
            registered_face_encodings = face_recognition.face_encodings(registered_image)

            if len(registered_face_encodings) > 0 and len(login_face_encodings) > 0:
                matches = face_recognition.compare_faces(registered_face_encodings, login_face_encodings[0])

                if any(matches):
                    response = {"success": True, "name": name}
                    return jsonify(response)

        response = {"success": False, "error": "No matching face found in registered data"}
        return jsonify(response)

    except Exception as e:
        # Log the exception for debugging
        print(f"Exception in login route: {e}")
        response = {"success": False, "error": "Internal Server Error"}
        return jsonify(response)

@app.route("/success")
def success():
    user_name = request.args.get("user_name")
    return render_template("index.html", user_name=user_name)




def index():
    return render_template('home.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    try:
        data = request.form['user_input']
        print("Received data:", data)  # Print the received data to the terminal

        # Initialize Groq client
        client = Groq(api_key="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")

        # Generate chat completion
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": data}],
            model="mixtral-8x7b-32768",
        )

        completion_text = chat_completion.choices[0].message.content
        print("Generated completion:", completion_text)

        return jsonify({"success": True, "completion": completion_text})

    except Exception as e:
        print(f"Error processing input: {e}")
        return jsonify({"success": False, "error": "Internal Server Error"})


if __name__ == '__main__':
    app.run(debug=True)

