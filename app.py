from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy() # db intitialized here
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable = False)
    
    def __repr__(self):
        return '<Movie %r>' % self.id
    
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
        movie_content = request.form['content']
        new_movie = Todo(content=movie_content)

        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your movie'
    else:
        movies = Todo.query 
        return render_template('index.html', movies = movies)
    
@app.route('/delete/<int:id>')
def delete(id):
        movie_to_delete = Todo.query.get_or_404(id) #Attempts to get task by ID, if it doesn't work it will 404

        try:
            db.session.delete(movie_to_delete)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error :("
        
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    movie = Todo.query.get_or_404(id)

    if request.method == 'POST':
        movie.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating task'
    else:
        return render_template('update.html', movie = movie)
    

if __name__ == "__main__":
    app.run(debug = True)