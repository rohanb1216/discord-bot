def botToken():
    f = open("token.txt", 'r')
    token = f.read()
    f.close()
    return token