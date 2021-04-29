from robos import robo_state

def ask_termo_busca():
    '''
    funcao que pergunta e retorna o termo de busca informado pelo usuário
    '''
    return input('\nInforme o termo de busca a ser pesquisado na wikipedia: ')

def ask_prefixo():
    prefixos = ['Quem é', 'O que é', 'A história de']
    return key_in_select(prefixos, 'Escolha uma opção: ') 
    

def key_in_select(arr, msg):
    '''
    mostra um array de opcoes no console
        arr - array com as opcoes
        msg - mensagem
    '''
    print('\n')
    [print(f'[{idx}] {opt}') for idx, opt in enumerate(arr)]

    opt = None

    try:
        opt = int(input(f'\n{msg}'))
    except:
        print('É esperado um número')
        return 

    if opt < 0 or opt > len(arr) -1 :
        print('Índice fora do valor esperado')
        return

    return arr[opt]

def init(contexto):
    contexto.set_termo_busca(ask_termo_busca())
    contexto.set_prefixo(ask_prefixo())

    robo_state.save(contexto)