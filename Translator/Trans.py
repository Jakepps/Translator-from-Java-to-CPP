import json
import re
from tkinter import *
import tkinter.scrolledtext as st
from tkinter import ttk
import tkinter as tk
import os
import re

CLASSES_OF_TOKENS = ['W', 'I', 'O', 'R', 'N', 'C']

def prog1():
    #LAB1
    SERVICE_WORDS = ['abstract', 'case', 'continue', 'extends', 'goto', 'int', 'package', 'short',
                    'try', 'assert', 'catch', 'default', 'final', 'if', 'private',
                    'static', 'this', 'void', 'boolean', 'char', 'do','long', 'protected',
                    'throw', 'volatile', 'break', 'class', 'double', 'float', 'import', 'native',
                    'public', 'super','throws','while','byte','const','else','for','instanceof',
                    'new','return','switch','transient','print','println','main','System',
                    'out','String','args','in.nextInt()']

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
    input_sequence = re.sub(r"(\w)\+\+", r"\1 = \1 + 1", input_sequence)
    input_sequence = input_sequence.replace("public static void main(String[] args)\n{\n","\n\n")
    input_sequence = input_sequence.replace("\n}\n","")
    input_sequence = input_sequence.replace("public static division (int a, int b) {","\n\n")
    input_sequence = input_sequence.replace("System.out.println(","alert(")
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

