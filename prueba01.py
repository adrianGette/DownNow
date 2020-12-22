# /usr/bin/env python
# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import pafy
import threading
from PIL import ImageTk, Image
import tkinter.font as tkFont
 
ventana=Tk()
ventana.geometry("700x650")
#ventana.configure(background="black")
ventana.title("Down Now - video downloader")
ventana.iconphoto(False, PhotoImage(file='IMAGEN DOWNLOAD.png'))
ventana.resizable(width=False, height=False)
URLL=StringVar()
directorio_actual=StringVar()
total_size=0
dif=0
img = ImageTk.PhotoImage(Image.open("LOGO DOWN NOW.png"))
small_font = ('Verdana',15)



def dire_actu():
    directorio_actual.set(os.getcwd())
 
def direc():
    directorio=filedialog.askdirectory()
    if directorio!="":
        os.chdir(directorio)
        directorio_actual.set(os.getcwd())
 
def verif_url():
    try:
        v = pafy.new(URLL.get())
        print(v.title)
        return v
    except:
        messagebox.showwarning("Error", "Ingresar link nuevamente")
        entrada.delete(0,len(URLL.get()))
 
def get(c,v):
    global total_size
    if c == "vid":
        try:
            s = v.getbest(preftype="mp4")
        except:
            s = v.getbest()
    else:
        try:
            s = v.getbestaudio(preftype="m4a")
        except:
            s = v.getbestaudio()
    total_size=s.get_filesize()
    return s
 
def estado(s):
    boton_dire.config(state = s)
    boton_descarga.config(state = s)
    boton_audio.config(state = s)
 
def mycb(total,recvd,ratio,rate,eta):
    global dif
    porcen=(recvd*100/total_size)
    eti_porcent.config(text=((int(porcen),"%")))
    prog.step(porcen-dif)
    dif=porcen
 
def descargando(co,vid):
    global dif
    so = get(co,vid)
    try:
        so.download(quiet=True,callback=mycb)
        messagebox.showinfo("Fin de descarga","Descarga finalizada con éxito")
    except:
        messagebox.showwarning("Error","Se ha producido un error en la descarga")
        prog.step(100)
        entrada.delete(0,len(URLL.get()))
    estado('normal')
    eti.place(x=150,y=380)
    eti_porcent.config(text=" ")
    dif=0
    total_size=0
 
def descarga(co):
    vid = verif_url()
    if vid!=None:
        eti.place(x=150,y=380)
        estado('disabled')
        t1 = threading.Thread(target = descargando , args = (co,vid) )
        t1.start()

def center(toplevel): 
    toplevel.update_idletasks() 
    w = toplevel.winfo_screenwidth() 
    h = toplevel.winfo_screenheight() 
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x')) 
    x = w/2 - size[0]/2 
    y = h/2 - size[1]/2 
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y))) 
 
dire_actu() #LLAMADA A PRIMERA FUNCIÓN A EJECUTAR.
 

panel = Label(ventana, image = img)
panel.place(x=150, y=0, width=400, height=350)

Label(ventana,text="URL Youtube",bg="black",
        fg="white").place(x = 150, y = 330,
        width=100, height=40)

entrada=Entry(ventana,font=small_font,
            textvariable=URLL)

entrada.place(x = 250, y = 330, width=300, height=40)

eti=Label(ventana,text="Progreso",bg="black", fg="white")
eti.place(x = 150, y = 380, width=80, height=40)

eti_porcent=Label(ventana,bg="black", fg="white")
eti_porcent.place(x = 230, y = 380, width=40, height=40)

prog=progressbar = ttk.Progressbar(ventana)
prog.place(x = 270, y = 380, width=280, height=40)




boton_descarga=Button(ventana,text="Descargar video",
                    bg="#7B047D", fg="white",
                    command=lambda:descarga("vid"))

boton_descarga.place(x = 190, y = 450, width=150, height=40)

boton_audio=Button(ventana,text="Descargar audio",bg="#7B047D",
                 fg="white",command=lambda:descarga("aud"))

boton_audio.place(x = 360, y = 450, width=150, height=40)



entrada2=Entry(ventana,font=('Arial',8),textvariable=directorio_actual)
entrada2.place(x = 250, y = 590, width=200, height=40)

Label(ventana,text="Destino",bg="black", fg="white").place(x=150,
         y=590, width=100, height=40)


boton_dire=Button(ventana,text="Cambiar directorio",bg="#7B047D",
                 fg="white",command=direc)

boton_dire.place(x = 450, y = 590, width=150, height=40)



center(ventana)
 
ventana.mainloop()