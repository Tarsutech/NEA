import cv2
import mediapipe as mp
import time
import pyttsx3
import speech_recognition as sr

# ===============================
# TEXT TO SPEECH (STAGE 6)
# ===============================
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# ===============================
# SPEECH TO TEXT (STAGE 7)
# ===============================
recogniser = sr.Recognizer()
microphone = sr.Microphone()

# ===============================
# MEDIAPIPE HANDS (STAGE 2)
# ===============================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# ===============================
# CAMERA (STAGE 1)
# ===============================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("Camera not opening")
    exit()

# ===============================
# VARIABLES (STAGE 5)
# ===============================
output_text = ""
spoken_text = ""
last_letter = ""
last_time = time.time()
delay = 1.0   # seconds

# ===============================
# MAIN LOOP
# ===============================
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # ===============================
    # HAND PROCESSING (STAGES 3–5)
    # ===============================
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            lm = hand_landmarks.landmark

            # -------------------------------
            # STAGE 3: FINGER LOGIC (ROBUST)
            # -------------------------------
            fingers = []

            # Thumb (works for both hands)
            fingers.append(1 if abs(lm[4].x - lm[3].x) > 0.04 else 0)

            # Other fingers
            fingers.append(1 if lm[8].y < lm[6].y else 0)
            fingers.append(1 if lm[12].y < lm[10].y else 0)
            fingers.append(1 if lm[16].y < lm[14].y else 0)
            fingers.append(1 if lm[20].y < lm[18].y else 0)

            # -------------------------------
            # STAGE 4: LETTER RECOGNITION
            # -------------------------------
            letter = "None"

            if fingers == [0,0,0,0,0]:
                letter = "A"
            elif fingers == [0,1,1,1,1]:
                letter = "B"
            elif fingers == [1,1,0,0,0]:
                letter = "L"
            elif fingers == [0,1,1,0,0]:
                letter = "U"
            elif fingers == [0,1,0,0,0]:
                letter = "D"

            # -------------------------------
            # STAGE 5: STABILITY CHECK
            # -------------------------------
            current_time = time.time()

            if letter != "None":
                if letter == last_letter and current_time - last_time >= delay:
                    output_text += letter
                    last_time = current_time
                elif letter != last_letter:
                    last_letter = letter
                    last_time = current_time

            # DEBUG (REMOVE LATER IF YOU WANT)
            cv2.putText(
                frame,
                f"Fingers: {fingers}",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

    # ===============================
    # DISPLAY OUTPUT
    # ===============================
    cv2.putText(frame, f"Signed Text: {output_text}", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)

    cv2.putText(frame, f"Spoken Text: {spoken_text}", (10, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    cv2.putText(frame,
                "C: Speak | V: Voice input | R: Reset | Q: Quit",
                (10, 170),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,0), 2)

    cv2.imshow("SignSpeak - Final System", frame)

    key = cv2.waitKey(1) & 0xFF

    # ===============================
    # CONTROLS (STAGES 6–7)
    # ===============================
    if key == ord('q'):
        break

    if key == ord('r'):
        output_text = ""
        spoken_text = ""
        last_letter = ""

    # STAGE 6: TEXT TO SPEECH
    if key == ord('c') and output_text != "":
        engine.say(output_text)
        engine.runAndWait()

    # STAGE 7: SPEECH TO TEXT
    if key == ord('v'):
        with microphone as source:
            recogniser.adjust_for_ambient_noise(source)
            audio = recogniser.listen(source)

        try:
            spoken_text = recogniser.recognize_google(audio)
        except:
            spoken_text = "Speech not recognised"

# ===============================
# CLEAN UP
# ===============================
cap.release()
cv2.destroyAllWindows()

