from configparser import ConfigParser
from datetime import datetime
from os.path import isdir
from random import randint, seed
from sys import exit as sys_exit
from threading import Thread
from time import perf_counter, sleep
from tkinter import END, VERTICAL, WORD
from tkinter.messagebox import askyesno, showinfo, showwarning  # type: ignore
from tkinter.simpledialog import askstring
from typing import Any
from webbrowser import open_new
from zipfile import ZipFile

from customtkinter import (  # type: ignore
    DISABLED,
    CTk,
    CTkButton,
    CTkEntry,
    CTkImage,
    CTkLabel,
    CTkScrollbar,
    CTkSlider,
    CTkTextbox,
    CTkToplevel,
    E,
    N,
    S,
    W,
    set_appearance_mode,
)
from PIL import Image, ImageTk
from playsound import playsound  # type: ignore
from pyttsx3 import Engine, init  # type: ignore
from pyvolume import custom  # type: ignore

# pylint: disable=pointless-string-statement
"""Pigeon Scaring V2
By Gabriel Alonso-Holt.

Recommended/default settings: 2700 seconds (timer), 60 seconds (min time), 300 seconds (max time).

The days of having me run around scaring pigeons manually are over! 
With Pigeon Scaring, you can just start the program, 
choose a time to scare pigeons for, and relax as the pigeons fly away when you want.

Instructions:

1. Start program ("python main.pyw" is preferred, it's your choice how to run it, not mine)
2. Input your settings or use default settings, then click "scare the pigeons".
3. Every (minimum wait time - maximum wait time) minutes or seconds, you will hear a pigeon coo.
4. At least 1 pigeon should fly away every time the noise is played.
5. When the program finishes, you will see finish time and approximate number of pigeons scared.

"""

seed()

# Load config file
parser: ConfigParser = ConfigParser()
parser.read(r"psv2cfg.ini")

config: list[str] = parser.sections()

FMT: str = "%d.%m.%y %H:%M:%S"

# define a root element
root: CTk = CTk()
root.title(string="Pigeon Scaring V2")
root.geometry(geometry_string="400x400+200+200")
root.resizable(width=False, height=False)
set_appearance_mode("light")


def get_time(function: Any):
    """

    Times any function

    """

    def wrapper(*args: tuple[Any, ...], **kwargs: dict[Any, Any]) -> Any:

        start_time: float = perf_counter()

        response: Any = function(*args, **kwargs)
        end_time: float = perf_counter()
        total_time: float = end_time - start_time

        print(f"Time taken: {total_time:.2f} seconds.")

        return response

    return wrapper


def get_values() -> None:
    """

    Obtains and stores values from setting entry boxes.

    """

    global timer, min_time, max_time  # pylint: disable=global-variable-undefined

    try:

        timer = int(scaring_time.get())  # type: ignore

        min_time = int(x_time.get())  # type: ignore
        max_time = int(y_time.get())  # type: ignore

    # Use default settings
    except NameError:

        timer = int(parser[config[0]]["scaring_time"])

        min_time = int(parser[config[0]]["min_time"])
        max_time = int(parser[config[0]]["max_time"])

    scare_pigeons()


