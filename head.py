from comm import *
    
def genFuncDef(file):
    for i in range(len(tableField)):
        fieldsplit = tableField[i].name.lower().split('_')
        fieldname = ''
        for j in range(len(fieldsplit)):
            fieldname += fieldsplit[j].capitalize()
        file.write('    void set' + fieldname)
        if tableField[i].type == 'NUMBER':
            if tableField[i].len <= 9:
                file.write('(int32_t nValue);\n')
            else:
                file.write('(int64_t lValue);\n')
        elif tableField[i].type == 'VARCHAR2':
            file.write('(const char* szValue);\n')
        elif tableField[i].type == 'DATE':
            file.write('(TTime tValue);\n')
        else:
            print 'unkown type'
    file.write('\n')
    
    for i in range(len(tableField)):
        fieldsplit = tableField[i].name.lower().split('_')
        fieldname = ''
        for j in range(len(fieldsplit)):
            fieldname += fieldsplit[j].capitalize()
        if tableField[i].type == 'NUMBER':
            if tableField[i].len <= 9:
                file.write('    int32_t get' + fieldname + '();\n')
            else:
                file.write('    int64_t get' + fieldname + '();\n')
        elif tableField[i].type == 'VARCHAR2':
            file.write('    const char* get' + fieldname + '();\n')
        elif tableField[i].type == 'DATE':
            file.write('    TTime get' + fieldname +'();\n')
        else:
            print 'unkown type'

def genSelectFunc(file):
    file.write('    int ' + 'getOneByKey(')
    flag = 0
    for i in range(len(tableField)):
        if tableField[i].iskey:         
            fieldsplit = tableField[i].name.lower().split('_')
            fieldname = ''
            if flag == 1:
                file.write(', ')
            else:
                flag = 1
            for j in range(len(fieldsplit)):
                fieldname += fieldsplit[j].capitalize()
            if tableField[i].type == 'NUMBER':
                if tableField[i].len <= 9:
                    file.write('int32_t n' + fieldname)
                else:
                    file.write('int64_t l' + fieldname)
            elif tableField[i].type == 'VARCHAR2':
                file.write('const char* sz' + fieldname)
            elif tableField[i].type == 'DATE':
                file.write('TTime' + fieldname)
            else:
                print 'unkown type'  
    file.write(');\n')
    
def genInsertFunc(file, structname):
    tempname = structname[0].lower() + structname[1:]
    file.write('    int32_t insert(const ' + structname + '& ' + tempname + ');')
    file.write('\n')

def genDeleteFunc(file, structname):
    tempname = structname[0].lower() + structname[1:]
    file.write('    int32_t deleteByKey(const ' + structname + '& ' + tempname + ');')
    file.write('\n')

def genSetFieldFunc(file, structname):
    tempname = structname[0].lower() + structname[1:]
    file.write('    int32_t setFields(const ' + structname + '& ' + tempname + ');')
    file.write('\n')
    
def genheadfile(filename, classname, structname):
    gencomm(filename)
    file = open(filename,'a+')   
    headmacro = '__' + filename.split('.')[0].upper() + '_H__'
    file.writelines('#ifndef ' + headmacro)
    file.write('\n')
    file.writelines('#define ' + headmacro)
    file.write('\n\n')
    file.write('#include "RBase.h"\n')
    file.write('\n')
    file.write('struct ' + structname)
    file.write('\n{\n')
    for i in range(len(tableField)):
        fieldsplit = tableField[i].name.lower().split('_')
        fieldname = ''
        for j in range(len(fieldsplit)):
            fieldname += fieldsplit[j].capitalize()   
        if tableField[i].type == 'NUMBER':
            if tableField[i].len <= 9:
                file.write('    int32_t m_n' + fieldname + ';')
            else:
                file.write('    int64_t m_l' + fieldname + ';')
        elif tableField[i].type == 'VARCHAR2':
            file.write('    char m_sz' + fieldname + '[' + str(tableField[i].len) + '];')
        elif tableField[i].type == 'DATE':
            file.write('    TTime m_t' + fieldname + ';')
        else:
            print 'unkown type'
        file.write('\n')
    file.write('};')
    file.write('\n\n\n')
    file.write('class ' + classname + ' : ' + 'public RBase<' + structname + '>')
    file.write('\n{')
    file.write('\npublic:\n')
    genFuncDef(file)
    file.write('\n\n')
    genSelectFunc(file)
    genInsertFunc(file, structname)
    genDeleteFunc(file, structname)
    file.write('\n')
    file.write('private:')
    file.write('\n')
    genSetFieldFunc(file, structname)
    file.write('\n};')
    file.write('\n\n#endif\n')
    file.close() 
