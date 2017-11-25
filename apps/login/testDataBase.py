import MySQLdb

db = MySQLdb.connect(host='db', user='root',
                     passwd='123456', db='test')

# db.query('''DROP TABLE user;''')

db.query("""CREATE TABLE IF NOT EXISTS user (UserID INT,
                                             Username VARCHAR(100) NOT NULL,
                                             Email VARCHAR(100) NOT NULL,
                                             Salt VARCHAR(100) NOT NULL,
                                             Password VARCHAR(100) NOT NULL);""")
