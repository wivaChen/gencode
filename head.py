from comm import *
    
def genFuncDef(file):
    for i in range(len(tableField)):
        fieldsplit = tableField[i].name.lower().split('_')
        fieldname = ''
        for j in range(len(fieldsplit)):
            fieldname += fieldsplit[j].capitalize()
        if tableField[i].type == 'NUMBER':
            if tableField[i].len <= 9:
                file.write('    void set' + fieldname + '(int32_t nValue);')
            else:
                file.write('    void set' + fieldname + '(int64_t lValue);')
        elif tableField[i].type == 'VARCHAR2':
            file.write('    void set' + fieldname + '(const char* szValue);')
        else:
            print 'unkown type'
        file.write('\n')
        
    file.write('\n\n')
    
    for i in range(len(tableField)):
        fieldsplit = tableField[i].name.lower().split('_')
        fieldname = ''
        for j in range(len(fieldsplit)):
            fieldname += fieldsplit[j].capitalize()
        if tableField[i].type == 'NUMBER':
            if tableField[i].len <= 9:
                file.write('    int32_t get' + fieldname + '();')
            else:
                file.write('    int64_t get' + fieldname + '();')
        elif tableField[i].type == 'VARCHAR2':
            file.write('    const char* get' + fieldname + '();')
        else:
            print 'unkown type'
        file.write('\n')

def genSelectFunc(file, structname):
    tempname = structname[0].lower() + structname[1:]
    file.write('    int32_t getOneByKey(const ' + structname + '& ' + tempname + ');')
    file.write('\n')
    
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
    genFuncDef(file)
    file.write('\n\n')
    genSelectFunc(file, structname)
    genInsertFunc(file, structname)
    genDeleteFunc(file, structname)
    file.write('\n')
    file.write('private:')
    file.write('\n')
    genSetFieldFunc(file, structname)
    file.write('\n};')
    file.write('\n\n#endif\n')
    file.close() 