import cv2
from pathlib import Path
import time
class Camera:

    def __init__(self, camera_index=0):
        self._video_capture = None
        self._camera_index = camera_index
        self._failed_frames = 0
        self.script_dir = Path(__file__).parent.resolve()
        self.faces_dir = self.script_dir.parent / "faces"
        self.faces_dir.mkdir(parents=True, exist_ok=True)

    def setup(self):
        self._video_capture = cv2.VideoCapture(self._camera_index)

        if not self._video_capture.isOpened():
            self.release()
            raise RuntimeError("Camera is already being used")
        
        
        self._video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self._video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

        success = False
        for _ in range(5):
            ret, frame = self._video_capture.read()
            if ret and frame is not None:
                success = True
                break
            time.sleep(0.1)  

        if not success:
            self.release()
            raise RuntimeError("Camera doesn't send frames")


    def _is_camera_down(self):
        if self._failed_frames >= 15:
            self.release()
            raise ConnectionError("Camera is not working")
        
    def get_frame(self):
        if self._video_capture is None:
            return None
        
        ret, frame = self._video_capture.read()
        if ret:
            self._failed_frames=0
            return frame
        
        self._failed_frames+=1
        self._is_camera_down()
        return None
    
    def take_picture(self, frame,  filename = "user.jpg") -> bool:
        if frame is not None:
            full_path = self.faces_dir / filename
            return cv2.imwrite(str(full_path), frame), str(full_path)
        return False, None

    
    def release(self):
        if self._video_capture is not None:
            self._video_capture.release()
            self._video_capture = None



if __name__ == "__main__":
    cam = Camera(0)
    try:
        cam.setup()
        if cam.take_picture("test_unit.jpg"):
            print("Picture saved succesfully")
    except Exception as e:
        print(f"Critical Error: {e}")
    finally:
        cam.release()
