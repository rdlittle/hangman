from PIL import Image, ImageTk, ImageSequence
from tkinter import Canvas, Tk, NW

class Winner:
    def __init__(self, canvas):
        self.canvas = canvas
        self.sequence = [ImageTk.PhotoImage(img.resize((150, 200))) for img in ImageSequence.Iterator(Image.open('winner.gif'))] 
        self.image = self.canvas.create_image(0, 0, anchor=NW, image = self.sequence[0])
        self.animating = True
        self.animate(0)
        
    def animate(self, counter):
        self.canvas.itemconfig(self.image, image=self.sequence[counter])
        if not self.animating:
            return
        self.canvas.after(50, lambda: self.animate((counter+1) % len(self.sequence)))
        

class Loser:
    def __init__(self, canvas):
        self.canvas = canvas
        self.sequence = [ImageTk.PhotoImage(img.resize((200, 200))) for img in ImageSequence.Iterator(Image.open('loser.gif'))] 
        self.image = self.canvas.create_image(0, 0, anchor=NW, image = self.sequence[0])
        self.animating = True
        self.animate(0)
        
    def animate(self, counter):
        self.canvas.itemconfig(self.image, image=self.sequence[counter])
        if not self.animating:
            return
        self.canvas.after(50, lambda: self.animate((counter+1) % len(self.sequence)))        
        
if __name__ == '__main__':        
    app = Tk()
    canvas = Canvas(app, width=200, height=200)
    #w = Winner(canvas)
    l = Loser(canvas)
    app.mainloop()
