import cv2
import face_recognition
import pygame
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from flask import Flask, request, jsonify
from ArdChip import set

EMAIL_ADDRESS = 'arundaniel.aac@gmail.com'
EMAIL_PASSWORD = 'oraa jnhl tdax gyek'
RECIPIENT_EMAIL = 'arundaniel.aac@gmail.com'

def process_unmatched_face(frame):
    def send_email_with_image(image_data):
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = 'Unmatched Face Capture'

        body = "We detected an unmatched face. Check the attached image."

        # Adding HTML content with lock and unlock buttons
        html_content = f"""
        <html>
          <body>
            <p>{body}</p>
            <img src="cid:image" alt="Unmatched Face" width="50%">
            <br><br>
            <a href="{"www.google.com"}" target="_blank">
              <button type="button">Visit Another URL</button>
            </a>
          </body>
        </html>
        """

        msg.attach(MIMEText(html_content, 'html'))

        image = MIMEImage(image_data, name='captured_image.jpg')
        image.add_header('Content-ID', '<image>')
        msg.attach(image)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            text = msg.as_string()
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, text)
            server.quit()
            print("Email sent successfully!")

        except Exception as e:
            print(f"Email could not be sent. Error: {e}")

    def ring_doorbell():
        pygame.mixer.init()
        pygame.mixer.music.load("Doorbell.wav")

        for _ in range(3):
            pygame.mixer.music.play()
            pygame.time.wait(1000)

        pygame.mixer.quit()

    ring_doorbell()
    _, buffer = cv2.imencode('.jpg', frame)
    image_bytes = buffer.tobytes()
    send_email_with_image(image_bytes)


known_image = face_recognition.load_image_file("Danny.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

video_capture = cv2.VideoCapture(0)

doorbell_counter = 0
match = False  # Initial state (door locked)

while True:
    ret, frame = video_capture.read()

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    if face_encodings:
        matches = face_recognition.compare_faces([known_encoding], face_encodings[0])

        if matches[0]:
            print("Yes, face matched!")
            doorbell_counter = 0
            door_locked = True  # Update the state (door locked)
        else:
            print("No, face not matched")
            process_unmatched_face(frame)
            door_locked = False  # Update the state (door unlocked)

        set(door_locked)  # Update the match variable in ArdChip module

    if cv2.waitKey(1) != -1:
        break

video_capture.release()
cv2.destroyAllWindows()


import cv2
import face_recognition
import pygame
from flask import Flask, request
from ArdChip import set

app = Flask(__name__)

door_locked = True  # Initial state (door locked)

def process_unmatched_face(frame):
    def send_email_with_image(image_data):
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = 'Unmatched Face Capture'

        body = "We detected an unmatched face. Check the attached image."

        # Adding HTML content with lock and unlock buttons
        html_content = f"""
        <html>
          <body>
            <p>{body}</p>
            <img src="cid:image" alt="Unmatched Face" width="50%">
            <br><br>
            <a href="file:///C:/Users/arunb/OneDrive/Desktop/AACprj.html" target="_blank">
              <button type="button">Visit Another URL</button>
            </a>
          </body>
        </html>
        """

        msg.attach(MIMEText(html_content, 'html'))

        image = MIMEImage(image_data, name='captured_image.jpg')
        image.add_header('Content-ID', '<image>')
        msg.attach(image)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            text = msg.as_string()
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, text)
            server.quit()
            print("Email sent successfully!")

        except Exception as e:
            print(f"Email could not be sent. Error: {e}")

    def ring_doorbell():
        pygame.mixer.init()
        pygame.mixer.music.load("Doorbell.wav")

        for _ in range(3):
            pygame.mixer.music.play()
            pygame.time.wait(1000)

        pygame.mixer.quit()

    ring_doorbell()
    _, buffer = cv2.imencode('.jpg', frame)
    image_bytes = buffer.tobytes()
    send_email_with_image(image_bytes)

known_image = face_recognition.load_image_file("Danny.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

video_capture = cv2.VideoCapture(0)

doorbell_counter = 0

while True:
    ret, frame = video_capture.read()

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    if face_encodings:
        matches = face_recognition.compare_faces([known_encoding], face_encodings[0])

        if matches[0]:
            print("Yes, face matched!")
            doorbell_counter = 0
            door_locked = True  # Update the state (door locked)
        else:
            print("No, face not matched")
            process_unmatched_face(frame)
            door_locked = False  # Update the state (door unlocked)

        set(door_locked)  # Update the state in ArdChip module

    if cv2.waitKey(1) != -1:
        break

video_capture.release()
cv2.destroyAllWindows()

@app.route('/handle_button_click', methods=['POST'])
def handle_button_click():
    global door_locked
    data = request.get_json()
    action = data.get('action')
    print(f'Button clicked: {action}')

    if action == 'unlock':
        door_locked = False
        print("True")  # Print True when Unlock Door button is clicked
    else:
        door_locked = True
        print("False")  # Print False when Lock Door button is clicked

    return jsonify({'status': 'OK'})