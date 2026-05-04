import customtkinter
import tkinter
from camera import Camera
from facerecognizer import FaceRecognizer
import cv2
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("ProfBlocker")

        self.geometry("800x500")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self._facerecognizer = FaceRecognizer()
        self._camera = Camera(0)
        self._camera_view_panel = CameraViewPanel(master=self, facerecognizer= self._facerecognizer, camera=self._camera)
        self._camera_view_panel.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
        actions = ["Action 1", "Action 2", "Action 3"]
        self._config_panel = ConfigPanel(master=self, values=actions, facerecognizer=self._facerecognizer, camera = self._camera)
        self._config_panel.grid(row=0, column=1, sticky="nswe", padx=(0,10), pady=10)

    def custom_destroy(self):
        if self._camera_view_panel._camera:
            self._camera_view_panel._camera.release()
        self.destroy()


class ConfigPanel(customtkinter.CTkFrame):
    def __init__(self, master,values, facerecognizer, camera):
        super().__init__(master)
        self.checkboxes=[]
        self.values=values
        self._facerecognizer = facerecognizer
        self._camera = camera
        self._label = customtkinter.CTkLabel(self, text="Settings",font=("Arial", 16, "bold") )
        self._label.pack(pady=20, padx=20)

        self.add_user_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.add_user_frame.pack(pady=10, padx=10, fill="x")

        self._add_user_entry = customtkinter.CTkEntry(self.add_user_frame, placeholder_text="Unique user name")
        self._add_user_entry.pack(pady=5, padx=10, fill="x")

        self._add_users_button = customtkinter.CTkButton(self.add_user_frame, text="Add User", fg_color="#2FA572", hover_color="#106A43", command=self.add_user)
        self._add_users_button.pack(pady=5, padx=10, fill="x")

        self._manage_users_button = customtkinter.CTkButton(self, text="Manage users")
        self._manage_users_button.pack(pady=10, padx=20)

        self.actions_frame = customtkinter.CTkFrame(self) 
        self.actions_frame.pack(pady=10, padx=15, fill="x")

        customtkinter.CTkLabel(self.actions_frame, text="Active Protections", font=("Arial", 12, "bold")).pack(pady=5)

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self.actions_frame, text=value)
            checkbox.pack(padx=20, pady=10)
            self.checkboxes.append(checkbox)

        self._close_app_button = customtkinter.CTkButton(
            self, 
            text="Close App", 
            command=self.master.custom_destroy, 
            fg_color="#922B21", 
            hover_color="#7B241C"
        )
        self._close_app_button.pack(pady=(20, 15), padx=20, side="bottom", fill="x")

        
    def get_checkboxed_values(self):
        checked_checkboxes=[]
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

    def add_user(self):
        entry = self._add_user_entry.get().strip()
        if  entry == "":
            self.add_user_show_message("empty_name")
            return
        frame = self._camera.get_frame()
        if frame is None:
            self.add_user_show_message("camera_error")
            return
        outcome, result = self._facerecognizer.is_there_a_single_face(frame)
        if outcome is False:
            self.add_user_show_message(result)
            return
        
        cropped_face = self._facerecognizer.crop_face(frame, result)

        success, path = self._camera.take_picture(cropped_face, f"{entry}.jpg")
        if success:
            outcome, message = self._facerecognizer.add_recognized_person(entry, frame, path)
            if outcome is True:
                self.add_user_show_message("success")
                self._add_user_entry.delete(0, 'end') 
            else:
                self.add_user_show_message(message)
        else:
            self.add_user_show_message("picture_error")

    def add_user_show_message(self, message):
        messages = {
            "empty_name": ("Warning", "You need to input user's name!"),
            "no_face": ("Warning", "No face was detected in front of the camera"),
            "multiple_faces": ("Warning", "There is more than one face in the frame"),
            "name_occupied": ("Error", "That name is already taken, pick a different name"),
            "empty_frame": ("Error", "Frame is empty"),
            "camera_error": ("Error", "Error connecting with the camera"),
            "picture_error": ("Error", "Unable to save the picture"),
            "success": ("Info", "User has ben succesfully added to the base")
        }
        msg_type, text = messages.get(message, ("Error", f"An unexpected error occured: {message}"))


        if msg_type == "Warning":
            messagebox.showwarning("Warning", text)
        elif msg_type == "Error":
            messagebox.showerror("Error", text)
        elif msg_type == "Info":
            messagebox.showinfo("Info", text)

    


    
class CameraViewPanel(customtkinter.CTkFrame):
    def __init__(self, master, facerecognizer, camera):
        super().__init__(master)

        self.grid_propagate(False)
        self.pack_propagate(False)

        self.current_width =640
        self.current_height = 480
        


        self._monitor = tkinter.Label(self, bg="black")
        self._monitor.pack(fill="both", expand=True)
        self.bind("<Configure>", self.on_resize)
        self._camera = camera
        self._camera.setup()
        self._facerecognizer = facerecognizer

        self.frame_counter = 0
        self.process_every_n_frames = 3

        self.last_recognized_faces = []

        self.update_frame()


    def on_resize(self, event):
        if event.width > 10 and event.height > 10:
            self.current_width = event.width
            self.current_height = event.height

    def update_frame(self):
        frame = self._camera.get_frame()
        if frame is not None:
            if self.frame_counter % self.process_every_n_frames == 0:
                success, recognized_people, message = self._facerecognizer.is_known_face(frame)
                if success:
                    self.last_recognized_faces = recognized_people
                else:
                    self.last_recognized_faces = []
            
            self.frame_counter += 1

            if self.last_recognized_faces:
                frame = self._facerecognizer.color_faces(frame, self.last_recognized_faces)



            h_cam, w_cam, _ = frame.shape
            ratio = min(self.current_width / w_cam, self.current_height / h_cam)
            
            new_width = int(w_cam * ratio)
            new_height = int(h_cam * ratio)
            
            if new_width < 1: new_width = 1
            if new_height < 1: new_height = 1

            frame = cv2.resize(frame, (new_width, new_height))

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)

            img = ImageTk.PhotoImage(image=pil_image)
            self._monitor.configure(image=img)
            self._monitor.image = img
        self.after(10, self.update_frame)


class UsersPanel(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)




if __name__ == "__main__":
    app = GUI()
    app.mainloop()