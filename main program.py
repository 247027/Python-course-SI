import tkinter as tk
import requests
import functions as f

HEIGHT = 200
WIDTH = 300

root = tk.Tk()
root['bg'] = '#ffe0b3'
root.title('Wallet')
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="#ffe0b3")
canvas.pack()

label = tk.Label(root, text="WELCOME IN YOUR WALLET ", bg="#ffe0b3")
label.place(relx=0.1, rely=0.1, relheight=0.1, relwidth=0.8)

button = tk.Button(root, text="SHOW PROFIT", bg='gray', command=f.show_profit_pressed)
button.place(relx=0.1, rely=0.3, relheight=0.15, relwidth=0.8)

button = tk.Button(root, text="SHOW RESOURCES", bg='gray', command=f.show_resources_pressed)
button.place(relx=0.1, rely=0.45, relheight=0.15, relwidth=0.8)

button = tk.Button(root, text="UPDATE RESOURCE", bg='gray', command=f.update_pressed)
button.place(relx=0.1, rely=0.60, relheight=0.15, relwidth=0.8)

button = tk.Button(root, text="DELETE RESOURCE", bg='gray', command=f.delete_pressed)
button.place(relx=0.1, rely=0.75, relheight=0.15, relwidth=0.8)

root.mainloop()
