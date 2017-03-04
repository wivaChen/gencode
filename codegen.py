#--*-- coding:utf8 --*--
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
 
class Field(object):
    def __init__(self, name, type, len, nullable, comments='', iskey=False):
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
    file = open(filename,'w')
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

def genheadfile(filename):
    gencomm(filename)
    file = open(filename,'a+')
    headmacro = '__' + filename.split('.')[0].upper() + '_H__'
    file.writelines('#ifndef ' + headmacro)
    file.write('\n')
    file.writelines('#define ' + headmacro)
    file.write('\n\n\n')
    file.write('struct ' + structname)
    file.write('\n{\n')
    for i in range(len(tableField)):
        fieldsplit = tableField[i].name.lower().split('_')
        fieldname = ''
        for j in range(len(fieldsplit)):
            fieldname += fieldsplit[j].capitalize()   
        if tableField[i].type == 'NUMBER':
            if tableField[i].len <= 9:
                file.write('    int32_t n' + fieldname + ';')
            else:
                file.write('    int64_t l' + fieldname + ';')
        elif tableField[i].type == 'VARCHAR2':
            file.write('    char sz' + fieldname + '[' + str(tableField[i].len) + '];')
        else:
            print 'unkown type'
        file.write('\n')
    file.write('};')
    file.write('\n\n\n')
    file.write('class ' + classname + ' : ' + 'public RBase<' + structname + '>')
    file.write('\n{')
    file.write('\npublic:\n')
    file.write('\n};')
    file.write('\n\n#endif\n')
    file.close() 
    
def gencppfile(filename):
    gencomm(filename)
    file = open(filename,'a+')
    includefile = '''#include "''' + headfile + '"'
    file.write(includefile)
    file.close() 
    
if __name__ == '__main__':    

    table_name = 'CACHE_TEST_T'
    tableField = []
    tableField.append(Field('TEST_ID', 'NUMBER', 9, 'Y'))
    tableField.append(Field('TEST_DESC', 'VARCHAR2', 64, 'N'))
    tableField.append(Field('TEST_FLAG', 'NUMBER', 12, 'N'))
    
    tablesplit = table_name.lower().split('_')
    tablesplit.remove('t')
    classname = 'R'
    structname = 'T'
    for i in range(len(tablesplit)):
        classname += tablesplit[i].capitalize()
        structname += tablesplit[i].capitalize()
    print 'classname = %s' % classname

    headfile = classname + '.h'
    cppfile = classname + '.cpp'

    print 'generate head file: %s' % headfile
    genheadfile(headfile)
    
    print 'generate cpp file: %s' % cppfile
    gencppfile(cppfile)
    
