from config import db

class Friends(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), nullable=False)
    role = db.Column('role', db.String(100), nullable=False)
    description = db.Column('description', db.Text, nullable=False)
    gender = db.Column('gender', db.String(10), nullable=False)
    img_url = db.Column('img_url', db.String(500), nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'description': self.description,
            'gender': self.gender,
            'imgUrl': self.img_url,
        }
    