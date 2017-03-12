from comm import *

fieldgetnumstr = '''
{
    if(m_pMem != NULL)
    {
        return m_pMem->%s;
    }
    return 0;
}
'''

fieldgetvarstr = '''
{
    if(m_pMem != NULL)
    {
        return m_pMem->%s;
    }
    return "";
}
'''

fileselectstr = '''
    DEMO_DEBUG_INFO("%s", "Enter getOneByKey.");
    IBOFactory *pFcty = CXT::getBOFactory();
    CHECK_NULL(pFcty);

    self_ptr<IPropertyValuePairs> pValues(IPropertyValuePairs::create(pFcty));
    CHECK_PTR(pValues);
        
    mpr_int32_t nRet = 0;
'''

funcendstr = '''
    RETURN_WHEN_ERR;
    
    RETURN_SUCCESS;
}

'''

funcinsertstr = '''
{
    IBOFactory *pFcty = CXT::getBOFactory();
    CHECK_NULL(pFcty);
    
    CREATE_BO(pFcty, "%s", m_pBO);
    CHECK_NULL(m_pBO);

    setFields(tRatableEventType);

    int nRet = pFcty->addRootBO(m_pBO);
    RETURN_WHEN_ERR;

    pFcty->registerObject(m_pBO);

    RETURN_SUCCESS;
}

'''

funcdeletestrhead = '''
{
    IBOFactory *pFcty = CXT::getBOFactory();
    CHECK_NULL(pFcty);

    mpr_int32_t nRet = 0;
    self_ptr<IPropertyValuePairs> pValues(IPropertyValuePairs::create(pFcty));
    CHECK_PTR(pValues);
    
'''
funcdeletestrend = '''
    RETURN_WHEN_ERR;
        
    nRet = pFcty->directDeleteBOByKey(m_pBO->getBONameID(), pValues);
    RETURN_WHEN_ERR;

    RETURN_SUCCESS;
}

'''

def gensetFuncDetail(file, classname, fieldname, tablefieldname, type, len):
    if type == 'NUMBER':
        if len <= 9:
            file.write('void ' + classname + '::set' + fieldname + '(int32_t nValue)\n')
            file.write('{\n')
            file.write('    m_pBO->setInteger("' + tablefieldname + '", nValue);\n')
            file.write('}\n')
        else:
            file.write('void ' + classname + '::set' + fieldname + '(int64_t lValue)\n')
            file.write('{\n')
            file.write('    m_pBO->setLong("' + tablefieldname + '", lValue);\n')
            file.write('}\n')
    elif type == 'VARCHAR2':
        file.write('void ' + classname + '::set' + fieldname + '(const char* szValue)\n')
        file.write('{\n')
        file.write('    m_pBO->setString("' + tablefieldname + '", szValue);\n')
        file.write('}\n')
    elif type == 'DATE':
        file.write('void ' + classname + '::set' + fieldname + '(TTime tValue)\n')
        file.write('{\n')
        file.write('    m_pBO->setDate("' + tablefieldname + '", tValue);\n')
        file.write('}\n')    
    else:
        print 'unkown type' 
        
def gengetFuncDetail(file, classname, fieldname, type, len):
    if type == 'NUMBER':
        if len <= 9:
            file.write('int32_t ' + classname + '::get' + fieldname + '() const')
            fieldname = 'm_n' + fieldname
            file.write(fieldgetnumstr % fieldname)
        else:
            file.write('int64_t ' + classname + '::get' + fieldname + '() const')
            fieldname = 'm_l' + fieldname
            file.write(fieldgetnumstr % fieldname)
    elif type == 'VARCHAR2':
        file.write('const char* ' + classname + '::get' + fieldname + '() const')
        fieldname = 'm_sz' + fieldname
        file.write(fieldgetvarstr % fieldname)
    elif type == 'DATE':
        file.write('TTime ' + classname + '::get' + fieldname + '() const')
        fieldname = 'm_t' + fieldname
        file.write(fieldgetnumstr % fieldname)        
    else:
        print 'unkown type' 
        
def genFuncimp(file, classname):
    for i in range(len(tableField)):
        fieldsplit = tableField[i].name.lower().split('_')
        fieldname = ''
        for j in range(len(fieldsplit)):
            fieldname += fieldsplit[j].capitalize()
        gensetFuncDetail(file, classname, fieldname, tableField[i].name, tableField[i].type, tableField[i].len)
        file.write('\n')

    for i in range(len(tableField)):
        fieldsplit = tableField[i].name.lower().split('_')
        fieldname = ''
        for j in range(len(fieldsplit)):
            fieldname += fieldsplit[j].capitalize()
        gengetFuncDetail(file, classname, fieldname, tableField[i].type, tableField[i].len)
        file.write('\n')

