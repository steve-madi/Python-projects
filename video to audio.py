import moviepy.editor
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import *

window = Tk()
# Set the size of the tkinter window
window.geometry("700x350")
window.title("PythonGeeks")  # Give title to the window

Label(window, text="VIDEO TO AUDIO CONVERTER", bg='orange', font=('Calibri', 15)).pack()
Label(window, text="Choose a File ").pack()

video = None  # Initialize video as None


def browse():  # Browsing function
    global video
    try:
        filepath = askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv")])
        if filepath:
            video = moviepy.editor.VideoFileClip(filepath)
            pathlab.config(text=f"Selected: {filepath}")
        else:
            pathlab.config(text="No file selected")
    except Exception as e:
        pathlab.config(text=f"Error: {e}")


def save():
    global video
    if video is None:
        Label(window, text="No video selected!", bg='red', font=('Calibri', 15)).pack()
        return
    try:
        output_path = asksaveasfilename(defaultextension=".wav", filetypes=[("Audio files", "*.wav")])
        if output_path:
            audio = video.audio  # Convert to audio
            audio.write_audiofile(output_path)  # Save as audio
            Label(window, text="Video converted to audio and saved successfully!", bg='blue', font=('Calibri', 15)).pack()
        else:
            Label(window, text="Save operation canceled.", bg='yellow', font=('Calibri', 15)).pack()
    except Exception as e:
        Label(window, text=f"Error: {e}", bg='red', font=('Calibri', 15)).pack()


pathlab = Label(window)
pathlab.pack()

# Creating buttons
Button(window, text='Browse', command=browse).pack()
Button(window, text='Save', command=save).pack()

window.mainloop()
