import os
import sys
import string
import datetime

g_map_type = {
   'VARCHAR2':'SqliteData::DataType::String',
   'NVARCHAR2':'SqliteData::DataType::String',
   'NUMBER':'SqliteData::DataType::Int',
   'DATE':'SqliteData::DataType::TimeStamp',
   'BLOB':'SqliteData::DataType::ByteArray',
}

g_map_type_func = {
   'VARCHAR2':'toString',
   'NVARCHAR2':'toString',
   'NUMBER':'toInt',
   'DATE':'toString',
   'BLOB':'toString',
}

g_map_nullable = {
    'Y':'true',
    'N':'false',
}

g_map_iskey = {
    True:'true',
    False:'false',
}

table_name = 'CACHE_TEST_T'
tableField = []
    
class Field(object):
    def __init__(self, name, type, len, nullable, comments, iskey):
        self.name = name
        self.type = type
        self.len = len
        self.nullable = nullable
        self.comments = comments
        self.iskey = iskey

def gencomm(filename):
#    if os.path.isfile(filename):
#        print '%s already exist!' % filename
#        os.remove(filename)
#        print '%s removed!' % filename 
    file = open(filename, 'w')
    today = datetime.date.today()
    date = today.strftime('%Y')+'-'+today.strftime('%m')+'-'+today.strftime('%d')
    filetypes = string.split(filename,'.')
    length = len(filetypes)
    filetype = filetypes[length-1]
     
    if filetype == 'c' or filetype == 'cpp' or filetype == 'h':
        file.writelines('/**')
        file.write('\n')
        file.writelines('* @File: '+ filename)
        file.write('\n')
        file.write('* @Date: '+date)
        file.write('\n')
        file.write('* @author: ')
        file.write('\n')
        file.write('*/\n')
    else:
        print 'just create %s' % filename
    file.close()