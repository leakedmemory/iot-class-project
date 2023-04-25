import os
import uuid

import cv2
from dotenv import load_dotenv


def main():
    load_dotenv()

    capture_positives_and_anchor()


def capture_positives_and_anchor():
    print("Press 'A' to collect anchors")
    print("Press 'P' to collect positives")
    print("Press 'Q' to quit\n")

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()

        # Cut frame to 250x250 px
        frame = frame[150:150+250, 200:200+250, :]

        # Collect anchors
        if cv2.waitKey(1) & 0xFF == ord("a"):
            image_name = os.path.join(
                    os.getenv(ANC_PATH), f"{uuid.uuid1()}.jpg")
            cv2.imwrite(image_name, frame)

        # Collect positives
        if cv2.waitKey(1) & 0xFF == ord("p"):
            image_name = os.path.join(
                    os.getenv(POS_PATH), f"{uuid.uuid1()}.jpg")
            cv2.imwrite(image_name, frame)

        # Show taken image on screen
        cv2.imshow("Image Collection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
