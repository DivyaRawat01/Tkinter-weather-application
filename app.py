from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
import requests
import json
from itertools import count

current_animation=None

def load_gif_frames(path):
    #Load all frames of a GIF into a list of PhotoImage objects.
    gif = Image.open(path)
    frames = []
    try:
        for i in count(0):
            gif.seek(i)
            frame = ImageTk.PhotoImage(gif.copy())
            frames.append(frame)
    except EOFError:
        pass
    return frames

def animate_gif(label, frames, delay, idx=0):
    #Loop through frames and update label image.
    global current_animation
    frame = frames[idx]
    label.config(image=frame)
    label.image = frame  # keep reference
    current_animation=label.after(delay, animate_gif, label, frames, delay, (idx+1) % len(frames))

def get_Weather():
    global current_animation

    city = city_dropdown.get()
    api_key = "Enter your API key"
    api_url = (
        fr'https://api.openweathermap.org/data/2.5/weather?q={city}'
        f'&appid={api_key}&units=metric'
    )
    server_dt = requests.get(api_url)
    server_dt_json = server_dt.json()

    # Weather data
    temp = server_dt_json["main"]["temp"]
    feels = server_dt_json["main"]["feels_like"]
    temp_min = server_dt_json["main"]["temp_min"]
    temp_max = server_dt_json["main"]["temp_max"]
    humidity = server_dt_json["main"]["humidity"]
    pressure = server_dt_json["main"]["pressure"]
    weather = server_dt_json["weather"][0]["description"].lower()
    wind_speed = server_dt_json["wind"]["speed"]

    final_weather = (
        f"Overall Weather: {weather}\n"
        f"Wind Speed: {wind_speed} m/s\n"
        f"Temperature: {temp} °C\n"
        f"Feels Like: {feels} °C\n"
        f"Minimum Temperature: {temp_min} °C\n"
        f"Maximum Temperature: {temp_max} °C\n"
        f"Humidity: {humidity} %\n"
        f"Pressure: {pressure} hPa"
    )

    # --- Choose GIF based on weather ---
    gif_map = {
        "clear": r"E:\project\WeatherApp\sunny.gif",
        "rain": r"E:\project\WeatherApp\rain.gif",
        "drizzle": r"E:\project\WeatherApp\rain.gif",
        "thunderstorm": r"E:\project\WeatherApp\rain.gif",
        "cloud": r"E:\project\WeatherApp\cloud.gif",
        "snow": r"E:\project\WeatherApp\snow.gif",
        "mist": r"E:\project\WeatherApp\fog.gif",
        "haze": r"E:\project\WeatherApp\fog.gif",
        "fog": r"E:\project\WeatherApp\fog.gif"
    }

    chosen_gif = None
    for key, path in gif_map.items():
        if key in weather:
            chosen_gif = path
            break
    
    if current_animation:
        gif_label.after_cancel(current_animation)

    if chosen_gif:
        frames = load_gif_frames(chosen_gif)
        animate_gif(gif_label, frames, delay=100)  
    
    output_lable.config(
        text=final_weather,
        fg="white",
        font=("Georgia",13,"bold"),
        bg="black"
    )
    output_lable.lift()
    output_frame.pack(pady=15)
        
#GUI design
root=Tk()
root.geometry("500x600")
root.resizable(True,True)
root.title("Weather Application")  #tile of application

# set backgroud image
bg_img_path=Image.open(r"E:\project\WeatherApp\cloud_sky_bg.jpg")
bg_img=ImageTk.PhotoImage(bg_img_path)
bg_img_lbl=Label(root,image=bg_img)
bg_img_lbl.place(relheight=1,relwidth=1)

#heading
Label(root,text="My Weather App",font=("Georgia",25),bg="sky blue",fg="dark blue").pack(pady=10)

Label(root,text="Select a city",font=("Georgia",18),bg="Light gray",width=25).pack(pady=15)

#Drop down 
city_choices=["Dehradun","Delhi","Mumbai","Lucknow","Rudraprayag","Goa","Noida"]
city_dropdown=ttk.Combobox(root,text="Select city",values=city_choices,font=("Georgia",18),width=15,height=10)
city_dropdown.pack(pady=15)
city_dropdown.current(0)

#button
weather_btn=Button(root,text="Get Weather",font=("Georgia",18),bg="Dark blue",fg="white",border=2,command=get_Weather)
weather_btn.pack(pady=20)

#output Frame
output_frame=Frame(root,highlightthickness=10)

gif_label=Label(output_frame)
gif_label.pack()

output_lable=Label(output_frame,text="",font=("Georgia",13),fg="white",bg="black")
output_lable.place(relx=0.5, rely=0.5,anchor="center")

root.mainloop()

