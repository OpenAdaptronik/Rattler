import bcrypt
import MySQLdb

db = MySQLdb.connect(host='db', user='root',
                     passwd='123456', db='test')
c = db.cursor()


used_ids = []
deleted_ids = []


# Entering Userdata
def enter_data(username, e_mail, password):
    return encryption(username, e_mail, password)


def encryption(username, e_mail, password):
    # turn password to bytes
    password_as_bytes = password.encode()

    # generate salt
    salt = bcrypt.gensalt()

    # hash password with salt using bcrypt
    hashed = bcrypt.hashpw(password_as_bytes, salt)
    return send_to_data_bank(username, e_mail, salt, hashed)


def send_to_data_bank(username, e_mail, salt, hashed):
    # userID for new user
    new_id = id_for_new_user(0, used_ids, deleted_ids)
    strsalt = str(salt)
    strhashed = str(hashed)
    insert = ('''INSERT INTO user (UserID, Username, Email, Salt, Password)
                   VALUES (%s, %s, %s, %s, %s)''')
    c.execute(insert, (new_id, username, e_mail, salt, hashed))
    db.commit()

def id_for_new_user(new_id, used_ids, deleted_ids):

    if len(used_ids) == 0:
        lnew_id = new_id
        used_ids.append(lnew_id)
        return lnew_id
    elif len(deleted_ids) == 0:
        lnew_id = used_ids[-1] + 1
        used_ids.append(lnew_id)
        return lnew_id
    else:
        lnew_id = deleted_ids[0]
        deleted_ids.remove(lnew_id)
        used_ids.insert(lnew_id, new_id)
        return lnew_id

