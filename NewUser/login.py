import bcrypt


# Entering Userdata
def enter_data():
    print('Enter E-Mail:')
    e_mail = input()
    print('Enter Password:')
    password = input()
    return encryption(e_mail, password)


def encryption(e_mail, password):
    # turn password to bytes
    password_as_bytes = password.encode()

    # generate salt
    salt = bcrypt.gensalt()

    # hash password with salt using bcrypt
    hashed = bcrypt.hashpw(password_as_bytes, salt)
    return send_to_data_bank(e_mail, salt, hashed)


def send_to_data_bank(e_mail, salt, hashed):
    # userID for new user
    user_data_bank = open(r'C:\Users\HuyNG\PycharmProjects\Webapp\NewUser\USERDATA.txt')
    user_data_as_list = user_data_bank.readlines()
    user_id = int(user_data_as_list[0]) + 1
    user_data_as_list[0] = str(user_id) + '\n'
    user_data_bank.close()

    user_data_as_str = ''.join(user_data_as_list)

    user_data_bank = open(r'C:\Users\HuyNG\PycharmProjects\Webapp\NewUser\USERDATA.txt', 'w')
    user_data_bank.write(user_data_as_str)
    user_data_bank.close()

    # compute distances for txt file
    user_id_dst = 8 - len(str(user_id))
    e_mail_dst = 37 - len(e_mail)

    # update databank
    user_data_bank = open(r'C:\Users\HuyNG\PycharmProjects\Webapp\NewUser\USERDATA.txt', 'a')
    user_data_bank.write(
        '\n' + str(user_id) + ' ' * user_id_dst + e_mail + ' ' * e_mail_dst + str(
            salt) + '  ' + str(hashed))
    user_data_bank.close()


enter_data()
