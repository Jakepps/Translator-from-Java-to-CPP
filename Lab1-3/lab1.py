import json
from tkinter import *
import tkinter.scrolledtext as st
import re

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


def prog():
    tokens = {'W': {}, 'I': {}, 'O': {}, 'R': {}, 'N': {}, 'C': {}}

    for service_word in SERVICE_WORDS:
        check(tokens, 'W', service_word)
    for operation in OPERATIONS:
        check(tokens, 'O', operation)
    for separator in SEPARATORS:
        check(tokens, 'R', separator)

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

    f2 = open('tokens.txt', 'w')
    output_sequence = output_sequence.replace('R1 ','\t')
    f2.write(output_sequence)
    f2.close()

    for token_class in tokens.keys():
        with open('%s.json' % token_class, 'w') as write_file:
            data = {val: key for key, val in tokens[token_class].items()}
            json.dump(data, write_file, indent=4, ensure_ascii=False)

def write_txt(data):
    with open('java.txt','w') as file:
        file.write(data)

def clicked():
    write_txt(codetxt.get("1.0","end"))

    tokenstext.delete("1.0",END)
    Wtext.delete("1.0",END)
    Rtext.delete("1.0",END)
    Otext.delete("1.0",END)
    Ntext.delete("1.0",END)
    Itext.delete("1.0",END)
    Ctext.delete("1.0",END)

    prog()

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

    f4=open('tokens.txt','r')
    text=f4.read()
    tokenstext.insert("1.0",text)
    f4.close()

window=Tk()
window.title("LR1")

window.geometry('1600x700')

codetxt=st.ScrolledText(window)
codetxt.place(x=40,y=0,width=410,height=250)

tokenstext=st.ScrolledText(window)
tokenstext.place(x=600,y=0,width=470,height=250)

Wlb=Label(text="Лексемы служебных слов:",font=("Arial", 12))
Wlb.place(x=35,y=280)
Wtext=st.ScrolledText(window)
Wtext.place(x=40,y=300,width=210,height=200)

Rlb=Label(text="Лексемы разделителей:",font=("Arial", 12))
Rlb.place(x=295,y=280)
Rtext=st.ScrolledText(window)
Rtext.place(x=300,y=300,width=210,height=200)

Olb=Label(text="Лексемы операций:",font=("Arial", 12))
Olb.place(x=555,y=280)
Otext=st.ScrolledText(window)
Otext.place(x=560,y=300,width=200,height=200)

Nlb=Label(text="Лексемы числовых констант:",font=("Arial", 12))
Nlb.place(x=815,y=280)
Ntext=st.ScrolledText(window)
Ntext.place(x=820,y=300,width=210,height=200)

Ilb=Label(text="Лексемы идентификаторов:",font=("Arial", 12))
Ilb.place(x=1075,y=280)
Itext=st.ScrolledText(window)
Itext.place(x=1080,y=300,width=210,height=200)

Clb=Label(text="Лексемы символьных констант:",font=("Arial", 12))
Clb.place(x=1335,y=280)
Ctext=st.ScrolledText(window)
Ctext.place(x=1340,y=300,width=210,height=200)

btngo=Button(window,text="Выполнить \n преобразование",command=clicked,font=("Arial", 10))
btngo.place(x=470,y=90,width=110,height=50)

window.mainloop()