def analyzer():
    global i
    global nxtsymb
    global row_counter
    i = -1
    nxtsymb = None # разбираемый символ
    row_counter = 1 # счётчик строк

    # лексемы
    tokens = {'W': {}, 'I': {}, 'O': {}, 'R': {}, 'N': {}, 'C': {}}

    # файлы, содержащие все таблицы лексем
    for token_class in tokens.keys():
        with open('%s.json' % token_class, 'r') as read_file:
            data = json.load(read_file)
            tokens[token_class] = data

    # файл, содержащий последовательность кодов лексем входной программы
    f = open('tokens.txt', 'r')
    input_sequence = f.read()
    f.close()

    regexp = '[' + '|'.join(tokens.keys()) + ']' + '\d+'
    match = re.findall(regexp, input_sequence)

    # обработка ошибочной ситуации
    def error():
        out_sq = 'Ошибка в строке '
        f = open('error.txt','w')
        out_sq += str(row_counter)
        f.write(out_sq)
        f.close()
        #print('Ошибка в строке', row_counter)
        return


    # помещение очередного символа в nxtsymb
    def scan():
        global i, nxtsymb, row_counter
        i += 1
        if i >= len(match):
            if not(nxtsymb in ['\n', ';', '}']):
                error()
        else:
            for token_class in tokens.keys():
                if match[i] in tokens[token_class]:
                    nxtsymb = tokens[token_class][match[i]]
            if nxtsymb == '\n':
                row_counter += 1
                scan()
            #print(i, row_counter, nxtsymb)

    # программа
    def program():
        operators()

    # операторы
    def operators():
        global i
        scan()
        while name() or \
            nxtsymb in ['int', 'double', 'string', 'boolean', 'float', '{', 'public static void main(String[] args)',\
                        'if', 'for', 'while', 'break', 'continue', 'return']:
            operator()
            if nxtsymb == ';':
                scan()
            if nxtsymb == '}':
                break

    # оператор
    def operator():
        if nxtsymb in ['int','double','float','boolean','string']:
            description()
            if nxtsymb != ';': error()
        elif name():
            scan()
            if nxtsymb == ':':
                scan()
                operator()
            elif nxtsymb == '(':
                scan()
                if nxtsymb != ')':
                    expression()
                    while nxtsymb == ',':
                        scan()
                        expression()
                    if nxtsymb != ')': error()
                scan()
            elif nxtsymb == '=':
                scan()
                expression()
                if nxtsymb != ';': error()
            else: error()
        elif nxtsymb == '{': compound_operator()
        elif nxtsymb == 'public static': function()
        elif nxtsymb == 'if': conditional_operator()
        elif nxtsymb == 'for': for_loop()
        elif nxtsymb == 'while': while_loop()
        elif nxtsymb == 'break':
            break_operator()
            scan()
            if nxtsymb != ';': error()
        elif nxtsymb == 'continue':
            continue_operator()
            scan()
            if nxtsymb != ';': error()
        elif nxtsymb == 'return':
            return_operator()
            if nxtsymb != ';': error()
        else: error()

    # имя (идентификатор)
    def name():
        return nxtsymb in tokens['I'].values() or \
            nxtsymb in ['System.out.println', 'alert']

    # описание
    def description():
        scan()
        if not(name()): error()
        scan()
        if nxtsymb == ',':
            while nxtsymb == ',':
                scan()
                if not(name()): error()
                scan()
        elif nxtsymb == '=':
            scan()
            if nxtsymb == 'new':
                scan()
                if not(name()): error()
                if not(nxtsymb == '['): error()
                scan()
                if not(integer()): error()
                scan()
                if not(nxtsymb == ']'): error()
                scan()
            else:
                expression()

    # список имен
    def list_of_names():
        if not(name()): error()
        scan()
        while nxtsymb == ',':
            scan()
            if not(name()): error()
            scan()

    # функция
    def function():
        if nxtsymb != 'public static void main(String[] args)\n{': error()
        scan()
        if not(name()): error()
        scan()
        if nxtsymb == '(':
            scan()
            if name():
                list_of_names()
        if nxtsymb != ')': error()
        scan()
        compound_operator()

    # выражение
    def expression():
        if nxtsymb == '(':
            scan()
            expression()
            if nxtsymb != ')': error()
            scan()
        elif name():
            scan()
            if nxtsymb == '(':
                scan()
                if nxtsymb != ')':
                    expression()
                    while nxtsymb == ',':
                        scan()
                        expression()
                    if nxtsymb != ')': error()
                scan()
            elif nxtsymb == '[':
                scan()
                expression()
                while nxtsymb == ',':
                    scan()
                    expression()
                if nxtsymb != ']': error()
                scan()
        elif number() or line(): scan()
        else: error()
        if arithmetic_operation():
            scan()
            expression()

    # число (числовая константа)
    def number():
        return nxtsymb in tokens['N'].values()

    # целое число (числовая константа)
    def integer():
        return nxtsymb in tokens['N'].values()

    # строка (символьная константа)
    def line():
        return nxtsymb in tokens['C'].values()

    # переменная
    def variable():
        if not(name()): error()
        scan()
        if nxtsymb == '[':
            scan()
            expression()
            if nxtsymb != ']': error()
            scan()

    # арифметическая операция
    def arithmetic_operation():
        return nxtsymb in ['%', '*', '+', '-', '/', '+=','-=', '*=', '/=', '%=']

    # составной оператор
    def compound_operator():
        if nxtsymb != '{': error()
        operators()
        if nxtsymb != '}': error()
        scan()

    # оператор присваивания
    def assignment_operator():
        scan()
        variable()
        if nxtsymb != '=': error()
        scan()
        expression()

    # условный оператор
    def conditional_operator():
        if nxtsymb != 'if': error()
        scan()
        if nxtsymb != '(': error()
        condition()
        if nxtsymb != ')': error()
        scan()
        operator()
        if nxtsymb == 'else':
            scan()
            operator()

    # условие
    def condition():
        if unary_log_operation():
            scan()
            if nxtsymb != '(': error()
            log_expression()
            if nxtsymb != ')': error()
            scan()
        else:
            log_expression()
            while binary_log_operation():
                log_expression()

    # унарная логическая операция
    def unary_log_operation():
        return nxtsymb == '!'

    # логическое выражение
    def log_expression():
        scan()
        expression()
        comparison_operation()
        scan()
        expression()

    # операция сравнения
    def comparison_operation():
        return nxtsymb in ['!=', '<', '<=', '==', '>', '>=']

    # бинарная логическая операция
    def binary_log_operation():
        return nxtsymb == '&&' or nxtsymb == '||'

    # цикл for
    def for_loop():
        if nxtsymb != 'for': error()
        scan()
        if nxtsymb != '(': error()
        assignment_operator()
        if nxtsymb != ';': error()
        condition()
        if nxtsymb != ';': error()
        assignment_operator()
        if nxtsymb != ')': error()
        scan()
        operator()

    # цикл while
    def while_loop():
        if nxtsymb != 'while': error()
        scan()
        if nxtsymb != '(': error()
        condition()
        if nxtsymb != ')': error()
        scan()
        operator()

    # оператор break
    def break_operator():
        return nxtsymb == 'break'

    # оператор continue
    def continue_operator():
        return nxtsymb == 'continue'

    # оператор return
    def return_operator():
        if nxtsymb != 'return': error()
        scan()
        expression()

    program()

