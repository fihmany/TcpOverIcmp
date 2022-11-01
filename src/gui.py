import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")

# create a label
label = customtkinter.CTkLabel(app, text="Hello World!", text_font=("Arial", 35))
text_var = customtkinter.StringVar(value="START")

def button_function():
    if text_var.get() == "START":
        text_var.set("STOP")
    else:
        text_var.set("START")

# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=app, textvariable=text_var, command=button_function)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
label.place(relx=0.5, rely=0.25, anchor=customtkinter.CENTER)


app.mainloop()