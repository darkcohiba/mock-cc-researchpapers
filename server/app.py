#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Research, Author, ResearchAuthors

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'


@app.get('/research')
def get_research():
    research_list = [r.to_dict() for r in Research.query.all()]

    return make_response(research_list,200)

@app.route('/research/<id>', methods = ["GET","DELETE"])
def research_by_id(id):
    if request.method == "GET":

        research_list = Research.query.filter_by(id = id).first()

        if not research_list:
            return {"error": "Research paper not found"}

        l = research_list.to_dict(rules=('authors',))
        return make_response(jsonify(l), 200)
    
    elif request.method =="DELETE":
        research_list = Research.query.filter_by(id = id).first()

        if not research_list:
            return {"error": "Research paper not found"}

        db.session.delete(research_list)
        db.session.commit()
        return make_response("", 204)
    
@app.get('/authors')
def get_authors():
    author_list = [a.to_dict() for a in Author.query.all()]
    return make_response(author_list, 200)
    
    
@app.post('/authors')
def post_authors():
    form_json = request.get_json()

    new_research = ResearchAuthors(
        author_id = form_json["author_id"],
        research_id = form_json["research_id"]
    )

    research = Research.query.get(form_json['research_id'])
    author = Author.query.get(form_json['author_id'])

    if not research or not author:
        return {"errors": ["validation errors"]}

    db.session.add(new_research)
    db.session.commit()

    return make_response(author.to_dict(), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
