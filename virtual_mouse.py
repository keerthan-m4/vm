import sys
print(sys.executable)
import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh

hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7, model_complexity=1)
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.7)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

screen_w, screen_h = pyautogui.size()

smooth_factor = 7
prev_x, prev_y = 0, 0

zone_half_w = 100
zone_half_h = 100

calib_x = None
calib_y = None
hand_present_prev = False

EYE_LANDMARKS = [33, 160, 158, 133, 153, 144]
BLINK_THRESHOLD = 0.25
blink_count = 0
last_blink_time = 0
double_blink_interval = 1.0

def eye_aspect_ratio(landmarks, eye_indices, image_w, image_h):
    coords = [(int(landmarks[idx].x * image_w), int(landmarks[idx].y * image_h)) for idx in eye_indices]
    A = np.linalg.norm(np.array(coords[1]) - np.array(coords[5]))
    B = np.linalg.norm(np.array(coords[2]) - np.array(coords[4]))
    C = np.linalg.norm(np.array(coords[0]) - np.array(coords[3]))
    ear = (A + B) / (2.0 * C)
    return ear

def is_middle_finger_extended(hand_landmarks):
    middle_tip_y = hand_landmarks.landmark[12].y
    middle_pip_y = hand_landmarks.landmark[10].y
    if middle_tip_y < middle_pip_y:
        folded = True
        for tip_id, pip_id in zip([8, 16, 20], [6, 14, 18]):
            if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[pip_id].y:
                folded = False
                break
        if folded:
            return True
    return False

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    hand_results = hands.process(rgb_frame)
    face_results = face_mesh.process(rgb_frame)

    hand_present = bool(hand_results.multi_hand_landmarks)

    if not hand_present:
        calib_x = None
        calib_y = None

    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if is_middle_finger_extended(hand_landmarks):
                print("Middle finger detected: closing app.")
                cap.release()
                cv2.destroyAllWindows()
                exit(0)

            index_fingertip = hand_landmarks.landmark[8]
            x = int(index_fingertip.x * frame.shape[1])
            y = int(index_fingertip.y * frame.shape[0])

            if calib_x is None:
                calib_x, calib_y = x, y

            zone_left = calib_x - zone_half_w
            zone_right = calib_x + zone_half_w
            zone_top = calib_y - zone_half_h
            zone_bottom = calib_y + zone_half_h

            screen_x = np.interp(x, [zone_left, zone_right], [0, screen_w])
            screen_y = np.interp(y, [zone_top, zone_bottom], [0, screen_h])

            screen_x = np.clip(screen_x, 0, screen_w - 1)
            screen_y = np.clip(screen_y, 0, screen_h - 1)

            smooth_x = prev_x + (screen_x - prev_x) / smooth_factor
            smooth_y = prev_y + (screen_y - prev_y) / smooth_factor
            pyautogui.moveTo(smooth_x, smooth_y, duration=0)

            prev_x, prev_y = smooth_x, smooth_y

            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
            cv2.rectangle(frame, (zone_left, zone_top), (zone_right, zone_bottom), (0, 200, 255), 2)

    blinked = False
    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            image_h, image_w = frame.shape[:2]
            ear = eye_aspect_ratio(face_landmarks.landmark, EYE_LANDMARKS, image_w, image_h)
            for idx in EYE_LANDMARKS:
                x_eye = int(face_landmarks.landmark[idx].x * image_w)
                y_eye = int(face_landmarks.landmark[idx].y * image_h)
                cv2.circle(frame, (x_eye, y_eye), 2, (255, 0, 0), -1)
            if ear < BLINK_THRESHOLD:
                blinked = True

    current_time = time.time()
    if blinked:
        if (current_time - last_blink_time) > 0.3:
            blink_count += 1
            last_blink_time = current_time

    if blink_count >= 2 and (current_time - last_blink_time) < double_blink_interval:
        pyautogui.click()
        print("Double blink detected - mouse click triggered")
        blink_count = 0

    if blink_count == 1 and (current_time - last_blink_time) > double_blink_interval:
        blink_count = 0

    cv2.imshow("Virtual Mouse with Blink Click and Middle Finger Exit", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
