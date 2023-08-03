import tkinter

class Tooltip:#eveh=hover enter event, evex=hover exit event, evem=hover motion event
	def __init__(self, parent, text='text', bg='gray94', fg='black', cursor='arrow', relief='groove', borderwidth=2, textvar=False, move_with_cursor=False, eveh=False, evex=False, evem=False):
		self.parent = parent
		self.text = text
		self.bg = bg
		self.fg = fg
		self.cursor = cursor
		self.relief = relief# flat, groove, raised, ridge, solid, or sunken
		self.borderwidth = borderwidth
		self.strVar = textvar
		if self.strVar is True:
			self.strVar = tkinter.StringVar()
		self.parent.bind("<Enter>", lambda event: self.Hover(event) if not eveh else eveh(event))
		self.parent.bind("<Leave>", lambda event: self.Hover(event) if not evex else evex(event))
		if move_with_cursor:
			self.parent.bind("<Motion>", lambda event: self.motion(event) if not evem else evem(event))

	def Hover(self, event):
		evetype = int(event.type)
		if evetype == 7:
			self.Hovertoplevel = tkinter.Toplevel(self.parent)
			self.Hovertoplevel.overrideredirect(True)
			self.Hovertoplevel.geometry(f"+{event.x_root}+{event.y_root+20}")
			self.parent.config(cursor=self.cursor)
			if self.strVar:
				tkinter.Label(self.Hovertoplevel, text=self.text, bg=self.bg, fg=self.fg, relief=self.relief, borderwidth=self.borderwidth, textvariable=self.strVar).grid(column=0, row=0)
			else: 
				tkinter.Label(self.Hovertoplevel, text=self.text, bg=self.bg, fg=self.fg, relief=self.relief, borderwidth=self.borderwidth).grid(column=0, row=0)
		if evetype == 8:
			self.Hovertoplevel.destroy()

	def motion(self, event):
		self.Hovertoplevel.geometry(f"+{event.x_root}+{event.y_root+20}")

if __name__ == "__main__":
	root = tkinter.Tk()
	lbl = tkinter.Label(root, text='hover over me!')
	lbl.grid(column=0, row=0)
	msg = "cool right?\n at least I think so!"
	Tooltip(lbl, text=msg, bg='green', fg='purple', cursor="hand2", relief='sunken', borderwidth=10, move_with_cursor=True)
	#methods
	#test.text = "new words though \"text\""
	#test.strVar.set("new text though \"StringVar\"\n benefit to this is it updates live rather then needing to be destroyed and remade but it really doesn't\n matter unless you remove the \"Leave\" event but that kind of defeats the purpose of this library") #only works if textvar=True
	root.mainloop()
