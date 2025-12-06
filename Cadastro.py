 
def linha(tam = 42):
    return '-' * tam

def cabecalho(txt):
    print(linha())
    print(txt.center(42))
    print(linha())

def leiaInt(msg):
    while True:
        try:
            n = int(input(msg))
        except (ValueError, TypeError):
            print('ERRO! Por favor digite um número inteiro válido.')
            continue
        except (KeyboardInterrupt):
            print('\nO usuário preferiu não inserir os dados')
            return 0
        else:
            return n

def leiaSenha(msg):
    """Lê a senha e garante que tenha entre 4 e 6 caracteres."""
    while True:
        try:
            senha = str(input(msg)).strip()
            tamanho = len(senha)

            if tamanho == 0:
                print('ERRO! A senha não pode ser vazia.')
                continue

            if tamanho < 4 or tamanho > 6:
                print(f'ERRO! A senha deve ter entre 4 e 6 caracteres. Você digitou {tamanho}.')
                continue

        except (KeyboardInterrupt):
            print('\nO usuário preferiu não inserir a senha.')
            return None 
        else:
            return senha
            
# =======================================================
# FUNÇÕES DE CADASTRO E LOGIN (Novas)
# =======================================================

def cadastrar_usuario():
    """Lê a Matrícula e Senha e salva no arquivo 'usuarios.txt'."""
    cabecalho('NOVO CADASTRO')
    
    # Matrícula é lida como string para aceitar letras ou números
    while True:
        matricula = str(input('Matrícula (texto ou número): ')).strip()
        if len(matricula) > 0:
            break
        print('ERRO! A matrícula não pode ser vazia.')
    
    # Senha é lida e validada pelo tamanho
    senha = leiaSenha('Senha (4 a 6 caracteres): ')
    
    if senha is None: # Se o usuário interromper a leitura da senha
        return 

    # Salva no arquivo no formato MATRICULA;SENHA
    try:
        with open('usuarios.txt', 'a') as arquivo:
            arquivo.write(f'{matricula};{senha}\n')
        print(linha())
        print('Usuário cadastrado com sucesso!')
        
    except Exception as e:
        print(f'ERRO ao cadastrar usuário: {e}')

def logar():
    """Lê a Matrícula e Senha e verifica se existe no 'usuarios.txt'."""
    cabecalho('TELA DE LOGIN')
    
    matricula_login = str(input('Matrícula: ')).strip()
    senha_login = str(input('Senha: ')).strip() # Não precisa da validação de tamanho na hora do login

    if not matricula_login or not senha_login:
        print('ERRO: Matrícula e/ou Senha não podem ser vazias.')
        return False
    
    try:
        with open('usuarios.txt', 'r') as arquivo:
            # O arquivo é lido linha por linha
            for linha_usuario in arquivo:
                # O formato é MATRICULA;SENHA\n. O .strip() remove o \n
                dados = linha_usuario.strip().split(';') 
                
                # Garante que a linha tem os dois campos esperados
                if len(dados) == 2:
                    matricula_cadastrada, senha_cadastrada = dados
                    
                    # Verifica se a Matrícula e a Senha coincidem
                    if matricula_login == matricula_cadastrada and senha_login == senha_cadastrada:
                        print(linha())
                        print(f'Bem-vindo(a), {matricula_login}! Login bem-sucedido.')
                        return True # Login realizado com sucesso!
            
            # Se o loop terminar sem encontrar a conta
            print(linha())
            print('ERRO! Matrícula ou senha incorretas.')
            return False

    except FileNotFoundError:
        print(linha())
        print('ERRO! O arquivo de usuários não existe. Cadastre um usuário primeiro.')
        return False
    except Exception as e:
        print(f'Ocorreu um erro inesperado: {e}')
        return False

# =======================================================
# SISTEMA PRINCIPAL
# =======================================================
def menu(lista):
    cabecalho('MENU PRINCIPAL')
    c = 1
    for i in lista:
        print(f'{c} - {i}')
        c += 1
    print(linha())
    opc = leiaInt('Sua Opção: ')
    return opc

# O programa principal (loop)
while True:
    opcao = menu(['Cadastrar Novo Usuário', 'Fazer Login', 'Sair do Sistema'])
    
    if opcao == 1:
        cadastrar_usuario()
    elif opcao == 2:
        logar()
    elif opcao == 3:
        cabecalho('Saindo do Sistema... Até logo!')
        break
    else:
        print('ERRO! Digite uma opção válida (1, 2 ou 3).')