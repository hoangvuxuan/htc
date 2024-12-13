import tkinter as tk
from subprocess import Popen

def open_play_online():

    try:
        Popen(["python", "./client/client1.py"])
    except Exception as e:
        print(f"Error opening Play Online: {e}")

def play_with_ai():
    Popen(["python", "client1.py", "AI"])

main_window = tk.Tk()
main_window.title("Tic Tac Toe Menu")
main_window.geometry("300x200")

title_label = tk.Label(main_window, text="Tic Tac Toe", font=("Arial", 18, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=20)


play_online_button = tk.Button(main_window, text="Play Online", font=("Arial", 14), command=open_play_online)
play_online_button.grid(row=1, column=0, padx=10, pady=10)


play_ai_button = tk.Button(main_window, text="Play with AI", font=("Arial", 14), command=play_with_ai)
play_ai_button.grid(row=1, column=1, padx=10, pady=10)

main_window.mainloop()
