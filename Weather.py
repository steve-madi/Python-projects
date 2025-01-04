import time
from tkinter import *
from tkinter import messagebox as mb
import requests
from plyer import notification
from PIL import Image, ImageTk  # For adding icons

# Function to get notification of weather report
def getNotification():
    cityName = place.get()  # getting input of name of the place from user
    baseUrl = "http://api.openweathermap.org/data/2.5/weather?"  # base URL to extract weather report
    try:
        # Complete URL to get weather conditions of a city
        url = baseUrl + "appid=" + 'd850f7f52bf19300a9eb4b0aa6b80f0d' + "&q=" + cityName
        response = requests.get(url)  # requesting the content of the URL
        x = response.json()  # converting it into JSON
        y = x["main"]  # getting the "main" key from the JSON object

        # Extracting weather details
        temp = y["temp"] - 273.15  # converting temperature from Kelvin to Celsius
        pres = y["pressure"]
        hum = y["humidity"]
        z = x["weather"]
        weather_desc = z[0]["description"]

        # Combining the above values as a string
        info = (
            f"Weather in {cityName}:\n"
            f"Temperature: {temp:.2f}°C\n"
            f"Pressure: {pres} hPa\n"
            f"Humidity: {hum}%\n"
            f"Condition: {weather_desc.capitalize()}"
        )

        # Showing the notification
        notification.notify(
            title="Your Weather Report",
            message=info,
            timeout=2
        )
        time.sleep(7)
    except Exception as e:
        mb.showerror('Error', f"An error occurred: {e}")

# Creating the main window
wn = Tk()
wn.title("Code 45 Weather App")
wn.geometry('800x500')
wn.configure(bg='#F5F5F5')

# Adding a background image
background_image = Image.open("background.jpg")  # Add a background image file
background_image = background_image.resize((800, 500), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)
background_label = Label(wn, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Customizing font styles
heading_font = ('Arial', 24, 'bold')
label_font = ('Arial', 16)
button_font = ('Arial', 14)

# Adding an icon
icon_image = Image.open("w-icon.png")  # Add an icon file
icon_image = icon_image.resize((80, 80), Image.LANCZOS)
icon_photo = ImageTk.PhotoImage(icon_image)
icon_label = Label(wn, image=icon_photo, bg='#F5F5F5')
icon_label.place(relx=0.5, rely=0.05, anchor=CENTER)

# Heading label
Label(
    wn, text="Code 45 Weather Notifier", font=heading_font, fg='#333333', bg='#F5F5F5'
).place(relx=0.5, rely=0.2, anchor=CENTER)

# Label for location input
Label(
    wn, text="Enter Location:", font=label_font, fg='#333333', bg='#F5F5F5'
).place(relx=0.3, rely=0.4, anchor=CENTER)

# Entry box for location input
place = StringVar()
place_entry = Entry(
    wn, width=30, textvariable=place, font=('Arial', 14), justify='center', bg='#FFFFFF', fg='#333333', insertbackground='#333333'
)
place_entry.place(relx=0.6, rely=0.4, anchor=CENTER)

# Button to get notification
btn = Button(
    wn,
    text='Get Notification',
    font=button_font,
    fg='white',
    bg='#0078D7',
    activebackground='#0053A0',
    activeforeground='white',
    command=getNotification
)
btn.place(relx=0.5, rely=0.6, anchor=CENTER)

# Hover effect for button
def on_enter(e):
    btn['bg'] = '#0053A0'

def on_leave(e):
    btn['bg'] = '#0078D7'

btn.bind('<Enter>', on_enter)
btn.bind('<Leave>', on_leave)

# Run the main event loop
wn.mainloop()
