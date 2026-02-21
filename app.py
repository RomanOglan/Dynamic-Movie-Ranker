from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy() # db intitialized here
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Movie.db"
db.init_app(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable = True)
    
    def __repr__(self):
        return '<Movie %r>' % self.id
    
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        pass
        movie_content = request.form['content'] 
        movie_rating = request.form.get('rating')
        new_movie = Movie(content=movie_content, rating = movie_rating)

        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"ERROR: {e}") 
            return f"The error is: {e}"
    else:
        movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()
        return render_template('index.html', movies = movies)
    
@app.route('/delete/<int:id>')
def delete(id):
    movie_to_delete = db.session.get(Movie, id) 
    
    if movie_to_delete is None:
        return "Movie not found", 404

    try:
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error :("
        
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    movie = db.get_or_404(Movie, id) 

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