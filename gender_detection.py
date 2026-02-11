import cv2

def main():
    # Load Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # Load pre-trained gender detection model (DNN)
    gender_net = cv2.dnn.readNetFromCaffe(
        "deploy_gender.prototxt",
        "gender_net.caffemodel"
    )

    # Labels for gender
    gender_list = ["Male", "Female"]

    # Start webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Tidak dapat membuka kamera.")
        return

    print("Tekan 'q' untuk keluar dari deteksi wajah.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Gagal membaca frame.")
            break

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        male_count = 0
        female_count = 0

        for (x, y, w, h) in faces:
            # Extract face ROI
            face_img = frame[y:y+h, x:x+w].copy()
            blob = cv2.dnn.blobFromImage(
                face_img, 1.0, (227, 227),
                (78.4263377603, 87.7689143744, 114.895847746), swapRB=False
            )
            gender_net.setInput(blob)
            gender_preds = gender_net.forward()
            gender = gender_list[gender_preds[0].argmax()]

            # Count
            if gender == "Male":
                male_count += 1
            else:
                female_count += 1

            # Draw rectangle + label
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                frame, gender, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2
            )

        # Show total counts
        cv2.putText(frame, f"Total Faces: {len(faces)}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"Males: {male_count}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, f"Females: {female_count}", (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show the video feed with detection
        cv2.imshow("Face & Gender Detection", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