def prog2():
    #LAB1
    SERVICE_WORDS = ['abstract', 'case', 'continue', 'extends', 'goto', 'int', 'package', 'short',
                    'try', 'assert', 'catch', 'default', 'final', 'if', 'private',
                    'static', 'this', 'void', 'boolean', 'char', 'do','long', 'protected',
                    'throw', 'volatile', 'break', 'class', 'double', 'float', 'import', 'native',
                    'public', 'super','throws','while','byte','const','else','for','instanceof',
                    'new','return','switch','transient','print','println','main','System',
                    'out','String','args','in.nextInt()']

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
        if token in ['}', 'public','static','void', 'procedure', 'int', 'double', 'boolean', 'String', 'float', 'args','return','System.out.println', 'main', 'in.nextInt()']:
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
                        stack[-1] += ' M' + str(tag_count)
                        out_seq += 'M' + str(tag_count) + ' УПЛ '
                        is_if = False
                    if is_while:
                        while not(re.match(r'^while M\d+$', stack[-1])):
                            out_seq += stack.pop() + ' '
                        tag_count += 1
                        out_seq += 'M' + str(tag_count) + ' УПЛ '
                        stack[-1] += ' M' + str(tag_count)
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
                while not(re.match(r'^if M\d+$', stack[-1])):
                    out_seq += stack.pop() + ' '
                stack.pop()
                tag_count += 1
                stack.append('if M' + str(tag_count))
                out_seq += 'M' + str(tag_count) + ' БП M' + str(tag_count - 1) + ' : '
            elif t[i] == 'while':
                tag_count += 1
                stack.append(t[i] + ' M' + str(tag_count))
                out_seq += 'M' + str(tag_count) + ' : '
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
                if if_count > 0 and re.match(r'^if M\d+$', stack[-1]):
                    tag = re.search('M\d+', stack[-1]).group(0)
                    j = i + 1
                    while j < len(t) and t[j] == '\n':
                        j += 1
                    if j >= len(t) or t[j] != 'else':
                        stack.pop()
                        out_seq += tag + ' : '
                        if_count -= 1
                if while_count > 0 and re.match(r'^while M\d+ M\d+$', stack[-1]):
                    tag = re.findall('M\d+', stack[-1])
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
                        not(if_count > 0 and re.match(r'^if M\d+$', stack[-1])) and \
                        not(while_count > 0 and re.match(r'^while M\d+ M\d+$', stack[-1])):
                        out_seq += stack.pop() + ' '
                    if if_count > 0 and re.match(r'^if M\d+$', stack[-1]):
                        tag = re.search('M\d+', stack[-1]).group(0)
                        j = i + 1
                        while t[j] == '\n':
                            j += 1
                        if t[j] != 'else':
                            stack.pop()
                        out_seq += tag + ' : '
                        if_count -= 1
                    if while_count > 0 and re.match(r'^while M\d+ M\d+$', stack[-1]):
                        tag = re.findall('M\d+', stack[-1])
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

