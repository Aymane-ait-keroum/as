import tkinter as tk
from tkinter import messagebox
import requests

API_KEY = "6c7736986786bb4fcacabab9f8d84eef"

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            return f"93ma l9ina had mdina: {data.get('message', '')}"
        weather = data["weather"][0]["description"].capitalize()
        temperature = data["main"]["temp"]
        return f"Ta9ss f {city}: {weather}, {temperature}°C"
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la récupération : {e}"

def ask_question():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Fin tatskon?")
        return

    answer = messagebox.askquestion("Question", f"Wach tatsken f {city}?")
    if answer == 'yes':
        result_label.config(text="Toul mn cherjam hhhh")
    else:
        weather_info = get_weather(city)
        result_label.config(text=weather_info)

root = tk.Tk()
root.title("⛅ Weather App Marocaine")
root.geometry("420x280")
root.configure(bg="#f0f8ff")

frame = tk.Frame(root, bg="#f0f8ff")
frame.pack(pady=20)

title_label = tk.Label(frame, text="⛅ Ta9ss Dial Lyoum", font=("Helvetica", 16, "bold"), bg="#f0f8ff", fg="#333")
title_label.pack(pady=10)

city_entry = tk.Entry(frame, width=30, font=("Helvetica", 12), justify='center')
city_entry.pack(pady=5)

submit_button = tk.Button(frame, text="🔍 Vérifier", command=ask_question, font=("Helvetica", 11), bg="#4CAF50", fg="white", relief="raised", bd=3)
submit_button.pack(pady=10)

result_label = tk.Label(
    root,
    text="",
    font=("Helvetica", 12),
    fg="#1e90ff",
    bg="#f0f8ff",
    wraplength=380,
    justify="center"
)
result_label.pack(pady=10)

root.mainloop()
