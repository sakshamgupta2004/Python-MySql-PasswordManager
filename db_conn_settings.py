def getFromFile(tag, defaultVal = None):

    f = open("db.conf")
    lines = f.readlines()
    for l in lines:
        if (l.__contains__("<" + tag + ">") and l.__contains__("</" + tag + ">")):
            return l[l.index("<" + tag + ">") + len(tag) + 2 : l.index("</" + tag + ">")]

    return defaultVal


def getHost():
    tag = "host"
    defVal = "localhost"
    return getFromFile(tag, defaultVal = defVal)

def getPort():
    tag = "port"
    defVal = 3306
    return getFromFile(tag, defaultVal = defVal)

def getUser():
    tag = "user"
    defVal = "root"
    return getFromFile(tag, defaultVal = defVal)

def getPassword():
    tag = "password"
    defVal = "password_here"
    return getFromFile(tag, defaultVal = defVal)