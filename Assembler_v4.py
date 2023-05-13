#Assembler v4

#combined edits of v2.1 and v3

# ld and st (type D) use variables
# jump instructions (type E) use labels
# all instructions using mem_addr use labels/vars


#global errors dictionary
ERRORS_DIC = {}

#global dicts
variables = {}          #"var_name":"var_address"
labels = {}             #"label_name":"label_address"
output = {}             #"line_number":"binary_code"

flags_register = "0000_0000_0000_0000"
registers = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}


def decimal_to_binary(n):
    output_binary_code = bin(n)[2:]
    return output_binary_code

#3 register type
def type_A(line_output, line_lst, registers):
    global temp_cnt, alt_counter
    register1 = line_lst[1]
    register2 = line_lst[2]
    register3 = line_lst[3]

    if (register1 not in registers) or (register2 not in registers) or (register3 not in registers):
        ERRORS_DIC[temp_cnt+alt_counter+1] = "ERROR : Invalid Register"
        return "ERROR"
    elif "FLAGS" in (register1, register2, register3):
        ERRORS_DIC[temp_cnt+alt_counter+1] = "ERROR : Invalid use of FLAGS register"
        return "ERROR"

    line_output += f"00{registers[register1]}{registers[register2]}{registers[register3]}"
    return line_output


#register and immediate type
def type_B(line_output, line_lst, registers):
    global temp_cnt, alt_counter

    register = line_lst[1]

    if register not in registers:
        ERRORS_DIC[temp_cnt+alt_counter+1] = "ERROR : Invalid Register"
        return "ERROR"
    elif register == "FLAGS":
        ERRORS_DIC[temp_cnt+alt_counter+1] = "ERROR : Invalid use of FLAGS register"
        return "ERROR"

    imm = int(line_lst[2][1:])

    if (imm < 0) or (imm > 127):
        ERRORS_DIC[temp_cnt+alt_counter+1] = "ERROR : Illegal Immediate Value"
        return "ERROR"

    imm = decimal_to_binary(imm)

    length_of_imm_to_be_added = 7 - len(imm)       # handle overflow of 7 bits just before here pls
    for i in range(length_of_imm_to_be_added):
        imm = '0' + imm

    line_output += f"0{registers[register]}{imm}"

    return line_output


#2 register type
def type_C(line_output, line_lst, registers):
    global temp_cnt, alt_counter
    register1 = line_lst[1]
    register2 = line_lst[2]

    if (register1 not in registers) or (register2 not in registers):
        ERRORS_DIC[temp_cnt+alt_counter+1] = "ERROR : Invalid Register"
        return "ERROR"
    elif "FLAGS" in (register1, register2) and line_output != "00011":
        ERRORS_DIC[temp_cnt+alt_counter+1] = "ERROR : Invalid use of FLAGS register"
        return "ERROR"

    line_output += f"00000{registers[register1]}{registers[register2]}"
    return line_output


#register and memory address type (variable)
def type_D(line_output, line_lst):
    global temp_cnt, alt_counter
    register = line_lst[1]

    if register not in registers:
        ERRORS_DIC[temp_cnt+alt_counter+1] = "ERROR : Invalid Register"
        return "ERROR"
    elif register == "FLAGS":
        ERRORS_DIC[temp_cnt+alt_counter+1] = "ERROR : Invalid use of FLAGS register"
        return "ERROR"

    variable = line_lst[2]

    if variable not in variables:
        if variable not in labels:
            ERRORS_DIC[temp_cnt+alt_counter+1] = "ERROR : Undefined Variable"
            return "ERROR"
        
        else:
            ERRORS_DIC[temp_cnt+alt_counter+1] = "ERROR : Misuse of label as variable"
            return "ERROR"
        
    line_output += f"0{registers[register]}{variables[variable]}"
    return line_output


