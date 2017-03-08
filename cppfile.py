from comm import *

def gencppfile(filename, headfile):
    gencomm(filename)
    file = open(filename,'a+')
    includefile = '''#include "''' + headfile + '"'
    file.write(includefile)
    file.close() 