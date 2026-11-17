import cv2
from pathlib import Path
from gestureverse.hand_tracking import HandTracker, draw_hand_landmarks
from gestureverse.modes import AirCanvas, GestureKeyboard, GestureRacing, HandGestureReader

ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "models" / "hand_landmarker.task"

def main():
    if not MODEL.exists():
        print("Model missing. Run the model download script first.")
        return
    tracker = HandTracker(MODEL)
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Webcam not available.")
        tracker.close()
        return
    modes = {
        "1": ("AIR CANVAS", AirCanvas()),
        "2": ("GESTURE KEYBOARD", GestureKeyboard()),
        "3": ("GESTURE RACING", GestureRacing()),
        "4": ("HAND GESTURE READER", HandGestureReader()),
    }
    active = None
    print("1 Canvas | 2 Keyboard | 3 Racing | 4 Gesture Reader | 0 Dashboard | Q Quit")
    try:
        while True:
            ok, frame = cam.read()
            if not ok: break
            frame = cv2.flip(frame, 1)
            hands = tracker.detect(frame)
            draw_hand_landmarks(frame, hands)
            if active is None:
                cv2.rectangle(frame,(20,20),(frame.shape[1]-20,frame.shape[0]-20),(25,30,45),-1)
                cv2.putText(frame,"GESTUREVERSE",(50,90),cv2.FONT_HERSHEY_DUPLEX,1.2,(90,230,170),2)
                labels=["1  AIR CANVAS","2  GESTURE KEYBOARD","3  GESTURE RACING","4  HAND GESTURE READER"]
                for i,label in enumerate(labels):
                    cv2.putText(frame,label,(60,160+i*55),cv2.FONT_HERSHEY_SIMPLEX,.75,(245,245,245),2)
                cv2.putText(frame,"Press 1-4 to open a mode | Q to quit",(60,420),cv2.FONT_HERSHEY_SIMPLEX,.55,(190,200,215),1)
            else:
                title, mode = modes[active]
                mode.update(frame,hands)
                mode.draw(frame)
                cv2.putText(frame,title+" | 0: Dashboard | Q: Quit",(15,28),cv2.FONT_HERSHEY_SIMPLEX,.55,(90,230,170),2)
            cv2.imshow("GestureVerse",frame)
            key=cv2.waitKey(1)&0xFF
            if key in (ord("q"),ord("Q"),27): break
            if chr(key) in modes: active=chr(key)
            elif key==ord("0"): active=None
    finally:
        cam.release()
        tracker.close()
        cv2.destroyAllWindows()

if __name__=="__main__": main()
