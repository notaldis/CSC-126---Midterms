# Motion-Triggered Security Tracker

**Course:** CSC 126 (Graphics and Visual Computing)  
**Developers:** Aldis S. Valdehueza, Laurence Paul jigger R. Egay, Jiefhox G. Monter

## Project Description
The Motion-Triggered Security Tracker is a Python-based computer vision application built using OpenCV. It functions as an automated surveillance system that captures a static baseline of an empty room and continuously monitors the live webcam feed for significant pixel changes. 

Instead of relying on basic motion detection, this system features a **Persistent Intruder Alarm State**. When an intruder is detected, the system draws a tracking box around them, displays a visual warning, and continuously loops a custom audio alarm (`walangkanenbuseng.py`). If the environment remains completely still for 3 seconds, the system automatically purges the alarm, captures a fresh environmental baseline, and resumes quiet monitoring.

### Key OpenCV Techniques Used:
1. **Image Operations:** Grayscale conversion and Gaussian Blurring to optimize performance and reduce camera noise.
2. **Image Analysis:** Absolute Difference (`cv2.absdiff`) and Binary Thresholding to mathematically isolate new objects from the background.
3. **Motion Tracking:** Contour extraction and Bounding Boxes to visually track intruders on the live feed.

---

## Prerequisites
* Python 3.10+ (Installed via python.org, **NOT** the Windows Store or MSYS2).
* A working webcam.
* Windows OS (Required for the `winsound` audio integration).

---

## Setup Instructions

We utilize the standard Windows Command Prompt (`cmd`) and the `py` launcher to ensure a clean environment setup, bypassing PowerShell script execution restrictions.

1. **Clone or Download the Repository**
   Extract the files into a workspace folder named `midterms`. Ensure `security_tracker.py` and `walangkanenbuseng.wav` are in the root of this folder.

2. **Open Command Prompt**
   Open a terminal and navigate to your `midterms` folder.

3. **Create the Virtual Environment**
   Run the following command to force Windows to use the standard Python installation:
   ```cmd
   py -m venv midtermenv
   ```

4. **Activate the Environment**
   ```cmd
   midtermenv\Scripts\activate.bat
   ```

5. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

---

## How to Run the Application

1. Ensure your virtual environment is active (you should see `(midtermenv)` in your terminal).
2. Ensure your custom audio file `walangkanenbuseng.wav` is in the same folder as the script.
3. Execute the script:
   ```cmd
   python security_tracker.py
   ```
4. **Initialization:** The moment the camera activates, step out of the frame. The console will read: `"Capturing background... Please ensure the frame is empty!"`
5. **Testing:** Walk into the frame to trigger the tracking boxes and the custom looping audio alarm. 
6. **Auto-Reset:** Stand completely still or leave the frame for 3 seconds. The alarm will silence, and the system will recalibrate to the new background.
7. **Manual Override:** Press **'r'** on your keyboard to manually stop the alarm and force a background recalibration.
8. **Quit:** Press **'q'** on your keyboard to shut down the security system.