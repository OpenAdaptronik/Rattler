import MySQLdb
from django.db import models

db = MySQLdb.connect(host='db', user='root',
                     passwd='123456', db='test')

# db.query('''DROP TABLE user;''')

db.query("""CREATE TABLE IF NOT EXISTS user (UserID INT,
                                             Username VARCHAR(100) NOT NULL,
                                             Email VARCHAR(100) NOT NULL,
                                             Salt VARCHAR(100) NOT NULL,
                                             Password VARCHAR(100) NOT NULL);""")


'''class user(models.Model):
    userID = models.IntegerField()
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    salt = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


    def __init__(self, userID, username, email, salt, password, options=None, bases=None, managers=None):
        self.userID = userID
        self.username = username
        self.email = email
        self.salt = salt
        self.password = password
'''
