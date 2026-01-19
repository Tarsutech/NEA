import cv2
import mediapipe as mp
import time
import pyttsx3


# STAGE 1: INITIALISE MEDIAPIPE


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils


# STAGE 2: OPEN CAMERA


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera not opening")
    exit()


# STAGE 5: VARIABLES


output_text = ""
last_letter = ""
last_time = time.time()
delay = 1.0


# INITIALISE TEXT TO SPEECH


engine = pyttsx3.init()
engine.setProperty('rate', 150)


# MAIN LOOP


while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # DRAW HAND LANDMARKS
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

          
            # STAGE 3: FINGER LOGIC PLACEHOLDER
           
            # (You can add finger counting / sign detection here)
            pass

    # DISPLAY WINDOW
    

    cv2.imshow("Hand Tracking", frame)

  
    # EXIT ON Q
   

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# CLEAN UP


cap.release()
cv2.destroyAllWindows()
