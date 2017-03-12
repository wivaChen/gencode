import os
import sys
import string
import datetime

from comm import *

sttr = '''        <LoadPolicy namingSqlLabel="RATABLE_EVENT_TYPE_queryDataLoadData"> 
        </LoadPolicy>
        <ReadWritePolicy subSystem="RATING_BILLING">
            <ReadPolicy readMode="given">
                <BoMapping boMappingName="RATABLE_EVENT_TYPE_pdb" priority="0"/>
            </ReadPolicy>
            <WritePolicy>
                <Insert insertMode="given">
                    <BoMapping boMappingName="RATABLE_EVENT_TYPE_pdb" priority="0"/>
                </Insert>
                <Update updateMode="given">
                    <BoMapping boMappingName="RATABLE_EVENT_TYPE_pdb" priority="0"/>
                </Update>
                <Delete deleteMode="given">
                    <BoMapping boMappingName="RATABLE_EVENT_TYPE_pdb" priority="0"/>
                </Delete>
            </WritePolicy>
        </ReadWritePolicy>
        <ReadWritePolicy subSystem="BILLING">
            <ReadPolicy readMode="given">
                <BoMapping boMappingName="RATABLE_EVENT_TYPE_pdb" priority="0"/>
            </ReadPolicy>
        </ReadWritePolicy>'''
        
def genxmlfile(filename, tablename):
    file = open(filename,'w')
    file.write('<?xml version="1.0" encoding="UTF-8"?> \n')
    file.write('<BoDAF xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="..\..\..\\bo.xsd">\n')
    file.write('    <BoSchema name="' + tablename + '" type="root">\n')
    for i in range(len(tableField)):
        if tableField[i].iskey:
            file.write('        <Key name="' + tableField[i].name + '" dataType="')
        else:
            file.write('        <Property name="' + tableField[i].name + '" dataType="')
        if tableField[i].type == 'NUMBER':
            if tableField[i].len <= 9:
                file.write('int32" />\n')
            else:
                file.write('int64" />\n')
        elif tableField[i].type == 'VARCHAR2':
            nLen = tableField[i].len
            while(nLen % 4 != 0):
                nLen += 1
            file.write('string" length="' + str(nLen) + '" />\n')
        elif tableField[i].type == 'DATE':
            file.write('datetime" />\n') 
        else:
            print('unknown type\n')            
    file.write('    </BoSchema>\n')
    
    file.write('    <BoMapping boName="' + tablename +'">\n')
    file.write('        <ORMapping boMappingName="' + tablename +'_pdb" dsGroup="HBPA_PDB_DSGRP" tableName="' + tablename + '">\n')
    file.write('            <AutoMapping>\n')
    for i in range(len(tableField)):
        if tableField[i].iskey:
            file.write('                <KeyMapping fieldName="' + tableField[i].name + '" propertyName="' + tableField[i].name + '" />\n')
        else:
            file.write('                <PropertyMapping fieldName="' + tableField[i].name + '" propertyName="' + tableField[i].name + '" />\n')
            
    queryname = tablename + '_queryDataLoadData'
    
    file.write('                <QueryCondition name="' + queryname + '">\n')
    file.write('                    <SQL dbType="oracle" namingSqlLabel="' + queryname + '" />\n')
    file.write('                </QueryCondition>\n')
    file.write('            </AutoMapping>\n')
    file.write('        </ORMapping>\n')
    file.write('    </BoMapping>\n')
    file.write('    <BoNamingSql label="' + queryname + '">\n')
    file.write('        <Context>select ')
    
    for i in range(len(tableField)):
        if i != 0:
            file.write(',')
        file.write(tableField[i].name)
    file.write(' from ' + tablename + ' where 1=1 </Context>\n')
    file.write('    </BoNamingSql>\n') 
    
    file.write('    <BoPolicy boName="' + tablename + '">\n')
    tablestr = sttr.replace('RATABLE_EVENT_TYPE', tablename)    
    file.write(tablestr)
    file.write('\n')
    file.write('    </BoPolicy>\n')    
    file.write('</BoDAF>\n')
    
    file.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
