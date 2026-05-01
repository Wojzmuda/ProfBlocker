import customtkinter


class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("ProfBlocker")
        self.geometry("800x500")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self._camera_view_panel = CameraViewPanel(master=self)
        self._camera_view_panel.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
        actions = ["Action 1", "Action 2", "Action 3"]
        self._config_panel = ConfigPanel(master=self, values=actions)
        self._config_panel.grid(row=0, column=1, sticky="nswe", padx=(0,10), pady=10)

    def custom_destroy(self):
        self.destroy()


class ConfigPanel(customtkinter.CTkFrame):
    def __init__(self, master,values):
        super().__init__(master)
        self.checkboxes=[]
        self.values=values
        self._label = customtkinter.CTkLabel(self, text="Settings",font=("Arial", 16, "bold") )
        self._label.pack(pady=20, padx=20)

        self._add_users_button = customtkinter.CTkButton(self, text="Add a new user")
        self._add_users_button.pack(pady=10, padx=20)

        self._manage_users_button = customtkinter.CTkButton(self, text="Manage users")
        self._manage_users_button.pack(pady=10, padx=20)

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.pack(padx=20, pady=10)
            self.checkboxes.append(checkbox)

        self._close_app_button = customtkinter.CTkButton(self, text="Close app", command=self.master.custom_destroy, fg_color = "red", hover_color="darkred")
        self._close_app_button.pack(pady=20, padx=20, side="bottom")


        
    def get_checkboxed_values(self):
        checked_checkboxes=[]
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

    

class CameraViewPanel(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)


class UsersPanel(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)




if __name__ == "__main__":
    app = GUI()
    app.mainloop()