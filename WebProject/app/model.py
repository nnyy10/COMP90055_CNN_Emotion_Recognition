2# from operator import and_
# from app import db
#
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(32), unique=True)
#     username = db.Column(db.String(16), unique=True)
#     password = db.Column(db.String(16))
#
#     def valid_login(self, username, password):
#         user = User.query.filter(and_(self.username == username, self.password == password)).first()
#         if user:
#             return True
#         else:
#             return False
#
# class History(db.Model):
#     __tablename__ = 'histories'
#     id = db.Column(db.Integer, primary_key=True)
#     image_name = db.Column(db.String(50), unique=True)
#     image_location = db.Column(db.String(200), nullable=False)
#     submit_time = db.Column(db.DATETIME, nullable=True)
#     result = db.Column(db.String(100))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))