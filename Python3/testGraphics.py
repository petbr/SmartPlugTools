from graphics import *


def main():
    win = GraphWin('Face', 450, 450) # give title and dimensions
    #win.yUp() # make right side up coordinates!

    head = Circle(Point(40,100), 25) # set center and radius
    head.setFill("yellow")
    head.draw(win)

    # Left eye
    eye1 = Circle(Point(30, 90), 5)
    eye1.setFill('blue')
    eye1.draw(win)

    # Closed Right eye
    eye2Closed = Line(Point(45, 90), Point(55, 90)) # set endpoints
    eye2Closed.setWidth(3)
    eye2Closed.draw(win)

    # Mouth
    mouth = Oval(Point(30, 105), Point(50, 110)) # set corners of bounding box
    mouth.setFill("red")
    mouth.draw(win)

    label = Text(Point(100, 120), 'A face')
    label.draw(win)

    message = Text(Point(win.getWidth()/2, 20), 'Click anywhere to quit.')
    message.draw(win)
    win.getMouse()
    
    # Open Right eye
    eye2Open = Circle(Point(50, 90), 5)
    eye2Open.setFill('blue')
    eye2Open.draw(win)
    
    win.getMouse()

    for x in range(400):
        for y in range(400):
            win.plotPixel(x,y)

    win.getMouse()
	
    win.close()

main()
