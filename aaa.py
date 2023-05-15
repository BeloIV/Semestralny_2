import tkinter as tk

def _on_mousewheel(event):
    print(event)
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

root = tk.Tk()

# create a canvas
canvas = tk.Canvas(root, width=300, height=200)
canvas.pack()

# add content to the canvas
frame = tk.Frame(canvas)
canvas.create_window((0,0), window=frame, anchor='nw')

for i in range(50):
    tk.Label(frame, text=f"Label {i}").pack()

# create a scrollbar and attach it to the canvas
scrollbar = tk.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

# update the scroll region to match the size of the frame
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox('all'))

# bind the mouse wheel event to the canvas
canvas.bind_all("<MouseWheel>", _on_mousewheel)

root.mainloop()