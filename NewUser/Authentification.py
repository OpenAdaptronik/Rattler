import bcrypt
import MySQLdb

db = MySQLdb.connect(host='localhost', user='root',
                     passwd='Rattlers17', db='test')
c = db.cursor()


# Entering Userdata
def enter_data():

    print('Enter Username:')
    username = input()
    print('Enter E-Mail:')
    e_mail = input()
    print('Enter Password:')
    inpassword = input()
    return get_from_data_bank(username, e_mail, inpassword)


def get_from_data_bank(username, e_mail, inpassword):
    get = ('''SELECT Password FROM user 
                   WHERE (Username = %s  AND Email = %s)''')
    c.execute(get, (username, e_mail))
    data = c.fetchone()
    hashed = data[0]
    return authentificate(hashed, inpassword)


def authentificate(inpassword, hashed):

    # turn hashed_as_bytes to bytes
    hashed_as_bytes = hashed.encode()

    # turn inpassword to bytes
    inpassword_as_bytes = inpassword.encode()

    if bcrypt.checkpw(hashed_as_bytes, inpassword_as_bytes):
        return print('Access granted.')
    else:
        return print('Access denied.')


enter_data()

c.close()
