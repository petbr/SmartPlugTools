# by Antoni Gual Via 4/2015

from tkinter import Tk, Canvas, PhotoImage,NW,mainloop 
import time
#from time import clock


def mandel_pixel(c):
  """ calculates the color index of the mandelbrot plane point passed in the arguments """
  maxIt = 256
  z =  c   
  for i in range(maxIt):
      a = z * z
      z=a + c
      if a.real  >= 4.:
         return i
  return maxIt

def mandelbrot(xa,xb,ya,yb,x,y):
    """ returns a mandelbrot in a string for Tk PhotoImage"""
    #color string table in Photoimage format #RRGGBB 
    clr=[ ' #%02x%02x%02x' % (int(255*((i/255)**.25)),0,0) for i in range(256)]
    clr.append(' #000000')  #append the color of the centre as index 256
    #calculate mandelbrot x,y coordinates for each screen pixel
    xm=[xa + (xb - xa) * kx /x  for kx in range(x)]
    ym=[ya + (yb - ya) * ky /y  for ky in range(y)]
    #build the Photoimage string by calling mandel_pixel to index in the color table
    return" ".join((("{"+" ".join(clr[mandel_pixel(complex(i,j))] for i in xm))+"}" for j in ym))



#window size
x=12
y=9
#corners of  the mandelbrot plan to display  
xa = -2.0; xb = 1.0
ya = -1.27; yb = 1.27

#Tkinter window
window = Tk()
canvas = Canvas(window, width = x, height = y, bg = "#000000");canvas.pack()
img = PhotoImage(width = x, height = y)
canvas.create_image((0, 0), image = img, state = "normal", anchor = NW)

#do the mandelbrot 
t1=time.process_time()
#img.put(mandelbrot(xa,xb,ya,yb,x,y))
s=mandelbrot(xa,xb,ya,yb,x,y)
print("s = ", s)
img.put(s)
print(time.process_time()-t1, ' seconds')

ss={}
ss.union({#000000 #000000 #000000})
ss.union({#000000 #000000 #000000})
ss.union({#000000 #000000 #000000})

ss={#4b0000  #4b0000  #4b0000  #5f0000  #530000  #6b0000  #4b0000  #4b0000  #530000  #5f0000  #4b0000  #4b0000}
ss.add({ #4b0000  #4b0000  #4b0000  #5a0000  #530000  #530000  #5a0000  #5f0000  #740000  #630000  #4b0000  #4b0000})
ss.add({ #5a0000  #4b0000  #4b0000  #4b0000  #630000  #5a0000  #670000  #7f0000  #760000  #630000  #5a0000  #5f0000})
ss.add({ #530000  #630000  #670000  #6b0000  #670000  #740000  #000000  #000000  #000000  #000000  #630000  #530000})
ss.add({ #5a0000  #530000  #710000  #7f0000  #000000  #8b0000  #000000  #000000  #000000  #000000  #5f0000  #4b0000})
ss.add({ #5a0000  #530000  #710000  #7f0000  #000000  #8b0000  #000000  #000000  #000000  #000000  #5f0000  #4b0000})
ss.add({ #530000  #630000  #670000  #6b0000  #670000  #740000  #000000  #000000  #000000  #000000  #630000  #530000})
ss.add({ #5a0000  #4b0000  #4b0000  #4b0000  #630000  #5a0000  #670000  #7f0000  #760000  #630000  #5a0000  #5f0000})
ss.add({ #4b0000  #4b0000  #4b0000  #5a0000  #530000  #530000  #5a0000  #5f0000  #740000  #630000  #4b0000  #4b0000})

print("ss = ", ss)
mainloop()