def prog3():
    #LAB1
    SERVICE_WORDS = ['abstract', 'case', 'continue', 'extends', 'goto', 'int', 'package', 'short',
                    'try', 'assert', 'catch', 'default', 'final', 'if', 'private',
                    'static', 'this', 'void', 'boolean', 'char', 'do','long', 'protected',
                    'throw', 'volatile', 'break', 'class', 'double', 'float', 'import', 'native',
                    'public', 'super','throws','while','byte','const','else','for','instanceof',
                    'new','return','switch','transient','print','println','main','System',
                    'out','String','args','in.nextInt()']

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
        if token in ['}', 'public','static','void', 'procedure', 'int', 'double', 'boolean', 'String', 'float', 'args','return','System.out.println', 'main', 'in.nextInt()']:
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
                        stack[-1] += ' M' + str(tag_count)
                        out_seq += 'M' + str(tag_count) + ' УПЛ '
                        is_if = False
                    if is_while:
                        while not(re.match(r'^while M\d+$', stack[-1])):
                            out_seq += stack.pop() + ' '
                        tag_count += 1
                        out_seq += 'M' + str(tag_count) + ' УПЛ '
                        stack[-1] += ' M' + str(tag_count)
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
                while not(re.match(r'^if M\d+$', stack[-1])):
                    out_seq += stack.pop() + ' '
                stack.pop()
                tag_count += 1
                stack.append('if M' + str(tag_count))
                out_seq += 'M' + str(tag_count) + ' БП M' + str(tag_count - 1) + ' : '
            elif t[i] == 'while':
                tag_count += 1
                stack.append(t[i] + ' M' + str(tag_count))
                out_seq += 'M' + str(tag_count) + ' : '
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
                if if_count > 0 and re.match(r'^if M\d+$', stack[-1]):
                    tag = re.search('M\d+', stack[-1]).group(0)
                    j = i + 1
                    while j < len(t) and t[j] == '\n':
                        j += 1
                    if j >= len(t) or t[j] != 'else':
                        stack.pop()
                        out_seq += tag + ' : '
                        if_count -= 1
                if while_count > 0 and re.match(r'^while M\d+ M\d+$', stack[-1]):
                    tag = re.findall('M\d+', stack[-1])
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
                        not(if_count > 0 and re.match(r'^if M\d+$', stack[-1])) and \
                        not(while_count > 0 and re.match(r'^while M\d+ M\d+$', stack[-1])):
                        out_seq += stack.pop() + ' '
                    if if_count > 0 and re.match(r'^if M\d+$', stack[-1]):
                        tag = re.search('M\d+', stack[-1]).group(0)
                        j = i + 1
                        while t[j] == '\n':
                            j += 1
                        if t[j] != 'else':
                            stack.pop()
                        out_seq += tag + ' : '
                        if_count -= 1
                    if while_count > 0 and re.match(r'^while M\d+ M\d+$', stack[-1]):
                        tag = re.findall('M\d+', stack[-1])
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

    #LAB3
    def is_identifier(token):
        return ((token in inverse_tokens) and re.match(r'^I\d+$', inverse_tokens[token])) or re.match(r'^M\d+$', token) or token in ['String[]', 'args', 'System.out.println', 'System.out.print', 'int', 'double', 'boolean','float']

    def is_constant(token):
        return ((token in inverse_tokens) and re.match(r'^C\d+$', inverse_tokens[token])) or ((token in inverse_tokens) and re.match(r'^N\d+$', inverse_tokens[token])) or token.isdigit() or token in ["in.nextInt()", "division(num,i)","No","Yes"]

    def is_operation(token):
        return (token in inverse_tokens) and re.match(r'^O\d+$', inverse_tokens[token])

    # лексемы (код-значение)
    tokens = {}

    # файлы, содержащие все таблицы лексем
    for token_class in CLASSES_OF_TOKENS:
        with open('%s.json' % token_class, 'r') as read_file:
            data = json.load(read_file)
            if token_class == 'C':
                for k in data.keys():
                    data[k] = re.sub(r"'([^']*)'", r'"\1"', data[k])
            tokens.update(data)

    # лексемы (значение-код)
    inverse_tokens = {val: key for key, val in tokens.items()}

    replace = {'in.nextInt()': 'cin >> ', 'System.out.println': 'cout << ', 'System.out.print': 'cout << ', 'int': 'int', 'double': 'double','boolean':'bool', '=': '=', '||': '||', '&&': '&&', '!=': '!=', '==': '==', '/': '/', '%': '%', '!': '!', '++': '+= 1'}

    # файл, содержащий обратную польскую запись
    f = open('reverse_polish_entry.txt', 'r')
    inp_seq = f.read()
    inp_seq = inp_seq.replace("\"Yes\"","Yes")
    inp_seq = inp_seq.replace("\"No\"","No")
    inp_seq = inp_seq.replace("public static division a int b int a return b % ","")
    inp_seq = inp_seq.replace("division num i == 0 2Ф 1Ф (","division(num,i) 0 ==")
    inp_seq = inp_seq.replace("public static void 2 АЭМ String args ","String[] args НП ")
    inp_seq = re.sub(r"(System\.out\.println\s+)(\w+)", r"\g<1>\g<2> 1 Ф", inp_seq)
    inp_seq = inp_seq.replace("main ","")
    inp_seq = inp_seq.replace("1Ф int ","1Ф КП ")
    inp_seq = inp_seq.replace("int in . nextInt 0Ф","in.nextInt()")
    inp_seq = inp_seq.replace("++","1 +=")
    inp_seq = inp_seq.replace("import java . util . Scanner ","")
    f.close()

    t = re.findall(r'(?:\'[^\']*\')|(?:"[^"]*")|(?:[^ ]+)', inp_seq)

    i = 0
    stack = []
    out_seq = ''
    is_func = False
    variable = {}
    while i < len(t):
        if is_func == True and not(is_identifier(t[i])):
            out_seq += ' {\n'
            is_func = False
        if is_identifier(t[i]) or is_constant(t[i]):
            stack.append(replace[t[i]] if t[i] in replace else t[i])
        elif t[i] == 'НП':
            stack.pop()
            stack.pop()
            out_seq += 'void main ()'
            is_func = True
        elif t[i] == 'КП':
            out_seq += '}\n}'
        elif t[i] == 'КО':
            stack.pop()
            stack.pop()
        elif t[i] == 'УПЛ':
            arg1 = stack.pop()
            arg2 = stack.pop()
            out_seq += f'if (!({arg2})) goto {arg1};\n'
        elif t[i] == 'БП':
            arg1 = stack.pop()
            out_seq += f'goto {arg1};\n'
        elif t[i] == ':':
            arg1 = stack.pop()
            out_seq += f'{arg1}: '
        elif is_operation(t[i]):
            if t[i] == '=' and len(stack) == 2:
                arg1 = stack.pop()
                arg2 = stack.pop()
                out_seq += f'{arg2} = {arg1};\n'
            elif t[i] == '=' and len(stack) >= 3:
                arg1 = stack.pop()
                arg0 = stack.pop()
                arg2 = stack.pop()
                out_seq += f'{arg0} {arg2} = {arg1};\n'
            elif t[i] in ['+=', '-=', '*=', '/=', '++']:
                op = t[i][0]
                arg1 = stack.pop()
                arg2 = stack.pop()
                out_seq += f'{arg2} {op}= {arg1};\n'
            else:
                operation = replace[t[i]] if t[i] in replace else t[i]
                arg1 = stack.pop()
                if t[i] != '!':
                    arg2 = stack.pop()
                    stack.append(f'({arg2} {operation} {arg1})')
                else:
                    stack.append(f'({operation}{arg1})')
        elif t[i] == 'АЭМ':
            k = int(stack.pop())
            a = []
            while k != 0:
                a.append(stack.pop())
                k -= 1
            a.reverse()
            out_seq += a[0] + '[' + ']['.join(a[1:]) + ']'
        elif t[i] in ['break','continue']:
            stack.append(replace[t[i]] if t[i] in replace else t[i])
            arg0 = stack.pop();
            out_seq += f'\t{arg0};\n'

        elif t[i] == 'Ф':
            k = int(stack.pop()) + 1
            a = []
            while k != 0:
                a.append(stack.pop())
                k -= 1
            a.reverse()
            if a[0] == 'cin >>':
                b = []
                out_seq += a[0] + '("' + ' '.join(b) + '", ' + ', '.join(map(lambda x: '&' + x, a[1:])) + ');\n'
            else:
                out_seq += a[0] + ', '.join(a[1:]) + ';\n'
        i += 1

    #while
    out_seq = re.sub(r'(M\d+): if \(!\((.*)\)\) goto (M\d+);(?:\n|\n((?:.|\n)+)\n)goto \1;\n\3: ', r'while \2 {\n\4\n}\n', out_seq)

    # if else
    out_seq = re.sub(r'if\s*\((.*)\s*<\s*(.*)\)\s*{\s*(.*?)\s*}\s*else\s*{\s*(.*?)\s*}\s*', r'if (\1 < \2)\n{\n\3\n}\nelse\n{\n\4\n}\n', out_seq)

    #if
    out_seq = re.sub(r"if\s*\(\s*!\s*\(\s*(.*)\s*\)\s*\)\s*goto\s+(M\d+)\s*;\s*(\n(?:.|\n)+?)\s*\2:\s*", r"if \1 {\3\n}\n", out_seq)

    out_seq = 'int division(int a, int b){\nreturn a % b;\n}\n\n' + out_seq
    out_seq = 'using namespace std;\n\n' + out_seq

    out_seq = out_seq.replace("Yes;","\"Yes\";")
    out_seq = out_seq.replace("No;","\"No\";")

    out_seq = re.sub(r"goto M(\d);", r"else {", out_seq)
    out_seq = re.sub(r"M(\d): ", r"", out_seq)

    def indent_cpp_code(code):
        indented_code = ""
        indentation = 0
        for line in code.split("\n"):
            if "{" in line:
                indented_code += ("\t" * indentation) + line + "\n"
                indentation += 1
            elif "}" in line:
                indentation -= 1
                indented_code += ("\t" * indentation) + line + "\n"
            else:
                indented_code += ("\t" * indentation) + line + "\n"
        return indented_code

    out_seq = indent_cpp_code(out_seq)
    out_seq = out_seq.replace("+= 1","++")

    out_seq = out_seq.replace("isPrime {","(isPrime) {");

    stack.clear()

    # файл, содержащий текст на выходном языке программирования
    f = open('c++.txt', 'w')
    f.write(out_seq)
    f.close()

