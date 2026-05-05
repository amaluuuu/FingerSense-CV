import cv2
import time
import argparse
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np

def create_overlay(img, text, position, font_scale=1.0, color=(255, 255, 255), bg_color=(0, 0, 0), alpha=0.6):
    font = cv2.FONT_HERSHEY_SIMPLEX
    thickness = max(1, int(font_scale * 2))
    
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    x, y = position
    
    rect_x1 = x - 10
    rect_y1 = y - text_h - 10
    rect_x2 = x + text_w + 10
    rect_y2 = y + baseline + 10

    overlay = img.copy()
    cv2.rectangle(overlay, (rect_x1, rect_y1), (rect_x2, rect_y2), bg_color, -1)
    
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    
    cv2.putText(img, text, (x, y), font, font_scale, color, thickness)

def get_fingers_up(hand):
    fingers = []
    lmList = hand["lmList"]
    tipIds = [4, 8, 12, 16, 20]
    
    # Thumb: dynamic left/right based on index and pinky position
    if lmList[5][0] > lmList[17][0]:
        fingers.append(1 if lmList[4][0] > lmList[3][0] else 0)
    else:
        fingers.append(1 if lmList[4][0] < lmList[3][0] else 0)
            
    # 4 Fingers
    for id in range(1, 5):
        fingers.append(1 if lmList[tipIds[id]][1] < lmList[tipIds[id] - 2][1] else 0)
            
    return fingers

def detect_gesture(fingers):
    if fingers == [0, 0, 0, 0, 0]:
        return "Fist"
    elif fingers == [1, 1, 1, 1, 1]:
        return "Open Hand"
    elif fingers == [0, 1, 1, 0, 0]:
        return "Peace"
    elif fingers == [1, 0, 0, 0, 0]:
        return "Thumbs Up"
    elif fingers == [0, 1, 0, 0, 0]:
        return "Pointing"
    elif fingers == [0, 1, 0, 0, 1]:
        return "Rock"
    else:
        return f"Fingers: {fingers.count(1)}"

def main():
    parser = argparse.ArgumentParser(description="Finger Counting & Gesture Recognition")
    parser.add_argument("--camera", type=int, default=0)
    parser.add_argument("--confidence", type=float, default=0.8)
    parser.add_argument("--max_hands", type=int, default=2)
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        return

    detector = HandDetector(detectionCon=args.confidence, maxHands=args.max_hands)
    
    draw_landmarks = True
    pTime = 0
    script_dir = os.path.dirname(os.path.abspath(__file__))
    screenshot_dir = os.path.join(script_dir, "screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    cv2.namedWindow("Hand Tracking Pro", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Hand Tracking Pro", int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)

        hands, img = detector.findHands(img, draw=draw_landmarks)
        
        total_fingers = 0  

        if hands:
            for hand in hands:
                fingers = get_fingers_up(hand)
                finger_count = fingers.count(1)
                total_fingers += finger_count  

                hand_type = hand["type"]
                x, y, w, h = hand["bbox"]
                
                gesture_text = detect_gesture(fingers)

                create_overlay(
                    img, 
                    f"{hand_type}: {gesture_text}", 
                    (x, y - 20), 
                    font_scale=0.7, 
                    color=(0, 255, 0), 
                    bg_color=(50, 50, 50),
                    alpha=0.7
                )

        cTime = time.time()
        fps = 1 / (cTime - pTime) if pTime else 0
        pTime = cTime

        h_img, w_img, _ = img.shape
        
        create_overlay(img, f"FPS: {int(fps)}", (20, 50), font_scale=0.8, color=(255, 200, 0))

        total_text = f"Total Fingers: {total_fingers}"
        create_overlay(img, total_text, (w_img - 300, 50), font_scale=1.0, color=(0, 255, 255), bg_color=(0, 0, 150))
        
        create_overlay(img, "'q' Quit | 'd' Toggle Skeleton | 's' Screenshot", (20, h_img - 30), font_scale=0.6, color=(200, 200, 200))

        cv2.imshow("Hand Tracking Pro", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('d'):
            draw_landmarks = not draw_landmarks
        elif key == ord('s'):
            filename = os.path.join(screenshot_dir, f"snap_{int(time.time())}.jpg")
            cv2.imwrite(filename, img)

        if cv2.getWindowProperty("Hand Tracking Pro", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
