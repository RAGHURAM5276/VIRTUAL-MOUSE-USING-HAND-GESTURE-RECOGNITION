import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize webcam and mediapipe face mesh
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

def eye_move():
    blink_threshold = 0.2  # Threshold for blink detection
    blink_cooldown = 1     # Time in seconds between blinks for clicks
    last_blink_time = time.time()

    while True:
        # Read frame from webcam
        ret, frame = cam.read()
        if not ret:
            break

        # Flip and process frame
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape

        if landmark_points:
            landmarks = landmark_points[0].landmark

            # Cursor movement based on eye landmarks
            cursor_point = landmarks[474]  # Pupil landmark
            screen_x = int(cursor_point.x * screen_w)
            screen_y = int(cursor_point.y * screen_h)
            pyautogui.moveTo(screen_x, screen_y)

            # Eye blink detection
            left_eye = [landmarks[145], landmarks[159]]  # Top and bottom of left eye
            vertical_distance = abs(left_eye[0].y - left_eye[1].y)
            if vertical_distance < blink_threshold:
                current_time = time.time()
                if current_time - last_blink_time > blink_cooldown:
                    pyautogui.click()
                    last_blink_time = current_time

            # Draw landmarks for debugging
            for point in left_eye:
                x = int(point.x * frame_w)
                y = int(point.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)
            cv2.circle(frame, (int(cursor_point.x * frame_w), int(cursor_point.y * frame_h)), 5, (255, 0, 0), -1)

        # Display the frame
        cv2.imshow('Eye Controlled Mouse', frame)

        # Exit on pressing 'Q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cam.release()
    cv2.destroyAllWindows()

# Run the program
eye_move()
