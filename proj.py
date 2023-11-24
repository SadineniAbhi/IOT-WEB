import cv2
import face_recognition
import pygame
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import ArdChip as ab
EMAIL_ADDRESS = 'arundaniel.aac@gmail.com'
EMAIL_PASSWORD = 'oraa jnhl tdax gyek'
RECIPIENT_EMAIL = 'arundaniel.aac@gmail.com'

def process_unmatched_face(frame):
    def send_email_with_image(image_data):
        global door_locked  # Access the global variable

        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = 'Unmatched Face Capture'

        body = "We detected an unmatched face. Check the attached image."

        # Adding HTML content with lock and unlock buttons
        html_content = """
        <html>
          <body>
            <p>{body}</p>
            <img src="cid:image" alt="Unmatched Face" width="50%">
            <br><br>
            <button type="button" onclick="handleButtonClick('lock')">Lock Door</button>
            <button type="button" onclick="handleButtonClick('unlock')">Unlock Door</button>

            <script>
              function handleButtonClick(action) {
                // Perform actions based on the button click
                if (action === 'lock') {
                  console.log('Lock Door button clicked');
                  // Add code for the Lock Door action
                } else if (action === 'unlock') {
                  console.log('Unlock Door button clicked');
                  // Add code for the Unlock Door action
                }
              }
            </script>
          </body>
        </html>
        """

        # You can use the variable 'html_content' as needed in your Python script.

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
    match = False
    if face_encodings:
        matches = face_recognition.compare_faces([known_encoding], face_encodings[0])

        if matches[0]:
            print("Yes, face matched!")
            doorbell_counter = 0
            match = True
        else:
            print("No, face not matched")
            process_unmatched_face(frame)
        ab.set(match)
    if cv2.waitKey(1) != -1:
        break

video_capture.release()
cv2.destroyAllWindows()