import tkinter as tk
from PIL import Image, ImageTk
global xs, ys, xt, yt
count = 0
# --- functions ---

def on_click(event=None):
    # `command=` calls function without argument
    # `bind` calls function with one argument
    print("image clicked")

def callback(event=None):
    global count, xs, ys, xt, yt
    if count == 0:
        xs = event.x
        ys = event.y
    elif count == 1:
        xt = event.x
        yt = event.y
    count +=1
    print("clicked at", event.x, event.y)

# --- main ---

# init    
root = tk.Tk()
root.geometry('500x500')
# load image
image = Image.open("mazyboi/maze2.png")
out = image.resize((500,500))
photo = ImageTk.PhotoImage(out)

# label with image
l = tk.Label(root, image=photo)
l.pack()

# bind click event to image
l.bind('<Button-1>', callback)

# button with image binded to the same function 
b = tk.Button(root, image=photo, command=callback)
b.pack()

# button with text closing window
b = tk.Button(root, text="Close", command=root.destroy)
b.pack()

# "start the engine"
root.mainloop()