filename = "/kikupico.log"
errorfilename = "/error.log"

def __str(d):
    return str(d)


def log(*args):
    data = " ".join([__str(arg) for arg in args])
    fd = open(filename, "a")
    fd.write(data)
    print(data)
    fd.write("\n")
    fd.close()

def error(*args):
    data = " ".join([__str(arg) for arg in args])
    fd = open(errorfilename, "a")
    fd.write(str(data))
    print(str(data))
    fd.write("\n")
    fd.close()
