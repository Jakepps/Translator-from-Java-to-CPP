import json
import re
from tkinter import *
import tkinter.scrolledtext as st
import re

def prog():
    #LAB1
    SERVICE_WORDS = ['abstract', 'case', 'continue', 'extends', 'goto', 'int', 'package', 'short', 
                    'try', 'assert', 'catch', 'default', 'final', 'if', 'private', 
                    'static', 'this', 'void', 'boolean', 'char', 'do','long', 'protected', 
                    'throw', 'volatile', 'break', 'class', 'double', 'float', 'import', 'native', 
                    'public', 'super','throws','while','byte','const','else','for','instanceof',
                    'new','return','switch','transient','print','println','main','System',
                    'out','String','args']

    OPERATIONS = ['*','+','-','%', '/','++','*=','+=','-=','%=','/=','==', '<', '<=', '!=', '=', '>', '>=','&','|']

    SEPARATORS = ['\t', '\n', ' ', '(', ')', ',', '.', ':', ';', '[', ']','{','}']


    def check(tokens, token_class, token_value):
        if not(token_value in tokens[token_class]):
            token_code = str(len(tokens[token_class]) + 1)
            tokens[token_class][token_value] = token_class + token_code

    def get_operation(input_sequence, i):
        for k in range(2, 0, -1):
            if i + k < len(input_sequence):
                buffer = input_sequence[i:i + k]
                if buffer in OPERATIONS:
                    return buffer
        return ''

    def get_separator(input_sequence, i):
        buffer = input_sequence[i]
        if buffer in SEPARATORS:
            return buffer
        return ''

    # лексемы
    tokens = {'W': {}, 'I': {}, 'O': {}, 'R': {}, 'N': {}, 'C': {}}

    for service_word in SERVICE_WORDS:
        check(tokens, 'W', service_word)
    for operation in OPERATIONS:
        check(tokens, 'O', operation)
    for separator in SEPARATORS:
        check(tokens, 'R', separator)

    # файл, содержащий текст на входном языке программирования
    f = open('java.txt', 'r')
    input_sequence = f.read()
    f.close()

    i = 0
    state = 'S'
    output_sequence = buffer = ''
    while i < len(input_sequence):
        symbol = input_sequence[i]
        operation = get_operation(input_sequence, i)
        separator = get_separator(input_sequence, i)
        if state == 'S':
            buffer = ''
            if symbol.isalpha():
                state = 'q1'
                buffer += symbol
            elif symbol.isdigit():
                state = 'q3'
                buffer += symbol
            elif symbol == "'":
                state = 'q9'
                buffer += symbol
            elif symbol == '"':
                state = 'q10'
                buffer += symbol
            elif symbol == '/':
                state = 'q11'
            elif operation:
                check(tokens, 'O', operation)
                output_sequence += tokens['O'][operation] + ' '
                i += len(operation) - 1
            elif separator:
                if separator != ' ':
                    check(tokens, 'R', separator)
                    output_sequence += tokens['R'][separator]
                    if separator == '\n':
                        output_sequence += '\n'
                    else:
                        output_sequence += ' '
            elif i == len(input_sequence) - 1:
                state = 'Z'
        elif state == 'q1':
            if symbol.isalpha():
                buffer += symbol
            elif symbol.isdigit():
                state = 'q2'
                buffer += symbol
            else:
                if operation or separator:
                    if buffer in SERVICE_WORDS:
                        output_sequence += tokens['W'][buffer] + ' '
                    elif buffer in OPERATIONS:
                        output_sequence += tokens['O'][buffer] + ' '
                    else:
                        check(tokens, 'I', buffer)
                        output_sequence += tokens['I'][buffer] + ' '
                    if operation:
                        check(tokens, 'O', operation)
                        output_sequence += tokens['O'][operation] + ' '
                        i += len(operation) - 1
                    if separator:
                        if separator != ' ':
                            check(tokens, 'R', separator)
                            output_sequence += tokens['R'][separator]
                            if separator == '\n':
                                output_sequence += '\n'
                            else:
                                output_sequence += ' '
                state = 'S'
        elif state == 'q2':
            if symbol.isalnum():
                buffer += symbol
            else:
                if operation or separator:
                    check(tokens, 'I', buffer)
                    output_sequence += tokens['I'][buffer] + ' '
                    if operation:
                        check(tokens, 'O', operation)
                        output_sequence += tokens['O'][operation] + ' '
                        i += len(operation) - 1
                    if separator:
                        if separator != ' ':
                            check(tokens, 'R', separator)
                            output_sequence += tokens['R'][separator]
                            if separator == '\n':
                                output_sequence += '\n'
                            else:
                                output_sequence += ' '
                    state = 'S'
        elif state == 'q3':
            if symbol.isdigit():
                buffer += symbol
            elif symbol == '.':
                state = 'q4'
                buffer += symbol
            elif symbol == 'e' or symbol == 'E':
                state = 'q6'
                buffer += symbol
            else:
                if operation or separator:
                    check(tokens, 'N', buffer)
                    output_sequence += tokens['N'][buffer] + ' '
                    if operation:
                        check(tokens, 'O', operation)
                        output_sequence += tokens['O'][operation] + ' '
                        i += len(operation) - 1
                    if separator:
                        if separator != ' ':
                            check(tokens, 'R', separator)
                            output_sequence += tokens['R'][separator]
                            if separator == '\n':
                                output_sequence += '\n'
                            else:
                                output_sequence += ' '
                    state = 'S'
        elif state == 'q4':
            if symbol.isdigit():
                state = 'q5'
                buffer += symbol
        elif state == 'q5':
            if symbol.isdigit():
                buffer += symbol
            elif symbol == 'e' or symbol == 'E':
                state = 'q6'
                buffer += symbol
            else:
                if operation or separator:
                    check(tokens, 'N', buffer)
                    output_sequence += tokens['N'][buffer] + ' '
                    if operation:
                        check(tokens, 'O', operation)
                        output_sequence += tokens['O'][operation] + ' '
                        i += len(operation) - 1
                    if separator:
                        if separator != ' ':
                            check(tokens, 'R', separator)
                            output_sequence += tokens['R'][separator]
                            if separator == '\n':
                                output_sequence += '\n'
                            else:
                                output_sequence += ' '
                    state = 'S'
        elif state == 'q6':
            if symbol == '-' or symbol == '+':
                state = 'q7'
                buffer += symbol
            elif symbol.isdigit():
                state = 'q8'
                buffer += symbol
        elif state == 'q7':
            if symbol.isdigit():
                state = 'q8'
                buffer += symbol
        elif state == 'q8':
            if symbol.isdigit():
                buffer += symbol
            else:
                if operation or separator:
                    check(tokens, 'N', buffer)
                    output_sequence += tokens['N'][buffer] + ' '
                    if operation:
                        check(tokens, 'O', operation)
                        output_sequence += tokens['O'][operation] + ' '
                        i += len(operation) - 1
                    if separator:
                        if separator != ' ':
                            check(tokens, 'R', separator)
                            output_sequence += tokens['R'][separator]
                            if separator == '\n':
                                output_sequence += '\n'
                            else:
                                output_sequence += ' '
                state = 'S'
        elif state == 'q9':
            if symbol != "'":
                buffer += symbol
            elif symbol == "'":
                buffer += symbol
                check(tokens, 'C', buffer)
                output_sequence += tokens['C'][buffer] + ' '
                state = 'S'
        elif state == 'q10':
            if symbol != '"':
                buffer += symbol
            elif symbol == '"':
                buffer += symbol
                check(tokens, 'C', buffer)
                output_sequence += tokens['C'][buffer] + ' '
                state = 'S'
        elif state == 'q11':
            if symbol == '/':
                state = 'q12'
            elif symbol == '*':
                state = 'q13'
        elif state == 'q12':
            if symbol == '\n':
                state = 'S'
            elif i == len(input_sequence) - 1:
                state = 'Z'
        elif state == 'q13':
            if symbol == '*':
                state = 'q14'
        elif state == 'q14':
            if symbol == '/':
                state = 'q15'
        elif state == 'q15':
            if symbol == '\n':
                state = 'S'
            elif i == len(input_sequence) - 1:
                state = 'Z'
        i += 1

    # файлы, содержащие все таблицы лексем
    for token_class in tokens.keys():
        with open('%s.json' % token_class, 'w') as write_file:
            data = {val: key for key, val in tokens[token_class].items()}
            json.dump(data, write_file, indent=4, ensure_ascii=False)

    # файл, содержащий последовательность кодов лексем входной программы
    f = open('tokens.txt', 'w')
    f.write(output_sequence)
    f.close()

    #LAB2
    CLASSES_OF_TOKENS = ['W', 'I', 'O', 'R', 'N', 'C']

    def is_identifier(token):
        return re.match(r'^I\d+$', inverse_tokens[token])

    def get_priority(token):
        if token in ['(', 'for', 'if', 'while', '[', 'АЭМ', 'Ф', '{']:
            return 0
        if token in [')', ',', ';', 'do', 'else', ']']:
            return 1
        if token == '=':
            return 2
        if token == '||':
            return 3
        if token == '&&':
            return 4
        if token == '!':
            return 5
        if token in ['<', '<=', '!=', '=', '>', '>=']:
            return 6
        if token in ['+', '-', '+=', '-=', '*=', '/=']:
            return 7
        if token in ['*', '/', '%']:
            return 8
        if token in ['}', 'public.static.void', 'procedure','int', 'double', 'boolean', 'String', 'float', 'args','return','System.out.println', 'main']:
            return 9
        return -1

    # лексемы (код-значение)
    tokens = {}

    # файлы, содержащие все таблицы лексем
    for token_class in CLASSES_OF_TOKENS:
        with open('%s.json' % token_class, 'r') as read_file:
            data = json.load(read_file)
            tokens.update(data)

    # лексемы (значение-код)
    inverse_tokens = {val: key for key, val in tokens.items()}

    # файл, содержащий последовательность кодов лексем входной программы
    f = open('tokens.txt', 'r')
    inp_seq = f.read()
    f.close()

    regexp = '[' + '|'.join(CLASSES_OF_TOKENS) + ']' + '\d+'
    match = re.findall(regexp, inp_seq)

    t = [tokens[i] for i in match]

    i = 0
    stack = []
    out_seq = ''
    aem_count = proc_num = proc_level = operand_count = 1
    func_count = tag_count = proc_num = if_count = while_count = \
                begin_count = end_count = bracket_count = 0
    is_if = is_while = is_description_var = False
    while i < len(t):
        p = get_priority(t[i])
        if p == -1:
            if t[i] != '\n' and t[i] != '\t':
                out_seq += t[i] + ' '
        else:
            if t[i] == '[':
                aem_count += 1
                stack.append(str(aem_count) + ' АЭМ')
            elif t[i] == ']':
                while not(re.match(r'^\d+ АЭМ$', stack[-1])):
                    out_seq += stack.pop() + ' '
                out_seq += stack.pop() + ' '
                aem_count = 1
            elif t[i] == '(':
                if is_identifier(t[i - 1]):
                    if t[i + 1] != ')':
                        func_count += 1
                    stack.append(str(func_count) + ' Ф')
                else:
                    stack.append(t[i])
                bracket_count += 1
            elif t[i] == ')':
                while stack[-1] != '(' and not(re.match(r'^\d+ Ф$', stack[-1])):
                    out_seq += stack.pop() + ' '
                if re.match(r'^\d+ Ф$', stack[-1]):
                    stack.append(str(func_count + 1) + ' Ф')
                    func_count = 0
                stack.pop()
                bracket_count -= 1
                if bracket_count == 0:
                    if is_if:
                        while stack[-1] != 'if':
                            out_seq += stack.pop() + ' '
                        tag_count += 1
                        stack[-1] += ' М' + str(tag_count)
                        out_seq += 'М' + str(tag_count) + ' УПЛ '
                        is_if = False
                    if is_while:
                        while not(re.match(r'^while М\d+$', stack[-1])):
                            out_seq += stack.pop() + ' '
                        tag_count += 1
                        out_seq += 'М' + str(tag_count) + ' УПЛ '
                        stack[-1] += ' М' + str(tag_count)
                        is_while = False
            elif t[i] == ',':
                while not(re.match(r'^\d+ АЭМ$', stack[-1])) and \
                    not(re.match(r'^\d+ Ф$', stack[-1])) and \
                    not(re.match(r'^var', stack[-1])):
                    out_seq += stack.pop() + ' '
                if re.match(r'^\d+ АЭМ$', stack[-1]):
                    aem_count += 1
                    stack.append(str(aem_count) + ' АЭМ')
                if re.match(r'^\d+ Ф$', stack[-1]):
                    func_count += 1
                    stack.append(str(func_count) + ' Ф')
            elif t[i] == 'if':
                stack.append(t[i])
                if_count += 1
                bracket_count = 0
                is_if = True
            elif t[i] == 'else':
                while not(re.match(r'^if М\d+$', stack[-1])):
                    out_seq += stack.pop() + ' '
                stack.pop()
                tag_count += 1
                stack.append('if М' + str(tag_count))
                out_seq += 'М' + str(tag_count) + ' БП М' + str(tag_count - 1) + ' : '
            elif t[i] == 'while':
                tag_count += 1
                stack.append(t[i] + ' М' + str(tag_count))
                out_seq += 'М' + str(tag_count) + ' : '
                while_count += 1
                bracket_count = 0
                is_while = True
            elif t[i] == 'for':
                j = i + 2
                bracket_count = 1
                a = []
                while t[j] != ';':
                    a.append(t[j])
                    j += 1
                    if t[j] == '(':
                        bracket_count += 1
                    elif t[j] == ')':
                        bracket_count -= 1
                j += 1
                b = []
                while t[j] != ';':
                    b.append(t[j])
                    j += 1
                    if t[j] == '(':
                        bracket_count += 1
                    elif t[j] == ')':
                        bracket_count -= 1
                j += 1
                c = []
                while bracket_count != 0:
                    c.append(t[j])
                    j += 1
                    if t[j] == '(':
                        bracket_count += 1
                    elif t[j] == ')':
                        bracket_count -= 1
                j += 1
                d = []
                while t[j] != ';' and t[j] != '{':
                    d.append(t[j])
                    j += 1
                if t[j] == '{':
                    j += 1
                    bracket_count = 1
                    d = ['{']
                    while bracket_count != 0:
                        d.append(t[j])
                        j += 1
                        if t[j] == '{':
                            bracket_count += 1
                        elif t[j] == '}':
                            bracket_count -= 1
                    d.append('}')
                j += 1
                t = t[:i] + a + [';', '\n', 'while', '('] + b + [')', '{', '\n'] + d + \
                    ['\n'] + c + [';', '\n', '}'] + t[j:]
                i -= 1
            elif t[i] == 'sub':
                proc_num += 1
                stack.append('PROC ' + str(proc_num) + ' ' + str(proc_level))
            elif t[i] == '{':
                if len(stack) > 0 and re.match(r'^PROC', stack[-1]):
                    num = re.findall(r'\d+', stack[-1])
                    stack.pop()
                    out_seq += '0 Ф ' + str(num[0]) + ' ' + str(num[1]) + ' НП '
                    stack.append('PROC ' + str(proc_num) + ' ' + str(proc_level))
                begin_count += 1
                proc_level = begin_count - end_count + 1
                stack.append(t[i])
            elif t[i] == '}':
                end_count += 1
                proc_level = begin_count - end_count + 1
                while stack[-1] != '{':
                    out_seq += stack.pop() + ' '
                stack.pop()
                if len(stack) > 0 and re.match(r'^PROC', stack[-1]):
                    stack.pop()
                    out_seq += 'КП '
                if if_count > 0 and re.match(r'^if М\d+$', stack[-1]):
                    tag = re.search('М\d+', stack[-1]).group(0)
                    j = i + 1
                    while j < len(t) and t[j] == '\n':
                        j += 1
                    if j >= len(t) or t[j] != 'else':
                        stack.pop()
                        out_seq += tag + ' : '
                        if_count -= 1
                if while_count > 0 and re.match(r'^while М\d+ М\d+$', stack[-1]):
                    tag = re.findall('М\d+', stack[-1])
                    stack.pop()
                    out_seq += tag[0] + ' БП ' + tag[1] + ' : '
                    while_count -= 1
            elif t[i] == ';':
                if len(stack) > 0 and re.match(r'^PROC', stack[-1]):
                    num = re.findall(r'\d+', stack[-1])
                    stack.pop()
                    out_seq += str(num[0]) + ' ' + str(num[1]) + ' НП '
                elif len(stack) > 0 and stack[-1] == 'end':
                    stack.pop()
                    out_seq += 'КП '
                elif is_description_var:
                    proc_num, proc_level = re.findall('\d+', stack[-1])
                    stack.pop()
                    out_seq += str(operand_count) + ' ' + proc_num + ' ' + proc_level + \
                            ' КО '
                    is_description_var = False
                elif if_count > 0 or while_count > 0:
                    while not(len(stack) > 0 and stack[-1] == '{') and \
                        not(if_count > 0 and re.match(r'^if М\d+$', stack[-1])) and \
                        not(while_count > 0 and re.match(r'^while М\d+ М\d+$', stack[-1])):
                        out_seq += stack.pop() + ' '
                    if if_count > 0 and re.match(r'^if М\d+$', stack[-1]):
                        tag = re.search('М\d+', stack[-1]).group(0)
                        j = i + 1
                        while t[j] == '\n':
                            j += 1
                        if t[j] != 'else':
                            stack.pop()
                        out_seq += tag + ' : '
                        if_count -= 1
                    if while_count > 0 and re.match(r'^while М\d+ М\d+$', stack[-1]):
                        tag = re.findall('М\d+', stack[-1])
                        out_seq += tag[0] + ' БП ' + tag[1] + ' : '
                        while_count -= 1
                else:
                    while len(stack) > 0 and stack[-1] != '{':
                        out_seq += stack.pop() + ' '
            else:
                while len(stack) > 0 and get_priority(stack[-1]) >= p:
                    out_seq += stack.pop() + ' '
                stack.append(t[i])
        i += 1

    while len(stack) > 0:
        out_seq += stack.pop() + ' '

    out_seq = out_seq.replace("System . out . println", "System.out.println")
    out_seq = re.sub(r'(\d) Ф', r'\1Ф', out_seq)

    # файл, содержащий обратную польскую запись
    f = open('reverse_polish_entry.txt', 'w')
    f.write(out_seq)
    f.close()

def write_txt(data):
    with open('java.txt','w') as file:
        file.write(data)

def clicked():
    write_txt(codetxt.get("1.0","end"))

    opzstext.delete("1.0",END)

    prog()

    f1 = open('reverse_polish_entry.txt','r')
    text = f1.read()
    opzstext.insert("1.0",text)
    f1.close()

window=Tk()
window.title("LR2")

window.geometry('1100x500')

codetxt=st.ScrolledText(window)
codetxt.place(x=40,y=0,width=410,height=290)

opzstext=st.ScrolledText(window)
opzstext.place(x=600,y=80,width=500,height=140)

btngo=Button(window,text="Выполнить \n преобразование",command=clicked,font=("Arial", 10))
btngo.place(x=470,y=90,width=110,height=50)

window.mainloop()