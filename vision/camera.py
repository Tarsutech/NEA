import cv2


def open_camera(index: int = 0) -> cv2.VideoCapture:
    """Open the webcam and return the capture handle."""
    backend = cv2.CAP_DSHOW if hasattr(cv2, "CAP_DSHOW") else None
    if backend is not None:
        cap = cv2.VideoCapture(index, backend)
    else:
        cap = cv2.VideoCapture(index)

    if not cap.isOpened():
        raise RuntimeError("Camera not opening")
    return cap
