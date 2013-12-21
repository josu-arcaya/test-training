import sqlite3

class Database:
  def __init__(self, db_name, db_user):
    self.db_name = db_name
    self.db_user = db_user

  def getExams(self):
    connection = sqlite3.connect(self.db_name)
    cursor = connection.cursor()
    
    cursor.execute("SELECT id_exam,exam FROM exams")
    results = list(cursor)
        
    cursor.close()
    connection.close()    

    return results
  
  def getTypes(self):
    connection = sqlite3.connect(self.db_name)
    cursor = connection.cursor()
    
    cursor.execute("SELECT id_type,type FROM types")
    results = list(cursor)
        
    cursor.close()
    connection.close()    

    return results

  def getSingleQuestion(self, id_question):
    connection = sqlite3.connect(self.db_name)
    cursor = connection.cursor()
    
    t = (id_question, )
    cursor.execute("SELECT * FROM questions WHERE id_question=?", t)
    result = list(cursor)[0]
    
    cursor.close()
    connection.close()
    
    return result
      
  def getFullExam(self, id_exam):
    connection = sqlite3.connect(self.db_name)
    cursor = connection.cursor()
    
    t = (id_exam, )
    cursor.execute("SELECT id_question FROM questions WHERE id_exam=?", t)
    results = list(cursor)
    
    cursor.close()
    connection.close()
    
    return results

  def getFullType(self, id_type):
    connection = sqlite3.connect(self.db_name)
    cursor = connection.cursor()
    
    t = (id_type, )
    cursor.execute("SELECT id_question FROM questions WHERE id_type=? ORDER BY RANDOM()", t)
    results = list(cursor)
    
    cursor.close()
    connection.close()
    
    return results
      
  def getRandomQuestions(self):
    connection = sqlite3.connect(self.db_name)
    cursor = connection.cursor()
    
    cursor.execute("SELECT id_question FROM questions ORDER BY RANDOM() LIMIT 10")
    result = list(cursor)
    
    cursor.close()
    connection.close()
    
    return result

  def getWorstRated(self):
    connection = sqlite3.connect(self.db_user)
    cursor = connection.cursor()
    
    cursor.execute("SELECT id_question FROM register ORDER BY correct*1.0/total ASC, total DESC LIMIT 10")
    result = list(cursor)
    
    cursor.close()
    connection.close()
    
    return result
        
  def updateQuestion(self, id_question, id_exam, correct):
    connection = sqlite3.connect(self.db_user)
    cursor = connection.cursor()

    t = (id_question,)
    cursor.execute("SELECT * FROM register WHERE id_question=?", t)
    row=cursor.fetchone()
    if row is None:
      t = (id_question, id_exam, 1, correct,)
    else:
      row = list(row)
      row[2] += 1
      row[3] += correct
      t = tuple(row)

    cursor.execute("INSERT OR REPLACE INTO register (id_question, id_exam, total, correct) values (?,?,?,?)", t)
    connection.commit()

    cursor.close()
    connection.close()
    
  def insertScore(self, score):
    connection = sqlite3.connect(self.db_user)
    cursor = connection.cursor()
    
    t = (score, )
    cursor.execute("INSERT INTO history(score) VALUES (?)", t)
    connection.commit()
    
    cursor.close()
    connection.close()