def write_txt(data):
    with open('java.txt','w') as file:
        file.write(data)

def clicked1():
    write_txt(codetxt1.get("1.0","end"))

    tokenstext.delete("1.0",END)
    Wtext.delete("1.0",END)
    Rtext.delete("1.0",END)
    Otext.delete("1.0",END)
    Ntext.delete("1.0",END)
    Itext.delete("1.0",END)
    Ctext.delete("1.0",END)

    prog1()

    fw=open('W.json','r')
    textw=fw.read()
    textw=textw.replace("    ","")
    textw=textw.replace('"',"")
    textw=textw.replace(',',"")
    textw=textw[2:-1]
    Wtext.insert("1.0",textw)
    fw.close()

    fr=open('R.json','r')
    textr=fr.read()
    textr=textr.replace("    ","")
    textr=textr.replace('"',"")
    regex = r'(?<!,),(?!,)'
    textr=re.sub(regex,'',textr)
    textr=textr[2:-1]
    Rtext.insert("1.0",textr)
    fr.close()

    fo=open('O.json','r')
    texto=fo.read()
    texto=texto.replace("    ","")
    texto=texto.replace('"',"")
    texto=texto.replace(',',"")
    texto=texto[2:-1]
    Otext.insert("1.0",texto)
    fo.close()

    fn=open('N.json','r')
    textn=fn.read()
    textn=textn.replace("    ","")
    textn=textn.replace('"',"")
    textn=textn.replace(',',"")
    textn=textn[2:-1]
    Ntext.insert("1.0",textn)
    fn.close()

    fi=open('I.json','r')
    texti=fi.read()
    texti=texti.replace("    ","")
    texti=texti.replace('"',"")
    texti=texti.replace(',',"")
    texti=texti[2:-1]
    Itext.insert("1.0",texti)
    fi.close()

    fc=open('C.json','r')
    textc=fc.read()
    textc=textc.replace("    ","")
    textc=textc.replace('"',"")
    textc=textc.replace(',',"")
    textc=textc.replace("\\","")
    textc=textc[2:-1]
    Ctext.insert("1.0",textc)
    fc.close()

    f1 = open('tokens.txt','r')
    text = f1.read()
    tokenstext.insert("1.0",text)
    f1.close()

    filename = 'Trans.py'
    dir_path = os.getcwd()

    for file in os.listdir(dir_path):
        if file != filename:
            os.remove(os.path.join(dir_path, file))

