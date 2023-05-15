import tkinter as tk

def resize_canvas(event):
    canvas.configure(width=event.width, height=event.height)

root = tk.Tk()
root.title("Resizable Canvas")

# Vytvoření plátna
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True)

# Připojení funkce resize_canvas k události změny velikosti okna
root.bind("<Configure>", resize_canvas)

# Přidání obsahu na plátno
canvas.create_rectangle(50, 50, 200, 200, fill="red")

root.mainloop()