import customtkinter
import threading
from client import ProxyClient
from queue import Queue
from common.data_types import QUIT_COMMAND

class ClientGUI:
    def __init__(self):
        # Declare string variables
        self.title = "TCP over ICMP"
        self.subtitle = "Yair Fihman and Raz Gino"
        self.page_size = "600x400"

        self.server_ip_text = "Server IP:"
        self.target_ip_text = "Target IP:"
        self.target_port_text = "Target Port:"
    

        # Create the window
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

        self.app = customtkinter.CTk()
        self.app.geometry(self.page_size)
        self.app.title(self.title)

        # TODO: fix the icon to work on WSL, disabled for now
        # self.app.iconbitmap(r"{pathlib.Path(__file__).parent.parent.resolve()}\\icon.ico")

        # Declare text variables
        self.button_text = customtkinter.StringVar(value="START")
        self.server_ip_textfield_text = customtkinter.StringVar(value="127.0.0.1")
        self.target_ip_textfield_text = customtkinter.StringVar(value="www.example.com")
        self.target_port_textfield_text = customtkinter.StringVar(value="80")

        # define queues to communicate between the client thread and the gui thread
        self.in_queue = Queue()
        self.out_queue = Queue()

        self.client_logic_thread = threading.Thread(target=self.start_client)

        # Declare widgets
        self.title_label = customtkinter.CTkLabel(self.app, text=self.title, font=("Arial", 35))
        self.subtitle_label = customtkinter.CTkLabel(self.app, text=self.subtitle, font=("Arial", 25))

        self.server_ip_label = customtkinter.CTkLabel(self.app, text=self.server_ip_text, font=("Arial", 12))
        self.server_ip_textfield = customtkinter.CTkEntry(self.app, textvariable=self.server_ip_textfield_text, font=("Arial", 12))

        self.target_ip_label = customtkinter.CTkLabel(self.app, text=self.target_ip_text, font=("Arial", 12))
        self.target_ip_textfield = customtkinter.CTkEntry(self.app, textvariable=self.target_ip_textfield_text, font=("Arial", 12))

        self.target_port_label = customtkinter.CTkLabel(self.app, text=self.target_port_text, font=("Arial", 12))
        self.target_port_textfield = customtkinter.CTkEntry(self.app, textvariable=self.target_port_textfield_text, font=("Arial", 12))

        self.button = customtkinter.CTkButton(master=self.app, textvariable=self.button_text, command=self.button_function)

        self.place_widgets()


    # define a function which calls the client main in a seperate thread
    def start_client(self):
        client = ProxyClient(self.server_ip_textfield_text.get(), self.target_ip_textfield_text.get(), self.target_port_textfield_text.get(),
        # pass the in queue as the out queue and vice versa
        self.in_queue, self.out_queue)
        client.client_serve()


    # Declare widget actions
    def button_function(self):
        if self.button_text.get() == "START":
            self.client_logic_thread.start()
            self.button_text.set("STOP")
        else:
            # TODO: stop the client
            self.button_text.set("START")

    def place_widgets(self):
        # Place widgets
        self.title_label.place(relx=0.5, rely=0.15, anchor=customtkinter.CENTER)
        self.subtitle_label.place(relx=0.5, rely=0.30, anchor=customtkinter.CENTER)

        base_settings_y = 0.45
        diff_settings_items_y = 0.1
        settings_widgets = [(self.server_ip_label, self.server_ip_textfield), (self.target_ip_label, self.target_ip_textfield), (self.target_port_label, self.target_port_textfield)]

        for i, (label, textfield) in enumerate(settings_widgets):
            label.place(relx=0.1, rely=base_settings_y + diff_settings_items_y * i, anchor=customtkinter.CENTER)
            textfield.place(relx=0.85, rely=base_settings_y + diff_settings_items_y * i, anchor=customtkinter.CENTER)

        self.button.place(relx=0.5, rely=base_settings_y + diff_settings_items_y * len(settings_widgets), anchor=customtkinter.CENTER)

    # Add a listener to the x button on the gui
    def on_closing(self):
        self.app.destroy()
        # join the client thread to the main thread
        print("Sending the quit command")
        self.out_queue.put(QUIT_COMMAND)

        print("joining thread")
        self.client_logic_thread.join()

    def run_gui(self):
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Run the window
        self.app.mainloop()

        print("after mainloop")

if __name__ == '__main__':
    client_gui = ClientGUI()
    client_gui.run_gui()