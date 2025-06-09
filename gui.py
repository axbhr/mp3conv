import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
import conv
import threading

settings_var = False

# ---Funktionen und Klassen---
# GIF-Animation
class AnimatedGIF(ctk.CTkLabel):
    def __init__(self, master, gif_path, size=None):
        super().__init__(master, text="")
        self.size = size
        self.frames = []
        self.load_frames(gif_path)
        self.current_frame = 0
        self.animate()

    def load_frames(self, gif_path):
        pil_image = Image.open(gif_path)
        self.frames = []
        for frame in ImageSequence.Iterator(pil_image):
            if self.size:
                frame = frame.resize(self.size, Image.Resampling.LANCZOS)
            self.frames.append(ctk.CTkImage(frame.convert("RGBA"), size=self.size))

    def animate(self):
        self.configure(image=self.frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.after(50, self.animate)  # 20 FPS

# Download mit Thread
def start_download():
    url = url_entry.get()
    if not folder_path:
        chosen_path_label.configure(text="please choose a path!")
        return

    chosen_path_label.configure(text="downloading...")

    def download_thread():
        try:
            conv.download_mp3(url, folder_path, download_mp4_var.get())
            chosen_path_label.configure(text="download finished!")
        except Exception as e:
            chosen_path_label.configure(text=f"error: {str(e)}")
        finally:
            chosen_path_label.configure(text=f"chosen path: {folder_path}")
            url_entry.delete(0, "end")
            status_label.configure(text="")

    threading.Thread(target=download_thread, daemon=True).start()

# Einstellungsfenster
settings_win = None  # globale Variable

def open_settings():
    global settings_win
    if settings_win is not None and settings_win.winfo_exists():
        # Fenster ist schon offen → in den Vordergrund bringen
        global chosen_path_label
        chosen_path_label = ctk.CTkLabel(right_frame, text="settings is already open", font=ctk.CTkFont(size=12),
                                         text_color="#bbbbbb")
        settings_win.lift()
        settings_win.focus_force()
        return

    # Neues Fenster öffnen
    settings_win = ctk.CTkToplevel(app)
    settings_win.title("settings")
    settings_win.geometry("300x200")
    settings_win.resizable(False, False)

    label = ctk.CTkLabel(settings_win, text="settings", font=ctk.CTkFont(size=14))
    label.pack(pady=10, padx=10)

    download_mp4_switch = ctk.CTkSwitch(
        settings_win,
        text="download mp4",
        variable=download_mp4_var,
        onvalue=True,
        offvalue=False
    )
    download_mp4_switch.pack(pady=5)

    close_btn = ctk.CTkButton(settings_win, text="close", command=settings_win.destroy)
    close_btn.pack(pady=5)

    def on_close():
        global settings_win
        settings_win.destroy()
        settings_win = None

    settings_win.protocol("WM_DELETE_WINDOW", on_close)

# Gewählter Ordner
def select_folder():
    global folder_path
    folder_path = ctk.filedialog.askdirectory()
    if folder_path:
        print("Gewählter Ordner:", folder_path)
        chosen_path_label.configure(text=f"Chosen path: {folder_path}")
    else:
        chosen_path_label.configure(text="Chosen path: —")

# ---Allgemeines Fenster---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("colorscheme.json")

app = ctk.CTk()
app.title("yt-conv")
app.geometry("500x130")
app.resizable(False, False)
# app.overrideredirect(True)  # Entfernt die OS-Titelleiste

# Hauptframe für das Layout (horizontal)
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=7, pady=7)


# ---Globale Variablen---
folder_path = ""
download_mp4_var = ctk.BooleanVar(value=False)


# ---Links: animiertes Logo---
anim_gif = AnimatedGIF(main_frame, "sources/logo_glitch.gif", size=(150, 100))
anim_gif.pack(side="left", padx=(0,20), pady=7)


# ---Rechts: Eingabe und Buttons in einem vertikalen Frame---
right_frame = ctk.CTkFrame(main_frame)
right_frame.pack(side="left", fill="both", expand=True)

# Input + Ordnerwahl in einem horizontalen Frame
input_frame = ctk.CTkFrame(right_frame)
input_frame.pack(fill="x", pady=(0, 7))

url_entry = ctk.CTkEntry(input_frame, placeholder_text="URL...", font=ctk.CTkFont(size=14))
url_entry.pack(side="left", expand=True, fill="x", padx=(0,7))

select_folder_btn = ctk.CTkButton(
    input_frame,
    text="path",
    command=select_folder,
    width=80,
    height=23,
    fg_color="#5a5a5a",
    hover_color="#777777",
    text_color="white",
    corner_radius=10
)
select_folder_btn.pack(side="left")

# Buttons nebeneinander in einem eigenen Frame
buttons_frame = ctk.CTkFrame(right_frame)
buttons_frame.pack(fill="x", pady=(0, 10))

settings_button = ctk.CTkButton(
    buttons_frame,
    text="settings",
    command=open_settings,
    width=100,
    height=30,
    fg_color="#444444",
    hover_color="#555555",
    text_color="white",
    corner_radius=10,
    font=ctk.CTkFont(size=14)
)
settings_button.pack(side="left", padx=(0, 10))

download_button = ctk.CTkButton(
    buttons_frame,
    text="start",
    command=start_download,
    width=100,
    height=30,
    fg_color="#007aff",
    hover_color="#005ecb",
    text_color="white",
    corner_radius=15,
    font=ctk.CTkFont(size=16, weight="bold")
)
download_button.pack(side="left")

chosen_path_label = ctk.CTkLabel(right_frame, text="chosen path: —", font=ctk.CTkFont(size=12), text_color="#bbbbbb")
chosen_path_label.pack(fill="x", pady=(0, 10))

select_folder_btn.configure(command=select_folder)

status_label = ctk.CTkLabel(right_frame, text="", font=ctk.CTkFont(size=12), text_color="#bbbbbb")
status_label.pack(pady=(20,0))

app.bind("<Return>", lambda event: start_download())    #Startet den Download mit der "return"-Taste

app.mainloop()