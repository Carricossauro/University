import ply.yacc as yacc
import sys

from lex import tokens

def p_Programa(p):
    "Programa : Corpo"
    parser.assembly = f'START\n{p[1]}STOP'

def p_Programa_Decls(p):
    "Programa : Decls Corpo"
    parser.assembly = f'{p[1]}START\n{p[2]}STOP'

def p_Decls(p):
    "Decls    : Decl"
    p[0] = f'{p[1]}'

def p_Decls_Recursiva(p):
    "Decls    : Decls Decl"
    p[0] = f'{p[1]}{p[2]}'

def p_Decl_Int(p):
    "Decl     : INT NOME"
    if p[2] not in p.parser.registers:
        p.parser.registers.update({p[2] : p.parser.gp})
        p[0] = f'PUSHI 0\n'
        p.parser.ints.append(p[2])
        p.parser.gp += 1
    else:
        print("Erro: Variável já existe.")
        parser.success = False

def p_Decl_Int_Atr(p):
    "Decl     : INT NOME ATR NUM"
    if p[2] not in p.parser.registers:
        p.parser.registers.update({p[2] : p.parser.gp})
        p[0] = f'PUSHI {p[4]}\n'
        p.parser.ints.append(p[2])
        p.parser.gp += 1
    else:
        print("Erro: Variável já existe.")
        parser.success = False

def p_Decl_Array(p):
    "Decl     : ARRAY NOME NUM"
    if p[2] not in p.parser.registers:
        p.parser.registers.update({p[2] : (p.parser.gp, int(p[3]))})
        p[0] = f'PUSHN {p[3]}\n'
        p.parser.gp += int(p[3])
    else:
        print("Erro: Variável já existe.")
        parser.success = False

def p_Decl_Matriz(p):
    "Decl     : MATRIZ NOME NUM NUM"
    if p[2] not in p.parser.registers:
        p.parser.registers.update({p[2] : (p.parser.gp, int(p[3]), int(p[4]))})
        size = int(p[3])*int(p[4])
        p[0] = f'PUSHN {str(size)}\n'
        p.parser.gp += size
    else:
        print("Erro: Variável já existe.")
        parser.success = False

def p_Corpo(p):
    "Corpo    : Proc"
    p[0] = p[1]

def p_Corpo_Recursiva(p):
    "Corpo    : Corpo Proc"
    p[0] = f'{p[1]}{p[2]}'

def p_Proc_Atrib(p):
    "Proc     : Atrib"
    p[0] = p[1]

def p_Proc_Escrever(p):
    "Proc     : Escrever"
    p[0] = p[1]

def p_Proc_Se(p):
    "Proc     : Se"
    p[0] = p[1]

def p_Proc_Enquanto(p):
    "Proc     : Enquanto"
    p[0] = p[1]

def p_Se(p):
    "Se       : SE Cond ENTAO Corpo FIM"
    p[0] = f'{p[2]}JZ l{p.parser.labels}\n{p[4]}l{p.parser.labels}: NOP\n'
    p.parser.labels += 1

def p_Se_Senao(p):
    "Se       : SE Cond ENTAO Corpo SENAO Corpo FIM"
    p[0] = f'{p[2]}JZ l{p.parser.labels}\n{p[4]}JUMP l{p.parser.labels}f\nl{p.parser.labels}: NOP\n{p[6]}l{p.parser.labels}f: NOP\n'
    p.parser.labels += 1

def p_Enquanto(p):
    "Enquanto : ENQUANTO Cond FAZ Corpo FIM"
    p[0] = f'l{p.parser.labels}c: NOP\n{p[2]}JZ l{p.parser.labels}f\n{p[4]}JUMP l{p.parser.labels}c\nl{p.parser.labels}f: NOP\n'
    p.parser.labels += 1

def p_Atrib_expr_Int(p):
    "Atrib    : NOME ATR Expr"
    if p[1] in p.parser.registers:
        if p[1] in p.parser.ints:
            p[0] = f'{p[3]}STOREG {p.parser.registers.get(p[1])}\n'
        else:
            print("Erro: Variável não é de tipo inteiro.")
            parser.success = False

    else:
        print("Erro: Variável não definida.")
        parser.success = False

def p_Atrib_expr_Array(p):
    "Atrib    : NOME PRABRIR Expr PRFECHAR ATR Expr"
    if p[1] in p.parser.registers:
        if p[1] not in p.parser.ints and len(p.parser.registers.get(p[1])) == 2:
            p[0] = f'PUSHGP\nPUSHI {p.parser.registers.get(p[1])[0]}\nPADD\n{p[3]}{p[6]}STOREN\n'
        else:
            print(f"Erro: Variável {p[1]} não é um array.")
            parser.success = False
    else:
        print("Erro: Variável não definida.")
        parser.success = False

