from comm import *
from head import *
from cppfile import *
from xmlfile import *

if __name__ == '__main__': 
    classname = ''
    structname = ''

    tableField.append(Field('TEST_ID', 'NUMBER', 9, 'Y', '', True))
    tableField.append(Field('TEST_DESC', 'VARCHAR2', 64, 'N', '', False))
    tableField.append(Field('TEST_FLAG', 'NUMBER', 12, 'N', '', False))

    print table_name
    tablesplit = table_name.lower().split('_')
    tablesplit.remove('t')
    classname += 'C'
    structname += 'T'
    for i in range(len(tablesplit)):
        classname += tablesplit[i].capitalize()
        structname += tablesplit[i].capitalize()

    print classname
    print structname
    
    headfile = classname + '.h'
    cppfile = classname + '.cpp'
    xmlfile = table_name + '.bo.xml'
    
    print 'generate head file: %s' % headfile
    genheadfile(headfile, classname, structname)
    
    print 'generate cpp file: %s' % cppfile
    gencppfile(cppfile, headfile)
    
    print 'generate xml file: %s' % xmlfile
    genxmlfile(xmlfile,table_name)
    
