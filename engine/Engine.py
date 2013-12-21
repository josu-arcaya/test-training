from Database import Database
from Gui import Gui
from Tkinter import Tk

class Engine:
  def __init__(self):
    self.my_db = Database('ega.db','user.db')
    self.c = {}
    
    root = Tk()
    root.geometry("800x300+100+100")
    
    self.my_gui = Gui(self, root)

    root.mainloop()
    
  def doRandom(self):
    self.i = self.right = self.total = 0 
    self.wrong_questions = []
    self.questions = [x[0] for x in self.my_db.getRandomQuestions()]
    self.nextQuestion()
    
  def doWorstRated(self):
    self.i = self.right = self.total = 0 
    self.wrong_questions = []
    self.questions = [x[0] for x in self.my_db.getWorstRated()]
    self.nextQuestion()    
  
  def doType(self, id_type):
    self.i = self.right = self.total = 0
    self.wrong_questions = []
    self.questions = [x[0] for x in self.my_db.getFullType(id_type)]
    self.nextQuestion()
    
  def doExam(self, id_exam):
    self.i = self.right = self.total = 0
    self.wrong_questions = []
    self.questions = [x[0] for x in self.my_db.getFullExam(id_exam)]
    self.nextQuestion()
    
  def nextQuestion(self):
    if self.i < len(self.questions):
      id_question = self.questions[self.i]
      question = self.my_db.getSingleQuestion(id_question)
      self.c["id_question"] = id_question
      self.c["id_exam"] = question[9]
      self.c["solution"] = question[6]
      self.i += 1
      self.my_gui.setQuestion(question)
    else:
      if self.total == 10:
        self.my_db.insertScore(self.right)
      self.my_gui.launchPopup(self.doWrong)
      
  def doWrong(self):
    self.questions = list(set(self.wrong_questions))
    self.i = self.right = self.total = 0
    self.my_gui.setStatusBar(str(self.right) + " / " + str(self.total))
    self.wrong_questions = []    
    self.nextQuestion()

  def questionCallback(self, sel_option):
    c = self.c
    if not c["id_question"] in self.wrong_questions:
      self.total += 1
      if c["solution"] == sel_option:
        self.right += 1
      else:
        self.wrong_questions.append(c["id_question"])
      self.my_gui.setStatusBar(str(self.right) + " / " + str(self.total))
      self.my_db.updateQuestion(c["id_question"], c["id_exam"], (c["solution"] == sel_option))
    if c["solution"] == sel_option:
      self.nextQuestion()
    
