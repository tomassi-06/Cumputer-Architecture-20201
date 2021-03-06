import sys
import os
from pathlib import Path
from VM_PARSER import VM_Parser
from VM_WRITER import VM_Writer


#This is to be able to read inside directories all the .vm files, and translate them to hack
path = sys.argv[1::]
vm_files = []

# If there is an argument and it is a directory
if len(path) == 1 and Path(path[0]).is_dir():

    #if the directory doesn't have an / we add it
    if path[0].endswith("/") is False:
        path[0] = path[0]+'/'
    output_file_name = path[0] #output will be the same as the name of the dir
    for r, d, f in os.walk(sys.argv[1]): # we walk to find the .vm files that has the dir
        for file in f:
            if '.vm' in file:
                vm_files.append(output_file_name+file)
# If there is an argument and it is a file                
elif len(path) == 1 and Path(path[0]).is_file():
    if '.vm'in path[0]:
        output_file_name = path[0].split('.vm')[0]
        vm_files.append(output_file_name)

Writer = VM_Writer(output_file_name)


for file_path in vm_files:  

    print(file_path)
    Parser = VM_Parser(file_path+'.vm')
    Writer.set_output_filename(file_path)

    while Parser.hasMoreCommands():
        Parser.advance()
        if Parser.commandType() == 'C_PUSH':
            Writer.writePushPop('C_PUSH', Parser.arg1(), Parser.arg2())
        elif Parser.commandType() == 'C_POP':
            Writer.writePushPop('C_POP', Parser.arg1(), Parser.arg2())
        elif Parser.commandType() == 'C_ARITHMETIC':
            Writer.writeArithmetic(Parser.arg1())
        elif Parser.commandType() == 'C_LABEL':
            Writer.writeLabel(Parser.arg1())
        elif Parser.commandType() == 'C_IF':
            Writer.writeIf(Parser.arg1())
        elif Parser.commandType() == 'C_GOTO':
            Writer.writeGoto(Parser.arg1())
        elif Parser.commandType() == 'C_CALL':
            Writer.writeCall(Parser.arg1(), Parser.arg2())
        elif Parser.commandType() == 'C_FUNCTION':
            Writer.writeFunction(Parser.arg1(), Parser.arg2())
        elif Parser.commandType() == 'C_RETURN':
            Writer.writeReturn()
Writer.closeAll()    