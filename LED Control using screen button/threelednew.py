

import cv2
import mediapipe as mp
import serial
import time

# Arduino serial connection (change COM port if needed)
arduino = serial.Serial('COM8', 9600)
time.sleep(2)

# Mediapipe hands setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Open webcam
cap = cv2.VideoCapture(0)

# Define textboxes (x1, y1, x2, y2)
boxes = {
    "1st LED": (50, 100, 250, 200),
    "2nd LED": (50, 250, 250, 350),
    "3rd LED": (50, 400, 250, 500)
}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert to RGB for MediaPipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    fingertip_x, fingertip_y = None, None

    # Detect hand landmarks
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Index fingertip landmark (id=8)
            fingertip = hand_landmarks.landmark[8]
            fingertip_x, fingertip_y = int(fingertip.x * w), int(fingertip.y * h)

            # Draw fingertip point
            cv2.circle(frame, (fingertip_x, fingertip_y), 10, (0, 0, 255), -1)

    # Draw textboxes
    active_led = "0"
    for i, (label, (x1, y1, x2, y2)) in enumerate(boxes.items(), start=1):
        color = (200, 200, 200)  # default box color

        if fingertip_x and fingertip_y:
            if x1 < fingertip_x < x2 and y1 < fingertip_y < y2:
                color = (0, 255, 0)  # highlight if finger inside
                active_led = str(i)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
        cv2.putText(frame, label, (x1 + 20, y1 + 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Send command to Arduino
    arduino.write(active_led.encode())

    # Show active LED text
    cv2.putText(frame, f"Active LED: {active_led}", (350, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("LED Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
