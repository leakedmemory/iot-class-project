import os
import uuid

import cv2
from dotenv import load_dotenv


def main():
    load_dotenv()
    create_needed_directories()
    capture_anchor_and_positives()


def capture_anchor_and_positives():
    print("NOTE: it is recommended that you take at least 400 shots in different")
    print("positions for both anchor and positives before you start training the model")
    print("[A] Collect anchors")
    print("[P] Collect positives")
    print("[Q] Quit\n")

    # change the value inside the `cv2.VideoCapture` call to select the video
    # capture you want to use
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()

        # cut frame to 250x250 px
        frame = frame[150:150+250, 200:200+250, :]

        # collect anchors
        if cv2.waitKey(1) & 0xFF == ord("a"):
            image_name = os.path.join(
                    os.getenv("ANCHOR_PATH"), f"{uuid.uuid1()}.jpg")
            cv2.imwrite(image_name, frame)

        # collect positives
        if cv2.waitKey(1) & 0xFF == ord("p"):
            image_name = os.path.join(
                    os.getenv("POSITIVE_PATH"), f"{uuid.uuid1()}.jpg")
            cv2.imwrite(image_name, frame)

        # show taken image on screen
        cv2.imshow("Image Collection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def create_needed_directories():
    os.makedirs(os.getenv("ANCHOR_PATH"), exist_ok=True)
    os.makedirs(os.getenv("POSITIVE_PATH"), exist_ok=True)


if __name__ == "__main__":
    main()
