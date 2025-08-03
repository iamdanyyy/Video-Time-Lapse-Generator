# 🎞️ Time-lapse Video Generator

A simple and elegant desktop GUI tool built with **Python** and **Tkinter** that generates time-lapse videos from existing video files. Powered by **OpenCV**, it allows users to skip frames and set custom output resolutions.

---

## 🖥️ Features

* 📂 Load video files (`.mp4`, `.avi`, `.mov`, `.mkv`)
* 🖼️ Preview a thumbnail of the selected video
* ⏩ Set frame skipping interval (e.g., every 10th frame)
* 📏 Define custom output resolution
* 📊 Visual progress bar with frame count
* 💾 Save processed time-lapse video as `.mp4`
* ⚡ High-DPI aware for sharpness on 4K screens
* 🧵 Multi-threaded to keep UI responsive

---

## 🛠️ Requirements

* Python 3.7+
* [OpenCV](https://pypi.org/project/opencv-python/)
* [Pillow](https://pypi.org/project/Pillow/)

### 📦 Installation

Install dependencies using pip:

```bash
pip install opencv-python Pillow
```

---

## ▶️ How to Use

1. **Run the script**:

   ```bash
   python Video_Timelapse_Generator.py
   ```

2. **Select a video file** using the "Browse" button.

3. A **thumbnail** will be displayed and default resolution populated.

4. Adjust the **frame skip** value (e.g., `10` to use every 10th frame).

5. Set a **custom resolution** or keep the default.

6. Click **"Generate Time-lapse"**.

7. Choose where to **save the output** `.mp4` file.

8. A progress bar will show processing status. Once done, a success message will appear.

---

## 🧩 File Structure

```
Video_Timelapse_Generator.py        # Main GUI script (this file)
README.md               # This file
```

---

## 📸 Screenshot

*(Optional: Add a screenshot of the GUI here)*

---

## 👨‍💻 Author

**Emmanuel Amdany**
© 2025 — All rights reserved.

---

## 🔖 License

This project is open for personal and educational use. Attribution appreciated.

---