def scare_loop(start_config: str = "False") -> None:
    """

    Pigeon scaring loop with log window.

    """

    global timer, min_time, max_time, pigeon_path  # pylint: disable=global-variable-undefined global-variable-not-assigned

    log_window: CTkToplevel = CTkToplevel()
    log_window.title(string="pigeon log")
    log_window.geometry(geometry_string="300x300+400+200")
    log_window.attributes("-topmost", 1)  # type: ignore
    log_window.resizable(width=False, height=False)

    pigeon_image: Image.Image = Image.open(  # pylint: disable=redefined-outer-name
        r"pigeon.png"
    )

    # icon
    pigeon_icon: ImageTk.PhotoImage = ImageTk.PhotoImage(pigeon_image)
    root.iconphoto(False, pigeon_icon)

    pigeon_log: CTkTextbox = CTkTextbox(
        master=log_window, width=300, height=300, activate_scrollbars=True
    )
    pigeon_log.grid(sticky=N + E + S + W)  # type: ignore

    scroll_bar: CTkScrollbar = CTkScrollbar(master=pigeon_log)
    scroll_bar.grid(sticky=E)  # type: ignore

    pigeon_log.configure(yscrollcommand=scroll_bar.set)  # type: ignore

    pigeons_scared: int = 0

    if start_config == "True":

        min_time = int(parser[config[0]]["min_time"])
        max_time = int(parser[config[0]]["max_time"])
        timer = int(parser[config[0]]["scaring_time"])
        pigeon_path = r"media\pigeon.wav"

    else:

        timer = int(scaring_time.get())
        min_time = int(x_time.get())  # type: ignore
        max_time = int(y_time.get())  # type: ignore
        pigeon_path = r"media\pigeon.wav"

    # Scare pigeons in a loop until timer reaches 0
    while timer > 0:

        pause: int = randint(a=min_time, b=max_time)
        playsound(pigeon_path)  # pylint: disable=possibly-used-before-assignment
        sleep(3)
        
        for _ in range(10):
            playsound(pigeon_path)
        
        pigeon_log.insert(1.0, f"A pigeon was scared on {datetime.now():{FMT}}.\n")  # type: ignore pylint: disable=line-too-long
        pigeons_scared += 1
        sleep(pause)
        timer -= pause

    pigeon_log.configure(state=DISABLED)  # type: ignore

    # Show a message box when done.
    showinfo(
        title="Pigeon Scaring",
        message=f"Done!\nFinish time: {datetime.now():{FMT}}.\nPigeons scared: {pigeons_scared:,}",
    )

    # Save to file?
    save_confirmation: bool = askyesno(
        title="Pigeon Scaring", message="Do you want to save your logs to a file?"
    )
    if save_confirmation:

        with open(file=r"psv2_log.txt", mode="a", encoding="utf-8") as file:

            data: str = pigeon_log.get(index1=1.0, index2=END)  # type: ignore
            file.write(data)


def scare_pigeons() -> None:
    """Starts pigeon scaring in a separate thread."""

    start_value: str = parser[config[0]]["autostart"]

    thread: Thread = Thread(target=scare_loop, args={"autostart": start_value})
    thread.start()


def set_volume(volume: float) -> None:
    """Sets volume according to slider value"""

    custom(percent=int(volume))


def about_program() -> None:
    """Shows about window."""

    root_2: CTkToplevel = CTkToplevel()
    root_2.title(string="about this program")
    root_2.geometry(geometry_string="300x175")
    root_2.attributes("-topmost", 1)  # type: ignore
    root_2.resizable(width=False, height=False)

    # icon
    pigeon_icon: ImageTk.PhotoImage = ImageTk.PhotoImage(pigeon)  # type: ignore
    root_2.iconphoto(False, pigeon_icon)

    def github() -> None:
        """Self promo?"""

        open_new(r"github.com/Gabriel-H189/PigeonScaringV2")

    def extract_pigeon_effects() -> None:
        """Unzips a `media.zip` from the program directory."""

        file_path: str = r"media.zip"
        with ZipFile(file=file_path, mode="r") as zip_file:

            zip_file.extractall("media")

    about_label: CTkLabel = CTkLabel(
        master=root_2,
        text="Pigeon Scaring V2\nBy Gabriel Alonso-Holt",
        font=("calibri", 16, "bold"),
    )
    about_label.pack(pady=5)  # type: ignore

    gh_button: CTkButton = CTkButton(
        master=root_2, text="go to Gabriel's github", command=github
    )
    gh_button.pack(pady=7)  # type: ignore

    gull_effects_label: CTkLabel = CTkLabel(
        master=root_2, text="got gull effects?", font=("calibri", 16, "bold")
    )
    gull_effects_label.pack(pady=5)  # type: ignore

    extract_button: CTkButton = CTkButton(
        master=root_2, text="extract gull effects", command=extract_pigeon_effects
    )
    extract_button.pack()  # type: ignore

    if __name__ == "__main__":

        root_2.mainloop()


