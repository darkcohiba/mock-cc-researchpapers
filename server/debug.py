#!/usr/bin/env python3

from app import app
from models import db, Research, Author, ResearchAuthors



def create_authors():
    id = 3
    re = db.session.query(Research).filter_by(id=id).first()
    for auth in re.authors:
        print(auth)
    # author_array = []
    # for author in re.authors:
    #     for box in author.author_research_relationship_field:
    #         if box.research_id == id:
    #             author_block = {
    #                 "id": author.id,
    #                 "name": author.name,
    #                 "field_of_study": author.field_of_study
    #             }
    #             author_array.append(author_block)
    # return author_array


if __name__ == '__main__':
    with app.app_context():
        print(create_authors())


