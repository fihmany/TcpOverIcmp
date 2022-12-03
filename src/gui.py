import customtkinter
import pathlib
import threading
import client
from queue import Queue
from common.data_types import QUIT_COMMAND

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
# TODO: fix the icon
# app.iconbitmap(r"{pathlib.Path(__file__).parent.parent.resolve()}\\icon.ico")

# Declare text variables
button_text = customtkinter.StringVar(value="START")
server_ip_textfield_text = customtkinter.StringVar(value="127.0.0.1")
target_ip_textfield_text = customtkinter.StringVar(value="www.example.com")
target_port_textfield_text = customtkinter.StringVar(value="80")

# define queues to communicate between the client thread and the gui thread
in_queue = Queue()
out_queue = Queue()

# define a function which calls the client main in a seprate thread
def start_client():
    client.main(server_ip_textfield_text.get(),
                target_ip_textfield_text.get(),
                target_port_textfield_text.get(),
                # pass the in queue as the out queue and vice versa
                out_queue,
                in_queue)

client_logic_thread = threading.Thread(target=start_client)

# Declare widget actions
def button_function():
    if button_text.get() == "START":
        client_logic_thread.start()
        button_text.set("STOP")
    else:
        # TODO: stop the client
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

# Add a listener to the x button on the gui
def on_closing():
    app.destroy()
    # join the client thread to the main thread
    print("Sending the quit command")
    out_queue.put(QUIT_COMMAND)

    print("joining thread")
    client_logic_thread.join()


app.protocol("WM_DELETE_WINDOW", on_closing)

# Run the window
app.mainloop()

print("after mainloop")