# GestureVerse
Webcam hand tracking and gesture-controlled mini applications using Python, OpenCV and MediaPipe Tasks.

## Features
- 21-point hand landmark tracking
- Air Canvas
- Gesture Keyboard
- Gesture Racing
- Hand Gesture Reader for common static poses: open palm, fist, peace sign, pointing, thumbs up and three fingers

## Windows setup
```powershell
python -m pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File .\\scripts\\download_model.ps1
python main.py
```

## Keys
1 Canvas | 2 Keyboard | 3 Racing | 4 Gesture Reader | 0 Dashboard | Q Quit

Note: Gesture Reader uses simple landmark heuristics for common poses. It is not a full sign-language or unrestricted air-writing translator. Test gesture recognition in your own lighting and camera setup.
