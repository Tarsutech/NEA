import os

import cv2

from audio.speech import init_stt, listen_once_result
from core.fingerspell import (
    FingerspellConfig,
    clean_text_to_letters,
    load_letter_images,
    make_blank_image,
)
from ui.fingerspell import clear_window, init_window, show_letters


def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_folder = os.path.join(script_dir, "bsl_letters")

    config = FingerspellConfig(image_folder=image_folder)
    letter_images, missing = load_letter_images(config)

    if not letter_images:
        print(f"No letter images found in '{config.image_folder}'.")
        return

    if missing:
        print(f"Missing images for: {', '.join(missing)}")

    init_window(config)
    recogniser = init_stt(noise_duration=1.0)
    blank_image = make_blank_image(config)

    print("Press ENTER to speak | Q then ENTER to quit")

    try:
        while True:
            user_input = input().strip().lower()
            if user_input == "q":
                break

            spoken_text, error = listen_once_result(
                recogniser,
                on_listen=lambda: print("Listening..."),
            )

            if error:
                print(error)
                continue

            if not spoken_text:
                print("Speech not recognised")
                continue

            print(f"You said: {spoken_text}")

            letters = clean_text_to_letters(spoken_text)
            if not letters:
                clear_window(config, blank_image)
                continue

            show_letters(config, letter_images, letters)
            clear_window(config, blank_image)
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
