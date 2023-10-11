#!/usr/bin/env python3

from app import app
from models import db, Research, Author, ResearchAuthors



def create_authors():
    re = db.session.query(Research).filter_by(id=3).first()
    author_array =[]
    for author in re.research_author_relationship_field:
            author_block = {
                "id": author.author_relationship_field.id,
                "name": author.author_relationship_field.name,
                "field_of_study": author.author_relationship_field.field_of_study
            }
            print(author_block)
            author_array.append(author_block)
    return author_array


if __name__ == '__main__':
    with app.app_context():
        print(create_authors())


