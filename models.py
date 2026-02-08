from database import db

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    section = db.Column(db.String(50), nullable=False)  
    # programs, events, research_publications etc

    title = db.Column(db.String(200))
    desc = db.Column(db.Text)

    img = db.Column(db.String(500))

    date = db.Column(db.String(50))
    location = db.Column(db.String(100))

    author = db.Column(db.String(150))
    year = db.Column(db.String(10))

    position = db.Column(db.Integer, default=0)