def autostart() -> None:
    """Autostart function only available through config file."""

    a_window: CTkToplevel = CTkToplevel()
    a_window.title(string="Autostart")
    a_window.attributes("-topmost", 1)  # type: ignore
    a_window.resizable(height=False, width=False)

    text: CTkTextbox = CTkTextbox(
        master=a_window, font=("calibri", 14, "bold"), wrap=WORD
    )
    text.pack()  # type: ignore

    abort: CTkButton = CTkButton(
        master=a_window, text="abort pigeon scaring", command=exit
    )
    abort.pack()  # type: ignore

    def start() -> None:

        text.insert(END, "Autostart in...")  # type: ignore

        for i in range(int(parser[config[0]]["autostart_delay"]), 0, -1):

            text.insert(END, f"{i}!\n")  # type: ignore
            sleep(1)

        scare_pigeons()

    if __name__ == "__main__":

        start()


def send_announcement() -> None:
    """Sends a Pigeon Wars public service announcement."""

    message = askstring("Send announcement", "Enter message: ")

    def _send_a() -> None:

        engine: Engine = init()  # type: ignore
        engine.setProperty("rate", 140)  # type: ignore
        engine.say(f"This is a Pigeon Wars public service announcement. {message}")  # type: ignore

        engine.runAndWait()  # type: ignore

    thread: Thread = Thread(target=_send_a)
    thread.start()


def check_media_folder() -> None:
    """Verifies that sound effects are available."""

    if not isdir(r"media"):

        showwarning(title="No sound effects", message="No media folder present!")


pigeon: Image.Image = Image.open(fp=r"pigeon.png")
pigeon_image: CTkImage = CTkImage(pigeon)

si_label: CTkLabel = CTkLabel(master=root, text="", image=pigeon_image)
si_label.pack()  # type: ignore

# Icon
icon: ImageTk.PhotoImage = ImageTk.PhotoImage(pigeon)
root.iconphoto(True, icon)

ss_label: CTkLabel = CTkLabel(master=root, text="Pigeon Scaring", font=("arial", 16))
ss_label.pack()  # type: ignore

ts_label: CTkLabel = CTkLabel(master=root, text="Timer in seconds: ")
ts_label.place(x=90, y=53)  # type: ignore

scaring_time: CTkEntry = CTkEntry(master=root)
scaring_time.place(x=80, y=77)  # type: ignore
scaring_time.insert(0, parser[config[0]]["scaring_time"])  # type: ignore

xt_label: CTkLabel = CTkLabel(master=root, text="Minimum time: ")
xt_label.place(x=90, y=105)  # type: ignore

x_time: CTkEntry = CTkEntry(master=root)
x_time.place(x=80, y=130)  # type: ignore
x_time.insert(0, parser[config[0]]["min_time"])  # type: ignore

mt_label: CTkLabel = CTkLabel(master=root, text="Maximum time: ")
mt_label.place(x=90, y=161)  # type: ignore

y_time: CTkEntry = CTkEntry(master=root)
y_time.place(x=80, y=188)  # type: ignore
y_time.insert(0, parser[config[0]]["max_time"])  # type: ignore

scare_button: CTkButton = CTkButton(
    master=root, text="scare the pigeons", command=get_values
)
scare_button.place(x=80, y=250)  # type: ignore

send_button: CTkButton = CTkButton(
    master=root, text="send announcement", command=send_announcement
)
send_button.place(x=80, y=290)  # type: ignore

volume_label: CTkLabel = CTkLabel(master=root, text="Volume")
volume_label.place(x=265, y=110)  # type: ignore

slider: CTkSlider = CTkSlider(
    master=root, from_=0, to=100, orientation=VERTICAL, command=set_volume
)
slider.place(x=275, y=140)  # type: ignore
slider.set(int(parser[config[0]]["default_volume"]))  # type: ignore

about_button: CTkButton = CTkButton(
    master=root, text="about", width=10, command=about_program
)
about_button.place(x=265, y=350)  # type: ignore

if parser[config[0]]["autostart"] == "True":

    autostart()

check_media_folder()

# Start program
if __name__ == "__main__":

    root.mainloop()  # type: ignore
    sys_exit()