def genSelectFuncImp(file, classname):
    file.write('int ' + classname + '::getOneByKey(')
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
    file.write(')\n')
    file.write(fileselectstr)
    for i in range(len(tableField)):
        if tableField[i].iskey:         
            fieldsplit = tableField[i].name.lower().split('_')
            fieldname = ''
            for j in range(len(fieldsplit)):
                fieldname += fieldsplit[j].capitalize()
            if tableField[i].type == 'NUMBER':
                if tableField[i].len <= 9:
                    file.write('    nRet = pValues->setInteger("' + tableField[i].name + '", n' + fieldname + ');\n')
                else:
                    file.write('    nRet = pValues->setLong("' + tableField[i].name + '", l' + fieldname + ');\n')
            elif tableField[i].type == 'VARCHAR2':
                file.write('    nRet = pValues->setString("' + tableField[i].name + '", sz' + fieldname + ');\n')
            elif tableField[i].type == 'DATE':
                file.write('    nRet = pValues->setDate("' + tableField[i].name + '", t' + fieldname + ');\n')
            else:
                print 'unkown type'
            file.write('    RETURN_WHEN_ERR;\n\n')
    file.write('    nRet = getByKey(pFcty, "' + table_name + '", pValues);')
    file.write(funcendstr)            

def genSetFieldsFunc(file, classname, structname):
    tempname = structname[0].lower() + structname[1:]
    file.write('int32_t ' + classname + '::setFields(const ' + structname + '& ' + tempname + ')\n')
    file.write('{\n')
    for i in range(len(tableField)):        
        fieldsplit = tableField[i].name.lower().split('_')
        fieldname = ''
        for j in range(len(fieldsplit)):
            fieldname += fieldsplit[j].capitalize()    
        file.write('    this->set' + fieldname + '(' + tempname + '.')
        if tableField[i].type == 'NUMBER':
            if tableField[i].len <= 9:
                file.write('m_n' + fieldname + ');\n')
            else:
                file.write('m_l' + fieldname + ');\n')
        elif tableField[i].type == 'VARCHAR2':
            file.write('m_sz' + fieldname + ');\n')
        elif tableField[i].type == 'DATE':
            file.write('m_t' + fieldname + ');\n')
        else:
            print 'unkown type'
    file.write('\n    RETURN_SUCCESS;\n')
    file.write('}\n\n')

def genInsertFunc(file, classname, structname):
    tempname = structname[0].lower() + structname[1:]
    file.write('int32_t '+ classname + '::insert(const ' + structname + '& ' + tempname + ')')    
    file.write(funcinsertstr % table_name)

def gendeleteFunc(file, classname, structname):
    tempname = structname[0].lower() + structname[1:]
    file.write('int32_t '+ classname + '::deleteByKey(const ' + structname + '& ' + tempname + ')')    
    file.write(funcdeletestrhead)
    for i in range(len(tableField)):
        if tableField[i].iskey:         
            fieldsplit = tableField[i].name.lower().split('_')
            fieldname = ''
            for j in range(len(fieldsplit)):
                fieldname += fieldsplit[j].capitalize()
            if tableField[i].type == 'NUMBER':
                if tableField[i].len <= 9:
                    file.write('    nRet = pValues->setInteger("' + tableField[i].name + '", ' + tempname + '.m_n' + fieldname + ');\n')
                else:
                    file.write('    nRet = pValues->setLong("' + tableField[i].name + '", ' + tempname + '.m_l' + fieldname + ');\n')
            elif tableField[i].type == 'VARCHAR2':
                file.write('    nRet = pValues->setString("' + tableField[i].name + '", ' + tempname + '.m_sz' + fieldname + ');\n')
            elif tableField[i].type == 'DATE':
                file.write('    nRet = pValues->setDate("' + tableField[i].name + '", ' + tempname + '.m_t' + fieldname + ');\n')
            else:
                print 'unkown type'
    file.write('    nRet = pFcty->getBOByKey(m_pBO, "' + table_name + '", pValues);\n')
    file.write(funcdeletestrend)
                
def gencppfile(filename, headfile, classname, structname):
    gencomm(filename)
    file = open(filename,'a+')
    includefile = '''#include "''' + headfile + '"'
    file.write(includefile)
    file.write('\n#include "CXT.h"\n\n')
    genFuncimp(file, classname)
    genSelectFuncImp(file, classname)
    genSetFieldsFunc(file, classname, structname)
    genInsertFunc(file, classname, structname)
    gendeleteFunc(file, classname, structname)
    file.close() 
