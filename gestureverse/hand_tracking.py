import time
from pathlib import Path
import cv2
import mediapipe as mp

CONNECTIONS=((0,1),(1,2),(2,3),(3,4),(0,5),(5,6),(6,7),(7,8),(5,9),(9,10),(10,11),(11,12),(9,13),(13,14),(14,15),(15,16),(13,17),(17,18),(18,19),(19,20),(0,17))

class HandTracker:
    def __init__(self, model_path, num_hands=2):
        path=Path(model_path)
        if not path.is_file(): raise FileNotFoundError(f"Missing model: {path}")
        vision=mp.tasks.vision
        opts=vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=str(path)),
            running_mode=vision.RunningMode.VIDEO,num_hands=num_hands)
        self.detector=vision.HandLandmarker.create_from_options(opts)
        self.last=-1
    def detect(self,frame):
        rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        img=mp.Image(image_format=mp.ImageFormat.SRGB,data=rgb)
        ts=max(int(time.perf_counter()*1000),self.last+1); self.last=ts
        return self.detector.detect_for_video(img,ts).hand_landmarks or []
    def close(self): self.detector.close()

def draw_hand_landmarks(frame,hands):
    h,w=frame.shape[:2]
    for hand in hands:
        pts=[(int(p.x*w),int(p.y*h)) for p in hand]
        for a,b in CONNECTIONS: cv2.line(frame,pts[a],pts[b],(90,220,120),2,cv2.LINE_AA)
        for p in pts: cv2.circle(frame,p,4,(40,180,255),-1,cv2.LINE_AA)