def clicked2():
    write_txt(codetxt2.get("1.0","end"))

    opzstext.delete("1.0",END)

    prog2()

    f1 = open('reverse_polish_entry.txt','r')
    text = f1.read()
    opzstext.insert("1.0",text)
    f1.close()

    filename = 'Trans.py'
    dir_path = os.getcwd()

    for file in os.listdir(dir_path):
        if file != filename:
            os.remove(os.path.join(dir_path, file))

def clicked3():
    write_txt(codetxt3.get("1.0","end"))

    cpptext.delete("1.0",END)

    prog3()

    f1 = open('c++.txt','r')
    text = f1.read()
    cpptext.insert("1.0",text)
    f1.close()

    filename = 'Trans.py'
    dir_path = os.getcwd()

    for file in os.listdir(dir_path):
        if file != filename:
            os.remove(os.path.join(dir_path, file))

def clicked4():
    write_txt(codetxt4.get("1.0","end"))
    codetxt4.tag_remove("highlight", "1.0", "end")

    errorlb.config(text=" ")

    prog1()
    analyzer()

    dir_path = os.getcwd()

    ername = 'error.txt'
    for file in os.listdir(dir_path):
        if file == ername:
            f = open("error.txt",'r')
            err = f.read()
            errorlb.config(text= err)
            f.close()

            with open(ername) as f:
                for line in f:
                    match = re.search(r'\d+', line)
                    if match:
                        line_num = int(match.group())
                        highlight_line(codetxt4, line_num)
            break
        else:
            errorlb.config(text= 'Ошибок нет')

    filename = 'Trans.py'
    for file in os.listdir(dir_path):
        if file != filename:
            os.remove(os.path.join(dir_path, file))

