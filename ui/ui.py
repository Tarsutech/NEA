import cv2


def draw_hand_landmarks(frame, hand_landmarks, mp_hands, mp_draw) -> None:
    mp_draw.draw_landmarks(
        frame,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
    )


def draw_debug(frame, fingers) -> None:
    cv2.putText(
        frame,
        f"Fingers: {fingers}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2,
    )


def draw_status(frame, output_text: str, spoken_text: str) -> None:
    cv2.putText(
        frame,
        f"Signed Text: {output_text}",
        (10, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        f"Spoken Text: {spoken_text}",
        (10, 130),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2,
    )


def draw_controls(frame) -> None:
    cv2.putText(
        frame,
        "C: Speak | V: Voice input | R: Reset | Q: Quit",
        (10, 170),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (200, 200, 0),
        2,
    )
