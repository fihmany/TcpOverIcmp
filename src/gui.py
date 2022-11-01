import customtkinter
import pathlib

# Declare string variables
title = "TCP over ICMP"
subtitle = "Yair Fihman and Raz Gino"
page_size = "600x400"

server_ip_text = "Server IP:"
target_ip_text = "Target IP:"
target_port_text = "Target Port:"

# Create the window
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()
app.geometry(page_size)
app.title(title)
app.iconbitmap(f"{pathlib.Path(__file__).parent.parent.resolve()}\\icon.ico")


# Declare text variables
button_text = customtkinter.StringVar(value="START")
server_ip_textfield_text = customtkinter.StringVar(value="127.0.0.1")
target_ip_textfield_text = customtkinter.StringVar(value="www.example.com")
target_port_textfield_text = customtkinter.StringVar(value="80")

# Declare widget actions
def button_function():
    if button_text.get() == "START":
        button_text.set("STOP")
    else:
        button_text.set("START")

# Declare widgets
title_label = customtkinter.CTkLabel(app, text=title, text_font=("Arial", 35))
subtitle_label = customtkinter.CTkLabel(app, text=subtitle, text_font=("Arial", 25))

server_ip_label = customtkinter.CTkLabel(app, text=server_ip_text, text_font=("Arial", 12))
server_ip_textfield = customtkinter.CTkEntry(app, textvariable=server_ip_textfield_text, text_font=("Arial", 12))

target_ip_label = customtkinter.CTkLabel(app, text=target_ip_text, text_font=("Arial", 12))
target_ip_textfield = customtkinter.CTkEntry(app, textvariable=target_ip_textfield_text, text_font=("Arial", 12))

target_port_label = customtkinter.CTkLabel(app, text=target_port_text, text_font=("Arial", 12))
target_port_textfield = customtkinter.CTkEntry(app, textvariable=target_port_textfield_text, text_font=("Arial", 12))

button = customtkinter.CTkButton(master=app, textvariable=button_text, command=button_function)


# Place widgets
title_label.place(relx=0.5, rely=0.15, anchor=customtkinter.CENTER)
subtitle_label.place(relx=0.5, rely=0.30, anchor=customtkinter.CENTER)

base_settings_y = 0.45
diff_settings_items_y = 0.1
settings_widgets = [(server_ip_label, server_ip_textfield), (target_ip_label, target_ip_textfield), (target_port_label, target_port_textfield)]

for i, (label, textfield) in enumerate(settings_widgets):
    label.place(relx=0.1, rely=base_settings_y + diff_settings_items_y * i, anchor=customtkinter.CENTER)
    textfield.place(relx=0.85, rely=base_settings_y + diff_settings_items_y * i, anchor=customtkinter.CENTER)

button.place(relx=0.5, rely=base_settings_y + diff_settings_items_y * len(settings_widgets), anchor=customtkinter.CENTER)

# Run the window
app.mainloop()