def p_Atrib_expr_Matriz(p):
    "Atrib    : NOME PRABRIR Expr VIRG Expr PRFECHAR ATR Expr"
    if p[1] in p.parser.registers:
        if p[1] not in p.parser.ints and len(p.parser.registers.get(p[1])) == 3:
            c = p.parser.registers.get(p[1])[2]
            p[0] = f'PUSHGP\nPUSHI {p.parser.registers.get(p[1])[0]}\nPADD\n{p[3]}PUSHI {c}\nMUL\n{p[5]}ADD\n{p[8]}STOREN\n'
        else:
            print(f"Erro: Variável {p[1]} não é uma matriz.")
            parser.success = False
    else:
        print("Erro: Variável não definida.")
        parser.success = False

def p_Atrib_Ler_Array(p):
    "Atrib    : NOME PRABRIR Expr PRFECHAR ATR LER"
    if p[1] in p.parser.registers:
        if p[1] not in p.parser.ints and len(p.parser.registers.get(p[1])) == 2:
            p[0] = f'PUSHGP\nPUSHI {p.parser.registers.get(p[1])[0]}\nPADD\n{p[3]}READ\nATOI\nSTOREN\n'
        else:
            print(f"Erro: Variável {p[1]} não é um array.")
            parser.success = False
    else:
        print("Erro: Variável não definida.")
        parser.success = False

def p_Atrib_Ler_Matriz(p):
    "Atrib    : NOME PRABRIR Expr VIRG Expr PRFECHAR ATR LER"
    if p[1] in p.parser.registers:
        if p[1] not in p.parser.ints and len(p.parser.registers.get(p[1])) == 3:
            c = p.parser.registers.get(p[1])[2]
            p[0] = f'PUSHGP\nPUSHI {p.parser.registers.get(p[1])[0]}\nPADD\n{p[3]}PUSHI {c}\nMUL\n{p[5]}ADD\nREAD\nATOI\nSTOREN\n'
        else:
            print(f"Erro: Variável {p[1]} não é uma matriz.")
            parser.success = False
    else:
        print("Erro: Variável não definida.")
        parser.success = False

def p_Atrib_Ler(p):
    "Atrib    : NOME ATR LER"
    if p[1] in p.parser.registers:
        p[0] = f'READ\nATOI\nSTOREG {p.parser.registers.get(p[1])}\n'
    else:
        print("Erro: Variável não definida.")
        parser.success = False

def p_Escrever_a(p):
    "Escrever : ESCREVERA NOME"
    if p[2] in p.parser.registers:
        if p[2] not in p.parser.ints:
            if len(p.parser.registers.get(p[2])) == 2:
                array = ""
                for i in range(p.parser.registers.get(p[2])[1]):
                    array += f'PUSHGP\nPUSHI {p.parser.registers.get(p[2])[0]}\nPADD\nPUSHI {i}\nLOADN\nWRITEI\nPUSHS " "\nWRITES\n'
                p[0] = array + 'PUSHS "\\n"\nWRITES\n'
            else:
                matriz = ""
                for l in range(p.parser.registers.get(p[2])[1]):
                    for c in range(p.parser.registers.get(p[2])[2]):
                        matriz += f'PUSHGP\nPUSHI {p.parser.registers.get(p[2])[0]}\nPADD\nPUSHI {p.parser.registers.get(p[2])[2] * l + c}\nLOADN\nWRITEI\nPUSHS " "\nWRITES\n'
                    matriz += 'PUSHS "\\n"\nWRITES\n'
                p[0] = matriz

        else:
            print("Erro: Variável não é um array.")
            parser.success = False
    else:
        print("Erro: Variável não definida.")
        parser.success = False

def p_Escrever(p):
    "Escrever : ESCREVER Expr"
    p[0] = f'{p[2]}WRITEI\nPUSHS "\\n"\nWRITES\n'

def p_Expr_P(p):
    "Expr     : PCABRIR Expr PCFECHAR"
    p[0] = p[2]

def p_Expr_Var(p):
    "Expr     : Var"
    p[0] = p[1]

def p_Expr_Num(p):
    "Expr     : NUM"
    p[0] = f'PUSHI {p[1]}\n'

def p_Expr_Soma(p):
    "Expr     : SOMA PCABRIR Expr VIRG Expr PCFECHAR"
    p[0] = f'{p[3]}{p[5]}ADD\n'

def p_Expr_Sub(p):
    "Expr     : SUB PCABRIR Expr VIRG Expr PCFECHAR"
    p[0] = f'{p[3]}{p[5]}SUB\n'

def p_Expr_Mult(p):
    "Expr     : MULT PCABRIR Expr VIRG Expr PCFECHAR"
    p[0] = f'{p[3]}{p[5]}MUL\n'

def p_Expr_Div(p):
    "Expr     : DIV PCABRIR Expr VIRG Expr PCFECHAR"
    p[0] = f'{p[3]}{p[5]}DIV\n'

def p_Expr_Mod(p):
    "Expr     : MOD PCABRIR Expr VIRG Expr PCFECHAR"
    p[0] = f'{p[3]}{p[5]}MOD\n'

def p_Expr_Cond(p):
    "Expr     : Cond"
    p[0] = p[1]

