import MySQLdb

db = MySQLdb.connect(host='localhost', user='root',
                     passwd='Rattlers17', db='test')

# db.query('''DROP TABLE user;''')

db.query("""CREATE TABLE IF NOT EXISTS user (UserID INT,
                                             Username VARCHAR(100) NOT NULL,
                                             Email VARCHAR(100) NOT NULL,
                                             Password VARCHAR(100) NOT NULL,
                                             Admin INT);""")
