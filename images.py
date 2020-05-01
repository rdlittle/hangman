from PIL import Image, ImageTk, ImageSequence
from tkinter import Canvas, Tk, NW
import sys

"""
To be honest, I had no idea how to animate a gif with tkinter.
I got the solution from https://www.youtube.com/watch?v=lYIy4nJd7P8
"""

class Picture:
    def __init__(self, canvas, image_name):
        self.canvas = canvas
        self.image_name = image_name
        """ I know there's a better way to do this.
        I'll figure it out eventually
        """
        width = 200
        if self.image_name == 'winner.gif':
            width = 150
        """
        TODO: Remove hard coded width and still keep proportions
        """
        self.sequence = [ImageTk.PhotoImage(img.resize((width, 200))) 
                         for img in ImageSequence.Iterator(Image.open(self.image_name))] 
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
    if len(sys.argv) == 1:
        image_name = 'winners.gif'
    else:
        image_name = sys.argv[1]
    if image_name not in ['winner.gif', 'loser.gif']:
        image_name = 'winner.gif'
    canvas = Canvas(app, width=200, height=200)
    canvas.pack()
    l = Picture(canvas, image_name)
    app.mainloop()
