import cv2
import mediapipe as mp
import time
# stage 1
# INITIALISE MEDIAPIPE

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils


# OPEN CAMERA (WINDOWS SAFE)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print(" Camera not opening")
    exit()
#stage 5 variables
output_text=""
last_letter=""
last_time = time.time()
delay=1.0 
#stage 2

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

            # Draw hand landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

           
            # STAGE 3 LOGIC: FINGER UP / DOWN
           
            landmarks = hand_landmarks.landmark

            fingers = []

            # Thumb (special case: x-axis)
            if landmarks[4].x > landmarks[3].x:
                fingers.append(1)
            else:
                fingers.append(0)

            # Index finger
            fingers.append(1 if landmarks[8].y < landmarks[6].y else 0)

            # Middle finger
            fingers.append(1 if landmarks[12].y < landmarks[10].y else 0)

            # Ring finger
            fingers.append(1 if landmarks[16].y < landmarks[14].y else 0)

            # Little finger
            fingers.append(1 if landmarks[20].y < landmarks[18].y else 0)
            #stage 4
            if fingers==[0,0,0,0,0]:
                letter="A"
            elif fingers==[0,1,1,1,1]:
                letter="B"
            elif fingers == [1,1,0,0,0]:
                letter="L"
            elif fingers ==[0,1,1,0,0]:
                letter="U"
            elif fingers ==[0,1,0,0,0]:
                letter="D"
            else:
                letter="Unknown"
            #stage 5
            current_time= time.time()
            if letter != "None":
                if letter == last_letter and current_time- last_time >= delay:
                    output_text += letter
                    last_time = current_time
            elif letter != last_letter:
                last_letter = letter
                last_time = current_time


            # Display finger states
            cv2.putText(
                frame,
                f"Fingers: {fingers}",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            # Display finger count
            cv2.putText(
                frame,
                f"Up Count: {fingers.count(1)}",
                (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

    cv2.imshow("SignSpeak - Finger Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
