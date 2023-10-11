from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Research(db.Model, SerializerMixin):
    __tablename__ = "research_table"
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer)
    page_count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    research_author_relationship_field = db.relationship("ResearchAuthors", back_populates="research_relationship_field", cascade = 'all, delete')

    authors = association_proxy('research_author_relationship_field', 'author_relationship_field')
    def author_array(self):
        re = db.session.query(Research).filter_by(id=self.id).first()
        author_array = []
        for author in re.authors:
            for box in author.author_research_relationship_field:
                if box.research_id == self.id:
                    author_block = {
                        "id": author.id,
                        "name": author.name,
                        "field_of_study": author.field_of_study
                    }
                    print(author_block)
                    author_array.append(author_block)
        return author_array
    @validates('year')
    def validate_year(self, key, year):
        if len(str(year)) != 4:
            raise ValueError("Year must be four digits")
        return year
    serialize_rules=('-research_author_relationship_field','-created_at','-updated_at')

    
    

class Author(db.Model, SerializerMixin):
    __tablename__ = "author_table"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    author_research_relationship_field = db.relationship("ResearchAuthors", back_populates="author_relationship_field", cascade = 'all, delete')

    
    @validates("field_of_study")
    def validate_field(self, key, field_of_study):
        fields = ["AI", "Robotics", "Machine Learning", "Vision", "Cybersecurity"]
        if field_of_study not in fields:
            raise ValueError("Field of study must be in the list of fields")
        return field_of_study
    

class ResearchAuthors(db.Model, SerializerMixin):
    __tablename__ = "research_authors"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("author_table.id"))
    research_id = db.Column(db.Integer, db.ForeignKey("research_table.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    research_relationship_field = db.relationship("Research", back_populates="research_author_relationship_field", cascade = 'all, delete')
    author_relationship_field = db.relationship("Author", back_populates="author_research_relationship_field", cascade = 'all, delete')

    serialize_rules = ('-research_relationship_field','-author_relationship_field')
