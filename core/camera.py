import cv2

class Camera:

    def __init__(self, camera_index=0):
        self._video_capture = None
        self._camera_index = camera_index
        self._failed_frames = 0

    def setup(self):
        self._video_capture = cv2.VideoCapture(self._camera_index)

        if not self._video_capture.isOpened():
            raise RuntimeError("Camera is already being used")

        self._video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self._video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

    def _is_camera_down(self):
        if self._failed_frames >= 15:
            raise ConnectionError("Camera is not working")
        
    def get_frame(self):
        ret, frame = self._video_capture.read()
        if ret:
            self._failed_frames=0
            return frame
        
        self._failed_frames+=1
        self._is_camera_down()
        return None
    
    def take_picture(self, filename = "user.jpg") -> bool:
        ret, frame = self._video_capture.read()
        if ret:
            self._failed_frames=0
            cv2.imwrite(filename, frame)
            return True
            
        self._failed_frames+=1
        self._is_camera_down()
        return False

    
    def release(self):
        if self._video_capture is not None:
            self._video_capture.release()