def p_Cond_P(p):
    "Cond     : PCABRIR Cond PCFECHAR"
    p[0] = p[2]

def p_Cond_Maior(p):
    "Cond     : MAIOR PCABRIR Expr VIRG Expr PCFECHAR"
    p[0] = f'{p[3]}{p[5]}SUP\n'

def p_Cond_Menor(p):
    "Cond     : MENOR PCABRIR Expr VIRG Expr PCFECHAR"
    p[0] = f'{p[3]}{p[5]}INF\n'

def p_Cond_Maiori(p):
    "Cond     : MAIORI PCABRIR Expr VIRG Expr PCFECHAR"
    p[0] = f'{p[3]}{p[5]}SUPEQ\n'

def p_Cond_Menori(p):
    "Cond     : MENORI PCABRIR Expr VIRG Expr PCFECHAR"
    p[0] = f'{p[3]}{p[5]}INFEQ\n'

def p_Cond_Igual(p):
    "Cond     : IGUAL PCABRIR Expr VIRG Expr PCFECHAR"
    p[0] = f'{p[3]}{p[5]}EQUAL\n'

def p_Cond_Nigual(p):
    "Cond     : NIGUAL PCABRIR Expr VIRG Expr PCFECHAR"
    p[0] = f'{p[3]}{p[5]}EQUAL\nNOT\n'

def p_Cond_E(p):
    "Cond     : E PCABRIR Cond VIRG Cond PCFECHAR"
    p[0] = f'{p[3]}{p[5]}ADD\nPUSHI 2\nEQUAL\n'

def p_Cond_Ou(p):
    "Cond     : OU PCABRIR Cond VIRG Cond PCFECHAR"
    p[0] = f'{p[3]}{p[5]}ADD\nPUSHI 1\nSUPEQ\n'

def p_Cond_Neg(p):
    "Cond     : NEG PCABRIR Cond PCFECHAR"
    p[0] = f'{p[3]}NOT\n'

def p_Var_Matriz(p):
    "Var      : NOME PRABRIR Expr VIRG Expr PRFECHAR"
    if p[1] in p.parser.registers:
        if p[1] not in p.parser.ints and len(p.parser.registers.get(p[1])) == 3:
            c = p.parser.registers.get(p[1])[2]
            p[0] = f'PUSHGP\nPUSHI {p.parser.registers.get(p[1])[0]}\nPADD\n{p[3]}PUSHI {c}\nMUL\n{p[5]}ADD\nLOADN\n'
        else:
            print(f"Erro: Variável {p[1]} não é uma matriz.")
            parser.success = False
    else:
        print("Erro: Variável não definida.")
        parser.success = False

def p_Var_Array(p):
    "Var      : NOME PRABRIR Expr PRFECHAR"
    if p[1] in p.parser.registers:
        if p[1] not in p.parser.ints and len(p.parser.registers.get(p[1])) == 2:
            p[0] = f'PUSHGP\nPUSHI {p.parser.registers.get(p[1])[0]}\nPADD\n{p[3]}LOADN\n'
        else:
            print(f"Erro: Variável {p[1]} não é um array.")
            parser.success = False
    else:
        print("Erro: Variável não definida.")
        parser.success = False

def p_Var_Int(p):
    "Var      : NOME"
    if p[1] in p.parser.registers:
        if p[1] in p.parser.ints:
            p[0] = f'PUSHG {p.parser.registers.get(p[1])}\n'
        else:
            print("Erro: Variável não é de tipo inteiro.")
            parser.success = False
    else:
        print("Erro: Variável não definida.")
        parser.success = False

#----------------------------------------
def p_error(p):
    print('Syntax error: ', p)
    parser.success = False

#----------------------------------------
#inicio do Parser
parser = yacc.yacc()

parser.success = True
parser.registers = {}
parser.labels = 0
parser.gp = 0
parser.ints = []
parser.assembly = ""

try:
    if len(sys.argv) > 1:
        with open(sys.argv[1],'r') as file:
            inp = file.read()
            parser.parse(inp)
            if parser.success:
                if len(sys.argv) > 2:
                    with open(sys.argv[2], 'w') as output:
                        output.write(parser.assembly)
                        print("--------------------------------------")
                        print(f"Ficheiro {sys.argv[1]} compilado com sucesso.\nOutput guardado em {sys.argv[2]}.")
                        print("--------------------------------------")
                else:
                    print(parser.assembly)
            else:
                print("--------------------------------------")
                print("Erro ao compilar.")
                print("--------------------------------------")
    else:
        for line in sys.stdin:
            parser.success = True
            parser.registers = {}
            parser.labels = 0
            parser.gp = 0
            parser.ints = []
            parser.assembly = ""
            parser.parse(line)
            if parser.success:
                print("--------------------------------------")
                print(parser.assembly)
                print("--------------------------------------")
            else:
                print("--------------------------------------")
                print("Erro ao compilar.")
                print("--------------------------------------")
except KeyboardInterrupt:
    print()
