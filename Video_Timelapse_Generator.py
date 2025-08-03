import sys
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import threading
import sys

# High DPI awareness for Windows
if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # DPI aware
    except Exception:
        pass

# High DPI awareness (for Windows)
if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

def select_video():
    filepath = filedialog.askopenfilename(
        filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
    )
    if filepath:
        video_path.set(filepath)
        show_thumbnail(filepath)

def show_thumbnail(path):
    global original_width, original_height
    cap = cv2.VideoCapture(path)
    ret, frame = cap.read()
    if ret:
        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Pre-fill resolution fields
        res_width.set(str(original_width))
        res_height.set(str(original_height))

        # Show thumbnail
        frame = cv2.resize(frame, (200, 120))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image)
        thumbnail_label.config(image=photo)
        thumbnail_label.image = photo
    cap.release()

def generate_timelapse_thread():
    threading.Thread(target=generate_timelapse).start()

def generate_timelapse():
    input_path = video_path.get()
    if not input_path or not os.path.exists(input_path):
        messagebox.showerror("Error", "Please select a valid video file.")
        return

    try:
        skip = int(skip_frames.get())
        if skip < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Frame skip must be a positive integer.")
        return

    try:
        res_w = int(res_width.get())
        res_h = int(res_height.get())
        if res_w <= 0 or res_h <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Resolution must be positive integers.")
        return

    output_path = filedialog.asksaveasfilename(
        defaultextension=".mp4",
        filetypes=[("MP4 files", "*.mp4")],
        title="Save Time-lapse Video As"
    )
    if not output_path:
        return

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not open video file.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (res_w, res_h))

    frame_count = 0
    written_frames = 0

    progress_bar["maximum"] = total_frames

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % skip == 0:
            frame_resized = cv2.resize(frame, (res_w, res_h))
            out.write(frame_resized)
            written_frames += 1

        frame_count += 1
        progress_bar["value"] = frame_count
        progress_label.config(text=f"Processing frame {frame_count}/{total_frames}")
        root.update_idletasks()

    cap.release()
    out.release()
    progress_bar["value"] = 0
    progress_label.config(text="")
    messagebox.showinfo("Success", f"Time-lapse video saved!\nFrames written: {written_frames}")

# --- GUI Setup ---
root = tk.Tk()
root.tk.call('tk', 'scaling', 1.5)  # Adjust this as needed
root.title("🎞️ Time-lapse Video Generator")
root.geometry("600x600")
root.resizable(False, False)
root.configure(bg="#f0f0f5")

# Improve sharpness on HiDPI displays
root.tk.call('tk', 'scaling', 1.5)  # Adjust to 2.0 for 4K screens

# --- Style ---
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Segoe UI", 10), foreground="#333")
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6, background="#4CAF50", foreground="white")
style.map("TButton", background=[("active", "#45a049")])
style.configure("TEntry", font=("Segoe UI", 10), padding=4)

# --- Variables ---
video_path = tk.StringVar()
skip_frames = tk.StringVar(value="10")
res_width = tk.StringVar(value="1920")
res_height = tk.StringVar(value="1080")

# --- Layout ---
frame = ttk.Frame(root, padding=20)
frame.pack(expand=True, fill=tk.BOTH)

ttk.Label(frame, text="🎥 Select Video File:").pack(anchor="w", pady=(0, 5))
ttk.Entry(frame, textvariable=video_path, width=50).pack()
ttk.Button(frame, text="Browse", command=select_video).pack(pady=8)

thumbnail_label = ttk.Label(frame)
thumbnail_label.pack(pady=5)

ttk.Label(frame, text="⏩ Skip every N frames (e.g., 10):").pack(anchor="w", pady=(10, 5))
ttk.Entry(frame, textvariable=skip_frames, width=10).pack()

ttk.Label(frame, text="📏 Output Resolution (width x height):").pack(anchor="w", pady=(10, 5))
res_frame = ttk.Frame(frame)
res_frame.pack()
ttk.Entry(res_frame, textvariable=res_width, width=8).pack(side="left")
ttk.Label(res_frame, text=" x ").pack(side="left")
ttk.Entry(res_frame, textvariable=res_height, width=8).pack(side="left")

ttk.Button(frame, text="Generate Time-lapse", command=generate_timelapse_thread).pack(pady=15)

progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=5)

progress_label = ttk.Label(frame, text="")
progress_label.pack()

ttk.Label(frame, text="© 2025 Emmanuel Amdany | Powered by OpenCV", font=("Segoe UI", 8), foreground="#888").pack(side="bottom", pady=5)

root.mainloop()