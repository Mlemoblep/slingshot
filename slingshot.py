from tkinter import *
import time
import math
class GUI(object):
    def __init__(self):
        self.window = Tk()
        self.window.title('by Koteshov Semen')
        self.slingshot = None
        self.center = None
        self.height = 0
        self.usl=True
        self.trajectoryballs=[]
        self.canvas = Canvas(self.window,width=720, height=720)
        self.window.resizable(720, 720)
        self.create_ball(200, 720)
        self.createslingshot(0)
        self.startposition=[200,720]
        self.flighttime()
        self.canvas.place(x=0, y=0)
        self.canvas.bind('<B1-Motion>', self.stretching)
        self.canvas.bind('<ButtonRelease-1>', self.ballmove)
        self.whatheight()
        self.window.geometry('720x720+0+0')
        self.whatg()
        self.g = 10
        self.window.mainloop()
        
    def create_ball(self, coord_x, coord_y):
        self.ball = self.canvas.create_oval(coord_x, coord_y-50, coord_x + 50, coord_y,
                                          fill="red")
        self.speedy=self.canvas.create_text(coord_x+25, coord_y-60,text=str(0),fill="black")
        self.speedx=self.canvas.create_text(coord_x+60, coord_y-25,text=str(0),fill="black")
        self.canvas.update()
        if self.usl:
            self.slingshotline = self.canvas.create_line(225, 720 - int(self.height), coord_x + 25, coord_y, fill="black")

    def ballmove(self, event):
        print("Начальная скорость шара равна:", self.v0)
        if self.usl:
            steps=[]
            t=0
            self.usl=False
            for i in range(len(self.trajectoryballs)):
                self.canvas.delete(self.trajectoryballs[i])
            self.trajectoryballs=[]
            while self.canvas.coords(self.ball)[1]+25<720:
                t=t+0.01
                steps.append([self.whatx(t),self.whaty(t)])
                self.canvas.coords(self.ball,steps[-1][0]+200,720-steps[-1][1]-int(self.height),steps[-1][0]+250,720-steps[-1][1]-int(self.height)-50)
                self.canvas.coords(self.speedy, steps[-1][0]+200+25,720-steps[-1][1]-int(self.height)-60)
                self.canvas.coords(self.speedx, steps[-1][0]+200+70,720-steps[-1][1]-int(self.height)-25)
                if self.alpha>0 and self.alpha<181:
                    self.canvas.itemconfigure(self.speedy,text=str(round(abs(self.v0)*abs(self.sina)*(-1)-(self.g*t**2)/2,3)))
                else:
                    self.canvas.itemconfigure(self.speedy,text=str(round(abs(self.v0)*abs(self.sina)-(self.g*t**2)/2,3)))
                if self.alpha>90 or self.alpha>-90 and self.alpha<0:
                    self.canvas.itemconfigure(self.speedx,text=str(round(self.v0*abs(self.cosa),3)))
                else:
                    self.canvas.itemconfigure(self.speedx,text=str(round(self.v0*abs(self.cosa)*(-1),3)))
                self.window.update()
                time.sleep(0.001)
            if self.alpha>0 and self.alpha<181:
                self.flighttime1=(self.v0*abs(self.sina)*(-1)+math.sqrt((self.v0*abs(self.sina)*(-1))**2+2*self.g*int(self.height))/self.g)
            else:
                self.flighttime1=(self.v0*abs(self.sina)+math.sqrt((self.v0*abs(self.sina))**2+2*self.g*int(self.height))/self.g)
            self.flighttime1=round(self.flighttime1,3)
            self.labelflighttime.config(text="Время \nпоследнего\n полета: " + str(self.flighttime1))
            self.canvas.itemconfigure(self.speedy,text=str(0))
            self.canvas.itemconfigure(self.speedx,text=str(0))
            
            self.usl=True
    def flighttime(self):
        self.labelflighttime=Label(self.canvas,background="red",text="Время \nпоследнего\n полета: 0",width=14,height=6)
        self.labelflighttime.place(x=620,y=360)

    def trajectory(self):
        if self.usl:
            steps=[]
            t=0
            steps.append([self.whatx(t),self.whaty(t)])
            self.trajectoryballs.append(self.canvas.create_oval(steps[-1][0]+200,720-steps[-1][1]-int(self.height),steps[-1][0]+250,720-steps[-1][1]-int(self.height)-50,fill="green"))
            self.window.update()
            while self.canvas.coords(self.trajectoryballs[-1])[1]+25<720:
                t=t+2
                steps.append([self.whatx(t),self.whaty(t)])
                self.trajectoryballs.append(self.canvas.create_oval(steps[-1][0]+200,720-steps[-1][1]-int(self.height),steps[-1][0]+250,720-steps[-1][1]-int(self.height)-50,fill="green"))
                self.window.update()
                if self.canvas.coords(self.trajectoryballs[-1])[1]+25>720:
                    break
    
    def stretching(self, event):
        if self.usl:
            for i in range(len(self.trajectoryballs)):
                self.canvas.delete(self.trajectoryballs[i])
            self.trajectoryballs=[]
            if event.x > 0 and event.x < 720 and event.y < 720 and event.y > 0:
                self.canvas.coords(self.ball, event.x - 25, event.y - 25, event.x + 25, event.y + 25)
                self.canvas.coords(self.slingshotline, 225, 720 - int(self.height) - 25, event.x, event.y)
                self.a=((720-event.y)-int(self.height)-25)
                self.b=((event.x-225))
                self.canvas.coords(self.speedy, event.x, event.y-35)
                self.canvas.coords(self.speedx, event.x+35, event.y)
                self.startposition=[event.x,event.y]
                self.c=math.sqrt((self.a**2)+(self.b**2))
                self.sina = self.a/self.c
                self.cosa= self.b/self.c
                self.v0=abs(self.c)*0.4
                self.alpha=math.atan2(self.a,self.b)*180/math.pi
                if self.alpha<0:
                    self.alpha=-(180+self.alpha)
                if self.alpha==0:
                    self.alpha=-180
                if self.usl==True:
                    self.trajectory()
    def createslingshot(self, height):
        if self.slingshot==None:
            self.slingshot = self.canvas.create_rectangle(200, 720, 250, 720 - height - 50)
            self.center = self.canvas.create_oval(225, 720 - height - 25, 225, 720 - height - 25,
                                              fill="black")
        else:
            self.canvas.coords(self.slingshotline, 225, 720 - int(self.height) - 25, 225, 720 - int(self.height) - 25)
            self.canvas.coords(self.slingshot, 200, 720, 250, 720 - height - 50)
            self.canvas.coords(self.center, 225, 720 - height - 25, 225, 720 - height - 25)

    def whatheight(self):
        self.canvasheight = Canvas(self.canvas, width=100, height=120, background="red")
        self.labelheight = Label(self.canvasheight, width=0, height=0, text="Сброс позиции\n(регулирование\n высоты)",background="red")
        self.labelheight.place(x=8, y=8)
        self.scaleheight = Scale(self.canvasheight, to=668, command=self.setheight, from_=0, orient=HORIZONTAL, sliderlength=10, background="red", borderwidth=0)
        self.scaleheight.place(x=0, y=60)
        self.canvasheight.place(x=620, y=600)
        
    def setheight(self, var):
        self.height=var
        self.canvas.coords(self.ball, 200, 720 - int(self.height) - 50, 250, 720 - int(self.height))
        self.createslingshot(int(self.height))
        self.canvas.coords(self.speedy, 225, 720 - int(self.height) - 60)
        self.canvas.coords(self.speedx, 260, 720 - int(self.height) - 25)

    def whatg(self):
        self.canvasg = Canvas(self.canvas, width=100, height=120, background="red")
        self.labelheight = Label(self.canvasg, width=0, height=0, text="Ускорение\nсвободного\nпадения",background="red")
        self.labelheight.place(x=18, y=8)
        self.entryg = Entry(self.canvasg, width=14)
        self.entryg.place(x=8, y=60)
        self.buttong = Button(self.canvasg, width=8, height=0, text="Установить", background="red", command=self.setg)
        self.buttong.place(x=20, y=85)
        self.canvasg.place(x=620, y=0)
    def setg(self):
        self.g = self.entryg.get()
        if self.g == "":
            self.g = 10
        else:
            self.g=float(self.g)
    def whatx(self,t):
        if self.alpha>90 or self.alpha>-90 and self.alpha<0:
            return self.v0*t*abs(self.cosa)
        else:
            return self.v0*t*abs(self.cosa)*(-1)
    def whaty(self,t):
        if self.alpha>0 and self.alpha<181:
            return abs(self.v0)*t*abs(self.sina)*(-1)-(self.g*t**2)/2
        else:
            return abs(self.v0)*t*abs(self.sina)-(self.g*t**2)/2
        return abs(self.v0)*t*abs(self.sina)-(self.g*t**2)/2
a=GUI()
