from Tkinter import *
from random import shuffle
    
class Gui:
  def __init__(self, my_engine, root):
    self.my_engine = my_engine
    
    root.title("Test Training")
    root.bind_all('<Key>', self.keypress)
    
    # create a menu
    menu = Menu(root)
    root.config(menu=menu)
    
    filemenu = Menu(menu)
    filemenu.add_command(label="Salir", command=root.quit)
    menu.add_cascade(label="Archivo", menu=filemenu)
    
    self.createMenu(menu)
    
    # selected option
    self.opt = IntVar()

    # question Frame
    self.fr_que = Frame(root)
  
    self.tit_que = StringVar()
    Label(self.fr_que, textvariable=self.tit_que).grid(row=0, sticky=W)
    self.qa = StringVar()
    self.b = []
    self.b.append(Radiobutton(self.fr_que, textvariable=self.qa, 
      variable=self.opt, command=self.questionCallback, value=0))
    self.b[0].grid(row=1, sticky=W)
    self.qb = StringVar()
    self.b.append(Radiobutton(self.fr_que, textvariable=self.qb, 
      variable=self.opt, command=self.questionCallback, value=1))
    self.b[1].grid(row=2, sticky=W)
    self.qc = StringVar()
    self.b.append(Radiobutton(self.fr_que, textvariable=self.qc, 
      variable=self.opt, command=self.questionCallback, value=2))
    self.b[2].grid(row=3, sticky=W)
    self.qd = StringVar()
    self.b.append(Radiobutton(self.fr_que, textvariable=self.qd, 
      variable=self.opt, command=self.questionCallback, value=3))
    self.b[3].grid(row=4, sticky=W)
    
    # repeat wrong Frame
    self.fr_wrong = Frame(root)
    Label(self.fr_wrong, text="Quieres repetir las preguntas falladas?").pack()
    Button(self.fr_wrong, text="OK", command=self.my_engine.doWrong).pack()
    
    # status bar  
    self.str_statusbar = StringVar()
    status = Label(root, textvariable=self.str_statusbar, bd=1, relief=SUNKEN, anchor=E)
    status.pack(side=BOTTOM, fill=X)
    
    # randomly located questions
    self.seq = [0,1,2,3]

  def keypress(self, event):
    x = event.char
    if x != '' and x.upper() in "ABCD":
      self.opt.set("ABCD".index(x.upper()))
      self.questionCallback()
  
  def setStatusBar(self, text):
    self.str_statusbar.set(text)
  
  def hideFrames(self):
    self.fr_wrong.pack_forget()
    self.fr_que.pack_forget()
    
  def createMenu(self, menu):
    option_menu = Menu(menu)
    option_menu.add_command(label="Preguntas Aleatorias", command=self.my_engine.doRandom)
    option_menu.add_command(label="Peor Calificacion", command=self.my_engine.doWorstRated)
    menu.add_cascade(label="Menu", menu=option_menu)

    # Exam subMenu
    sub_menu = Menu(menu)
    items = self.my_engine.my_db.getExams()
    for i in range(len(items)):
      def item_command(name):
        def new_command():
          self.my_engine.doExam(name)
        return new_command
      f = item_command(items[i][0])
      sub_menu.add_command(label=items[i][1], command= f)
    option_menu.add_cascade(label="Hacer Examen", menu=sub_menu)

    # Type subMenu
    type_menu = Menu(menu)
    items = self.my_engine.my_db.getTypes()
    for i in range(len(items)):
      def item_command(name):
        def new_command():
          self.my_engine.doType(name)
        return new_command
      f = item_command(items[i][0])
      type_menu.add_command(label=items[i][1], command= f)
    option_menu.add_cascade(label="Hacer Tipo", menu=type_menu)
    
  def setQuestion(self, question):
    self.opt.set(-1)
    self.hideFrames()
    self.fr_que.pack(side=TOP, fill=BOTH, padx=5, pady=5)
    self.clearButtonColor()
    
    self.tit_que.set(str(question[0]) + " - " + question[1])
    
    shuffle(self.seq)
    self.qa.set("A) " + question[2 + self.seq[0]])
    self.qb.set("B) " + question[2 + self.seq[1]])
    self.qc.set("C) " + question[2 + self.seq[2]])
    self.qd.set("D) " + question[2 + self.seq[3]])
  
  def clearButtonColor(self):
    for button in self.b:
      button.configure(bg='#d9d9d9')
    
  def questionCallback(self):
    self.b[self.opt.get()].configure(bg='red')
    self.my_engine.questionCallback(self.seq[self.opt.get()])
    
  def launchPopup(self, callback):
    self.hideFrames()
    self.fr_wrong.pack(side=TOP, fill=BOTH, padx=5, pady=5)

