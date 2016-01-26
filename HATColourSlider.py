try:
    from Tkinter import * #Python2
except ImportError:
    from tkinter import * # Python3
import threading, time,os, sys

HAT = None
if os.path.isfile("/proc/device-tree/hat/product"):
    file = open("/proc/device-tree/hat/product","r")
    hat = file.readline()
    if  hat == "Sense HAT\x00":
        print('Sense HAT detected')
        mypath = os.path.dirname(os.path.abspath(__file__))
        file.close()
        from sense_hat import SenseHat
        HAT = 'SH'
    elif hat == "Unicorn HAT\x00":
        print('Unicorn HAT detected')
        mypath = os.path.dirname(os.path.abspath(__file__))
        file.close()
        import unicornhat as uh
        HAT = 'UH'
    else:
        print("Unknown HAT : " + str(hat))
        file.close()
        sys.exit()
else:
    print('No HAT detected')
    sys.exit()


def SH_show_colour(): # Thread to update colour on LED matrix
    sh = SenseHat()
    global running
    while running:
        red_val =red_var.get()
        green_val =green_var.get()
        blue_val =blue_var.get()
        time.sleep(0.05)
        sh.clear(red_val,green_val,blue_val)
    sh.clear([0,0,0])

def UH_show_colour(): # Thread to update colour on LED matrix
    global running
    while running:
        red_val =red_var.get()
        green_val =green_var.get()
        blue_val =blue_var.get()
        time.sleep(0.05)
        for y in range(8):
            for x in range(8):
                uh.set_pixel(x,y,red_val,green_val,blue_val)
        uh.show()
    sh.off()

def on_close(): # Graceful shutdown
    global running
    running=False
    root.destroy()

root = Tk()
root.protocol("WM_DELETE_WINDOW", on_close)
if HAT == 'SH':
    root.title("SenseHAT colour mixer")
elif HAT = 'UH':
    root.title("UnicornHAT colour mixer")
red_var = IntVar()
green_var = IntVar()
blue_var = IntVar()
red = Scale( root, variable = red_var, from_=0, to=255, orient=HORIZONTAL,length=300, label="Red", bg="red",fg="white",troughcolor="#ff6f00")
red.pack(anchor=CENTER)
blue = Scale( root, variable = blue_var, from_=0, to=255, orient=HORIZONTAL,length=300,label="Blue", bg="blue", fg="white", troughcolor="#00a9ff" )
blue.pack(anchor=CENTER)
green = Scale( root, variable = green_var, from_=0, to=255, orient=HORIZONTAL,length=300 ,label="Green", bg="green",fg="white", troughcolor="#5eff00")
green.pack(anchor=CENTER)
running = True
if HAT == 'SH':
    t1 = threading.Thread(target=SH_show_colour)
elif HAT == 'UH':
    t1 = threading.Thread(target=UH_show_colour)
t1.start()

root.mainloop()