#memory address type (jump to a label)
def type_E(line_output, line_lst):
    global temp_cnt, alt_counter
    line_output += "0000"

    label = line_lst[1]
    if label not in labels:
        if label not in variables:
            ERRORS_DIC[temp_cnt+alt_counter+1] = "ERROR : Undefined Label"
            return "ERROR"
        
        else:
            ERRORS_DIC[temp_cnt+alt_counter+1] = "ERROR : Misuse of variable as label"
            return "ERROR"
        
    line_output += labels[line_lst[1]]
    return line_output

for test_case in range(1,35):

    with open(f"hardBinTests\\test{test_case}.txt", 'r') as f:
        code_as_lst = f.readlines()

    #removing empty lines from code_as_lst
    if (code_as_lst):
        i = 0
        while(i < len(code_as_lst)):
            if (code_as_lst[i] == "" or code_as_lst[i] == "\n"):
                code_as_lst.pop(i)
            else:
                i += 1

    #checking all variable declarations are at beginning of program
    index = 0

    while(code_as_lst[index][:3] == 'var'):
        index += 1

    while(index < len(code_as_lst)):
        if code_as_lst[index][:3] == 'var':
            ERRORS_DIC[index+1] = "ERROR : Variable Declaration must be at the beginning"
        index += 1
    # pass 1
    """
    - count lines in the code
    - detect labels and vars
    - build dicts variables and labels
    - check for errors
    - initialise entries of output dictionary
    """

    line_counter = 0
    alt_counter = 0

    for line in code_as_lst:
        line_lst = line.split()

        match line_lst[0]:
            case "var":
                variables[line_lst[1]] = "0"
                alt_counter += 1

            case "hlt":
                line_counter += 1

            #type A instructions
            case "add":
                line_counter += 1

            case "sub":
                line_counter += 1

            case "mul":
                line_counter += 1

            case "xor":
                line_counter += 1

            case "or":
                line_counter += 1

            case "and":
                line_counter += 1


            #type B instructions
            case "mov":
                line_counter += 1

            case "rs":
                line_counter += 1

            case "ls":
                line_counter += 1


            #type C instructions
            case "div":
                line_counter += 1

            case "not":
                line_counter += 1

            case "cmp":
                line_counter += 1


            #type D instructions
            case "ld":
                line_counter += 1

            case "st":
                line_counter += 1


            #type E instructions
            case "jmp":
                line_counter += 1

            case "jlt":
                line_counter += 1

            case "jgt":
                line_counter += 1

            case "je":
                line_counter += 1


            #default case and label check
            case _:
                if (line_lst[0][-1] == ':'):                                #key-value pair is label-address in 7-bit binary
                    temp_addr = decimal_to_binary(line_counter)
                    temp_addr = "0"*(7 - len(temp_addr)) + temp_addr
                    labels[line_lst[0][:-1]] = temp_addr
                    line_counter += 1

                else:
                    alt_counter += 1
                    ERRORS_DIC[line_counter+alt_counter] = "Error: Operation does not exist"


    # pass 2
    """
    - replace labels and vars with their addresses
    - update entries of output dictionary
    """

    temp_cnt = 0
    alt_counter = 0
    for line in code_as_lst:
        line_lst = line.split()

        temp_lst = line_lst

        line_output = ""

        #replacing variables with their 7-bit addresses (zero based indexing), as they are encountered
        if (line_lst[0] == "var") and (line_lst[1] in variables.keys()):
            address = decimal_to_binary(line_counter)
            address = "0"*(7 - len(address)) + address
            variables[line_lst[1]] = address
            line_counter += 1

        elif (line_lst[0][-1] == ":"):
            temp_lst = line_lst[1:]
        
        #match case to manipulate changes in labels and variables, removed counter as temp counter would be sufficient
        match temp_lst[0]:

            case "var":
                alt_counter += 1

            case "hlt":
                line_output = "1101000000000000"

            #type A instructions
            case "add":
                line_output = "00000"
                try:
                    line_output = type_A(line_output, temp_lst, registers)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND ADD"

            case "sub":                                                                             
                line_output = "00001"
                try:
                    line_output = type_A(line_output, temp_lst, registers)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND SUB"

            case "mul":
                line_output = "00110"
                try:
                    line_output = type_A(line_output, temp_lst, registers)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND MUL"            

            case "xor":
                line_output = "01010"
                try:
                    line_output = type_A(line_output, temp_lst, registers)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND XOR"

            case "or":
                line_output = "01011"
                try:
                    line_output = type_A(line_output, temp_lst, registers)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND OR"

            case "and":
                line_output = "01100"
                try:
                    line_output = type_A(line_output, temp_lst, registers)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND AND"


            #type B instructions
            case "mov":
                if (temp_lst[2][0] == "$"):
                    line_output = "00010"
                    try:
                        line_output = type_B(line_output, temp_lst, registers)
                    except:
                        ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND MOV"

                else:       #type C (there are two mov instructions)                                                  
                    line_output = "00011"
                    try:
                        line_output = type_C(line_output, temp_lst, registers)
                    except:
                        ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND MOV"

            case "rs":
                line_output = "01000"
                try:
                    line_output = type_B(line_output, temp_lst, registers)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND RS"

            case "ls":
                line_output = "01001"
                try:
                    line_output = type_B(line_output, temp_lst, registers)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND LS"


            #type C instructions
            case "div":
                line_output = "00111"
                try:
                    line_output = type_C(line_output, temp_lst, registers)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND DIV"

            case "not":
                line_output = "01101"
                try:
                    line_output = type_C(line_output, temp_lst, registers)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND NOT"

            case "cmp":
                line_output = "01110"
                try:
                    line_output = type_C(line_output, temp_lst, registers)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND CMP"


            #type D instructions
            case "ld":
                line_output = "00100"
                try:
                    line_output = type_D(line_output, temp_lst)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND LD"


            case "st":
                line_output = "00101"
                try:
                    line_output = type_D(line_output, temp_lst)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND ST"


            #type E instructions
            case "jmp":
                line_output = "01111"
                try:
                    line_output = type_E(line_output, temp_lst)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND JMP"

            case "jlt":
                line_output = "11100"
                try:
                    line_output = type_E(line_output, temp_lst)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND JLT"

            case "jgt":
                line_output = "11101"
                try:
                    line_output = type_E(line_output, temp_lst)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND JGT"

            case "je":
                line_output = "11111"
                try:
                    line_output = type_E(line_output, temp_lst)
                except:
                    ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID USE OF COMMAND JE"


            #default case
            case _:
                ERRORS_DIC[temp_cnt+alt_counter+1] = "INVALID COMMAND"

        output[temp_cnt] = line_output
        #creating a temp counter (doesn't follow zero based indexing)
        if (line_lst[0] != "var"):    
            temp_cnt += 1


    # Missing HLT instruction
    binary_instruction_values = output.values()
    if "1101000000000000" not in binary_instruction_values:
        ERRORS_DIC[line_counter+1] = "ERROR : Missing hlt instruction"
    else:
        index = 0
        for i in code_as_lst:
            i = i.strip()
            index += 1
            if i == 'hlt' or i == 'hlt\n':
                break
        if index != len(code_as_lst):
            ERRORS_DIC[index] = "ERROR  hlt not last instruction"


    #code to merge the binary code, ie. values of output dictionary
    to_write = ""
    for i in output:
        to_write += str(i) + " : " + str(output[i]) + "\n"
    with open(f"hardBinOutputs\\hardBinOutput{test_case}.txt", 'w') as f:
        f.write(to_write)
    # with open("output_1.txt", 'w') as f:
    #     f.write("")
    # if "ERROR" not in to_write:
    #     with open("output_1.txt", 'w') as f:
    #         f.write(to_write)

    to_write = ""
    for i in ERRORS_DIC:
        to_write += str(i) + " : " + ERRORS_DIC[i] + "\n"

    with open(f"error_output\\error_dict{test_case}.txt", 'w') as f:
        f.write(to_write)
