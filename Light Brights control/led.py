import cv2
import mediapipe as mp
import numpy as np
import serial
import time

# Setup Serial (Change COM5 to your Arduino port, baud must match Arduino)
arduino = serial.Serial('COM8', 9600)
time.sleep(2)  # wait for Arduino to reset

# Mediapipe Hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Thumb tip = 4, Index tip = 8
            x1, y1 = int(hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h)
            x2, y2 = int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h)

            cv2.circle(frame, (x1, y1), 5, (0, 255, 0), -1)
            cv2.circle(frame, (x2, y2), 5, (0, 255, 0), -1)
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            # Distance between thumb and index finger
            dist = np.hypot(x2 - x1, y2 - y1)
            print(f"Distance: {dist}") 
            # Brightness mapping
            brightness = np.interp(dist, [30, 200], [0, 255])
            brightness = int(np.clip(brightness, 0, 255))

            # If no fingers up (distance small), LED OFF
            if dist < 30:
                brightness = 0
                cv2.putText(frame, "LED OFF", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(frame, f"Brightness: {brightness}", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Send to Arduino
            arduino.write(f"{brightness}\n".encode())
            print(f"Sent: {brightness}")  # Python-side Serial Monitor

    cv2.imshow("Hand Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
