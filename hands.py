import cv2
import mediapipe as mp


def init_hands(
    max_num_hands: int = 2,
    min_detection_confidence: float = 0.7,
    min_tracking_confidence: float = 0.7,
):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=max_num_hands,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )
    mp_draw = mp.solutions.drawing_utils
    return hands, mp_hands, mp_draw


def process_frame(frame, hands):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return hands.process(rgb)


def get_fingers(landmarks) -> list:
    fingers = []

    # Thumb (works for both hands)
    fingers.append(1 if abs(landmarks[4].x - landmarks[3].x) > 0.04 else 0)

    # Other fingers
    fingers.append(1 if landmarks[8].y < landmarks[6].y else 0)
    fingers.append(1 if landmarks[12].y < landmarks[10].y else 0)
    fingers.append(1 if landmarks[16].y < landmarks[14].y else 0)
    fingers.append(1 if landmarks[20].y < landmarks[18].y else 0)

    return fingers


def recognize_letter(fingers) -> str:
    if fingers == [0, 0, 0, 0, 0]:
        return "A"
    if fingers == [0, 1, 1, 1, 1]:
        return "B"
    if fingers == [1, 1, 0, 0, 0]:
        return "L"
    if fingers == [0, 1, 1, 0, 0]:
        return "U"
    if fingers == [0, 1, 0, 0, 0]:
        return "D"
    return "None"
