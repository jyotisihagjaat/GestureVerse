import cv2, numpy as np, random

def xy(hand,i,w,h): return int(hand[i].x*w),int(hand[i].y*h)
def fingers(hand):
    return [hand[t].y < hand[p].y for t,p in zip((8,12,16,20),(6,10,14,18))]
def pinch(hand):
    return ((hand[4].x-hand[8].x)**2+(hand[4].y-hand[8].y)**2)**0.5 < .055

class AirCanvas:
    def __init__(self): self.layer=None; self.last=None
    def update(self,frame,hands):
        if self.layer is None: self.layer=np.zeros_like(frame)
        if hands:
            x,y=xy(hands[0],8,frame.shape[1],frame.shape[0])
            if pinch(hands[0]): self.last=None
            elif fingers(hands[0])[0]:
                if self.last: cv2.line(self.layer,self.last,(x,y),(70,230,130),6,cv2.LINE_AA)
                self.last=(x,y)
            else: self.last=None
        else: self.last=None
    def draw(self,frame):
        mask=cv2.cvtColor(self.layer,cv2.COLOR_BGR2GRAY)>0
        frame[mask]=self.layer[mask]
        cv2.putText(frame,"Index finger: draw | Pinch: stop | C: clear",(15,60),0,.55,(255,255,255),2)
        if cv2.waitKey(1)&0xFF==ord("c"): self.layer[:]=0

class GestureKeyboard:
    def __init__(self): self.text=""
        # keyboard selection is by pointing and pinching
    def update(self,frame,hands):
        if not hands or not pinch(hands[0]): return
        h,w=frame.shape[:2]; x,y=xy(hands[0],8,w,h)
        keys="QWERTYUIOPASDFGHJKLZXCVBNM"
        if y>130:
            c=min(9,x//(w//10)); r=min(2,(y-130)//max(1,(h-130)//3)); i=r*10+c
            if i<len(keys): self.text+=keys[i]
    def draw(self,frame):
        h,w=frame.shape[:2]
        cv2.rectangle(frame,(0,0),(w,110),(25,30,45),-1)
        cv2.putText(frame,self.text[-50:],(15,55),0,.7,(100,240,170),2)
        keys="QWERTYUIOPASDFGHJKLZXCVBNM"; cw=w//10; ch=max(1,(h-130)//3)
        for i,k in enumerate(keys):
            r,c=divmod(i,10); x,y=c*cw,130+r*ch
            cv2.rectangle(frame,(x+2,y+2),(x+cw-2,y+ch-2),(80,90,110),2)
            cv2.putText(frame,k,(x+8,y+ch//2),0,.5,(255,255,255),1)

class GestureRacing:
    def __init__(self): self.x=.5; self.score=0; self.paused=True; self.obs=[]; self.tick=0
    def update(self,frame,hands):
        h,w=frame.shape[:2]; self.tick+=1
        if hands:
            hand=hands[0]; self.x=max(.08,min(.92,hand[9].x))
            n=sum(fingers(hand))
            if n>=4: self.paused=False
            elif n==0: self.paused=True
        if not self.paused:
            if self.tick%35==0: self.obs.append([random.randint(int(w*.1),int(w*.9),),-25])
            for o in self.obs:o[1]+=7
            self.obs=[o for o in self.obs if o[1]<h+30]; self.score+=1
    def draw(self,frame):
        h,w=frame.shape[:2]; cx=int(self.x*w)
        cv2.rectangle(frame,(cx-20,h-85),(cx+20,h-35),(80,210,255),-1)
        for x,y in self.obs:cv2.rectangle(frame,(x-17,y-20),(x+17,y+20),(60,70,240),-1)
        cv2.putText(frame,f"Score {self.score} | Open palm: resume | Fist: pause",(15,60),0,.55,(255,255,255),2)

class HandGestureReader:
    """Heuristic static-pose reader; this is not full sign-language translation."""
    def __init__(self): self.label="SHOW YOUR HAND"; self.info="Try open palm, fist, peace, pointing or thumbs up"; self.prev=""; self.stable=0
    def classify(self,hand):
        up=fingers(hand); count=sum(up); thumb=hand[4].y < hand[3].y-.025
        if count==4:return "OPEN PALM","Four fingers extended"
        if count==0 and not thumb:return "FIST","Closed hand"
        if up[0] and up[1] and not up[2] and not up[3]:return "PEACE SIGN","Index and middle fingers raised"
        if up[0] and not up[1] and not up[2] and not up[3]:return "POINTING","Index finger raised"
        if thumb and count<=1:return "THUMBS UP","Thumb raised"
        if count==3:return "THREE FINGERS","Three fingers raised"
        return "GESTURE DETECTED",f"{count} fingers extended"
    def update(self,frame,hands):
        if not hands:self.label="NO HAND DETECTED";self.info="Show one hand to the camera";return
        label,info=self.classify(hands[0])
        if label==self.prev:self.stable+=1
        else:self.prev=label;self.stable=0
        if self.stable>=2:self.label,self.info=label,info
    def draw(self,frame):
        h,w=frame.shape[:2]
        cv2.rectangle(frame,(10,h-125),(w-10,h-10),(25,30,45),-1)
        cv2.putText(frame,"HAND GESTURE READER",(25,h-88),0,.6,(100,240,170),2)
        cv2.putText(frame,self.label,(25,h-52),cv2.FONT_HERSHEY_DUPLEX,.85,(255,255,255),2)
        cv2.putText(frame,self.info,(25,h-24),0,.48,(210,220,230),1)
