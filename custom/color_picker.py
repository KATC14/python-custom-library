import tkinter
from tkinter.ttk import *

from custom import color_tools

class pick(tkinter.Frame):
	def __init__(self, parent, **kw):
		super().__init__(parent, **kw)

		self.var_0 = tkinter.IntVar(value='#000000')
		self.var_1 = tkinter.IntVar(value='0, 0, 0')
		self.colorlabel = Label(self, text="               ", background="#000000", foreground=color_tools.TCC("#000000"))
		self.hex_r = Label(self, text="00")
		self.hex_g = Label(self, text="00")
		self.hex_b = Label(self, text="00")
		self.scale = tkinter.Scale(self, orient='horizontal', length=250, from_=0, to=255, command=self.sacale)
		self.scale1 = tkinter.Scale(self, orient='horizontal', length=250, from_=0, to=255, command=self.sacale)
		self.scale2 = tkinter.Scale(self, orient='horizontal', length=250, from_=0, to=255, command=self.sacale)
		# hex
		hexxl = Label(self, text="hex")
		hexx = Entry(self, width=40, textvariable=self.var_0, validate='key', validatecommand=(self.register(lambda *args: False), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
		# rgb
		rgbl = Label(self, text="rgb")
		rgb = Entry(self, width=40, textvariable=self.var_1, validate='key', validatecommand=(self.register(lambda *args: False), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))

		self.colorlabel.grid(column=1, row=1)
		self.hex_r.grid(column=0, row=2)
		self.scale.grid(column=1, row=2, columnspan=2)
		self.hex_g.grid(column=0, row=3)
		self.scale1.grid(column=1, row=3, columnspan=2)
		self.hex_b.grid(column=0, row=4)
		self.scale2.grid(column=1, row=4, columnspan=2)

		hexxl.grid(column=0, row=5)
		hexx.grid( column=1, row=5)
		rgbl.grid( column=0, row=6)
		rgb.grid(  column=1, row=6)

	def return_color(self):
		return self.hexx.get()

	def sacale(self, event):
		r = self.scale.get()
		g = self.scale1.get()
		b = self.scale2.get()
		hexclr = color_tools.rgb2hex((r, g, b))
		self.colorlabel.config(background=hexclr)#, text=hex, foreground=TCC(hex)
		#self.config(background=f'#{h}{e}{x}')
		self.hex_r.config(text=hexclr[1:3])
		self.hex_g.config(text=hexclr[3:5])
		self.hex_b.config(text=hexclr[5:7])

		self.var_0.set(hexclr)
		self.var_1.set(f'{r}, {g}, {b}')

if __name__ == "__main__":
    root = tkinter.Tk()
    pick(root).grid(sticky='NW', column=0, row=0)
    root.mainloop()