def highlight_line(codetxt4, line_num):
    codetxt4.tag_remove("highlight", "1.0", "end")

    start = f"{line_num}.0"
    end = f"{line_num + 1}.0"

    codetxt4.tag_add("highlight", start, end)
    codetxt4.tag_config("highlight", background="red")

window = Tk()
window.title("Транслятор")
window.geometry('1100x500')

# Создаем виджет Notebook
notebook = ttk.Notebook(window)
notebook.pack(fill='both', expand=True)

# Создаем две вкладки
LR1 = ttk.Frame(notebook)
LR2 = ttk.Frame(notebook)
LR3 = ttk.Frame(notebook)
LR4 = ttk.Frame(notebook)

# Добавляем вкладки в Notebook
notebook.add(LR1, text='Токенизация')
notebook.add(LR2, text='Обратная польская нотация')
notebook.add(LR3, text='Перевод из Java в C++')
notebook.add(LR4, text='Синтаксический анализатор')

# Токены
codetxt1=st.ScrolledText(LR1)
codetxt1.place(x=40,y=0,width=410,height=250)

tokenstext=st.ScrolledText(LR1)
tokenstext.place(x=600,y=0,width=470,height=250)

Wlb=Label(LR1,text="Лексемы служебных слов:",font=("Arial", 12))
Wlb.place(x=35,y=280)
Wtext=st.ScrolledText(LR1)
Wtext.place(x=40,y=300,width=210,height=200)

Rlb=Label(LR1,text="Лексемы разделителей:",font=("Arial", 12))
Rlb.place(x=295,y=280)
Rtext=st.ScrolledText(LR1)
Rtext.place(x=300,y=300,width=210,height=200)

Olb=Label(LR1,text="Лексемы операций:",font=("Arial", 12))
Olb.place(x=555,y=280)
Otext=st.ScrolledText(LR1)
Otext.place(x=560,y=300,width=200,height=200)

Nlb=Label(LR1,text="Лексемы числовых констант:",font=("Arial", 12))
Nlb.place(x=815,y=280)
Ntext=st.ScrolledText(LR1)
Ntext.place(x=820,y=300,width=210,height=200)

Ilb=Label(LR1,text="Лексемы идентификаторов:",font=("Arial", 12))
Ilb.place(x=1075,y=280)
Itext=st.ScrolledText(LR1)
Itext.place(x=1080,y=300,width=210,height=200)

Clb=Label(LR1,text="Лексемы символьных констант:",font=("Arial", 12))
Clb.place(x=1080,y=0)
Ctext=st.ScrolledText(LR1)
Ctext.place(x=1080,y=30,width=210,height=200)

btngo=Button(LR1,text="Выполнить \n преобразование",command=clicked1,font=("Arial", 10))
btngo.place(x=470,y=90,width=110,height=50)

# ОПЗ
codetxt2=st.ScrolledText(LR2)
codetxt2.place(x=40,y=0,width=410,height=290)

opzstext=st.ScrolledText(LR2)
opzstext.place(x=600,y=80,width=500,height=140)

btngo=Button(LR2,text="Выполнить \n преобразование",command=clicked2,font=("Arial", 10))
btngo.place(x=470,y=90,width=110,height=50)

# Java -> C++
codetxt3 = st.ScrolledText(LR3)
codetxt3.place(x=40, y=0, width=410, height=390)

cpptext = st.ScrolledText(LR3)
cpptext.place(x=600, y=0, width=410, height=390)

btngo = tk.Button(LR3, text="Выполнить \n преобразование", command=clicked3, font=("Arial", 10))
btngo.place(x=470, y=90, width=110, height=50)

# Анализатор
codetxt4 = st.ScrolledText(LR4)
codetxt4.place(x=300, y=0, width=410, height=390)

codetxt4.tag_configure("highlight", background="red")

btngo = tk.Button(LR4, text="Проверить \n правильность кода", command=clicked4, font=("Arial", 10))
btngo.place(x=150, y=86, width=130, height=50)

errorlb = Label(LR4,text="Ошибок нет",font=("Arial", 12))
errorlb.place(x=400,y=400)

window.mainloop()
