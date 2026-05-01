import customtkinter


app = customtkinter.CTk()


def button_callack():
    print("button_pressed")

app.title("My app")
app.geometry("800x500")
app.grid_columnconfigure((0,1), weight=1)
button = customtkinter.CTkButton(app, text="my button", command = button_callack)
button.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
checkbox_1 = customtkinter.CTkCheckBox(app, text="checkbox 1")
checkbox_1.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
checkbox_2 = customtkinter.CTkCheckBox(app, text="checkbox 2")
checkbox_2.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="w")
app.mainloop()