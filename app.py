from flask import Flask, render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)

#tell your app about the location of your database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#initialize your database

db=SQLAlchemy(app)
#class to create tables in your database

class ToDo(db.Model):
   id=db.Column(db.Integer,primary_key=True)
   content=db.Column(db.String(200),nullable=False)
   datecreated=db.Column(db.DateTime,default=datetime.utcnow)

   def __repr__(self):
       return '<Task %r'%self.id

@app.route('/',methods=['GET','POST'])
def index():
   if request.method=="POST":
      #return "HEllo"
      #get data from the form
      task_content = request.form['content']
      #create new row in table--> create object of class
      new_task=ToDo(content=task_content)
      try:
         db.session.add(new_task)
         db.session.commit()
         return redirect('/')
      except:
         return "ERROR OCCURRED"
   else:
      tasks = ToDo.query.order_by(ToDo.datecreated).all()
      return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
   task_delete=ToDo.query.get_or_404(id)
   try:
      db.session.delete(task_delete)
      db.session.commit()
      return redirect('/')
   except:
      return "Error Occured in delete, Try again!!"

@app.route('/update/<int:id>',methods=["GET","POST"])
def update(id):
   task=ToDo.query.get_or_404(id)
   if request.method=="POST":
      task.content=request.form['content']
      try:
         db.session.commit()
         return redirect('/')
      except:
         return "Error Occured in Update, Try again!!"
   else:
      return render_template('update.html',task=task)


if __name__=="__main__":
   app.run(debug=True)