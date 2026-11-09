import cv2
import time
import winsound 
import os

# Dynamically grab the exact folder path where this python script lives
current_folder = os.path.dirname(os.path.abspath(__file__))
custom_audio = os.path.join(current_folder, "walangkanenbuseng.wav")

# Print the path so you can verify it is looking in the right place!
print(f"Loading alarm audio from: {custom_audio}")

# Initialize the webcam
cap = cv2.VideoCapture(0)
time.sleep(2)

# Step 1: Capture the STATIC baseline "empty room" frame
print("Capturing background... Please ensure the frame is empty!")
ret, baseline_frame = cap.read()

baseline_gray = cv2.cvtColor(baseline_frame, cv2.COLOR_BGR2GRAY)
baseline_blur = cv2.GaussianBlur(baseline_gray, (21, 21), 0)

# Variables to handle the persistent state and auto-reset timer
alarm_triggered = False
last_motion_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (21, 21), 0)

    # Compare CURRENT frame to the STATIC empty room
    diff = cv2.absdiff(baseline_blur, blur)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Flag to track if we saw movement in this specific frame
    motion_detected_this_frame = False

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        
        motion_detected_this_frame = True
        
        # Draw the tracking box
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # --- ENHANCED AUDIO & LOOP LOGIC ---
    if motion_detected_this_frame:
        if not alarm_triggered:
            print("MOTION DETECTED! Alarm activated.")
            # SND_FILENAME reads your custom .wav file
            # SND_ASYNC plays it in the background so the camera doesn't freeze
            # SND_LOOP forces the audio to repeat infinitely until stopped
            winsound.PlaySound(custom_audio, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
        
        alarm_triggered = True
        # Reset the timer because they are still moving
        last_motion_time = time.time()
        
    else:
        # If there is no motion, check if 3 seconds have passed
        if alarm_triggered and (time.time() - last_motion_time > 3):
            print("3 seconds of quiet. Stopping alarm and auto-resetting background...")
            alarm_triggered = False
            
            # Passing None with SND_PURGE stops the audio from looping
            winsound.PlaySound(None, winsound.SND_PURGE)
            
            # Take a fresh picture of the room to recalibrate
            ret, new_baseline = cap.read()
            baseline_gray = cv2.cvtColor(new_baseline, cv2.COLOR_BGR2GRAY)
            baseline_blur = cv2.GaussianBlur(baseline_gray, (21, 21), 0)

    # Display the persistent UI
    if alarm_triggered:
        cv2.putText(frame, "INTRUDER ALERT! (Auto-reset in 3s)", (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Display the final security feed
    cv2.imshow("Motion-Triggered Security Tracker", frame)

    key = cv2.waitKey(10)
    
    if key == ord('q'):
        # Ensure audio stops if you quit while the alarm is ringing
        winsound.PlaySound(None, winsound.SND_PURGE)
        break
    
    elif key == ord('r'):
        print("Manual reset forced. Stopping alarm and recalibrating...")
        alarm_triggered = False
        
        # Stop the looping audio manually
        winsound.PlaySound(None, winsound.SND_PURGE)
        
        ret, new_baseline = cap.read()
        baseline_gray = cv2.cvtColor(new_baseline, cv2.COLOR_BGR2GRAY)
        baseline_blur = cv2.GaussianBlur(baseline_gray, (21, 21), 0)

# Clean up resources
cap.release()
cv2.destroyAllWindows()