import bcrypt
import MySQLdb
from NewUser import userIDCreator

db = MySQLdb.connect(host='localhost', user='root',
                     passwd='Rattlers17', db='test')
c = db.cursor()


used_ids = []
deleted_ids = []


# Entering Userdata
def enter_data():

    print('Enter Username:')
    username = input()
    print('Enter E-Mail:')
    e_mail = input()
    print('Enter Password:')
    password = input()
    return encryption(username, e_mail, password)


def encryption(username, e_mail, password):
    # turn password to bytes
    password_as_bytes = password.encode()

    # generate salt
    salt = bcrypt.gensalt()

    # hash password with salt using bcrypt
    hashed = bcrypt.hashpw(password_as_bytes, salt)
    return send_to_data_bank(username, e_mail, hashed)


def send_to_data_bank(username, e_mail, hashed):
    # userID for new user
    new_id = userIDCreator.id_for_new_user(0, used_ids, deleted_ids)
    strhashed = str(hashed)
    print(str(new_id) + ' ' + username + ' ' + e_mail + ' ' + strhashed + ' ' + '0')
    insert = ('''INSERT INTO user (UserID, Username, Email, Password, Admin)
                   VALUES (%s, %s, %s, %s, %s)''')
    c.execute(insert, (new_id, username, e_mail, hashed, 0))
    db.commit()


enter_data()

c.close()
