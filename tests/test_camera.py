import pytest
import numpy as np
from core.camera import Camera

class TestCamera:
    @pytest.fixture
    def camera_obj(self):
        cam = Camera(0)
        yield cam
        cam.release()

    def test_camera_init(self):
        camera = Camera(5)

        assert camera._camera_index == 5
        assert camera._video_capture is None

    def test_camera_setup(self,camera_obj):
        camera_obj.setup()

        assert camera_obj._video_capture is not None
        assert camera_obj._video_capture.isOpened() is True

    def test_camera_get_frames(self, camera_obj):
        camera_obj.setup()
        frame = camera_obj.get_frame()

        assert frame is not None
        assert isinstance(frame, np.ndarray)
        assert len(frame.shape) == 3
        


        