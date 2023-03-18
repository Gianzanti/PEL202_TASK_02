import queue
import heapq

Estado = dict[str, int]
Acao = dict[str, int]

class MCProblem():

    def __init__(self, groupSize:int = 3) -> None:
        # defines the total size of each group (Missionaire or Cannibals)
        self.groupSize = groupSize
        
        # define a margem inicial do barco, 0 para esquerda e 1 para direita
        self.estadoInicial = {
            "missionarios": groupSize,
            "canibais": groupSize,
            "barco": 0
        }

        # define o estado final do problema
        self.estadoFinal = {
            "missionarios": 0,
            "canibais": 0,
            "barco": 1
        }

        self.acoes:dict[str, list[dict[str, int]]] = {}

        self.acoesRealizadas = 0

    def reprEstado(self, estado:Estado) -> str:
        barco = "esquerda" if estado['barco'] == 0 else "direita"
        return f"{estado} => ESQ: {estado['missionarios']}M {estado['canibais']}C | DIR: {self.groupSize - estado['missionarios']}M {self.groupSize - estado['canibais']}C | Barco: {barco}"

    def acaoValida(self, estado:Estado, mover:Acao) -> bool:
        # existe ao menos um tripulante no barco e no máximo 2:
        tripulantes = mover['missionarios'] + mover['canibais']
        if (tripulantes <= 0) or (tripulantes > 2):
            # print(f"Falha na tripulação: {tripulantes}")
            return False
        
        if mover['sentido'] == estado['barco']:
            # print(f"Falha no sentido da movimentação: {mover['sentido']}")
            return False

        if mover['sentido'] == 1:
            margem_Esq_M = estado['missionarios'] - mover['missionarios']
            margem_Dir_M = (self.groupSize - estado['missionarios']) + mover['missionarios']
            margem_Esq_C = estado['canibais'] - mover['canibais']
            margem_Dir_C = (self.groupSize - estado['canibais']) + mover['canibais']


        elif mover['sentido'] == 0:
            margem_Esq_M = estado['missionarios'] + mover['missionarios']
            margem_Dir_M = (self.groupSize - estado['missionarios']) - mover['missionarios']
            margem_Esq_C = estado['canibais'] + mover['canibais']
            margem_Dir_C = (self.groupSize - estado['canibais']) - mover['canibais']

        # missionarios a serem movidos é menor ou igual que o missionarios restantes na margem:
        if margem_Esq_M < 0 or margem_Dir_M < 0:
            # print(f"Falha na quantidade de missionários: Esq: {margem_Esq_M} | Dir: {margem_Dir_M}")
            return False
        
        if margem_Esq_C < 0 or margem_Dir_C < 0:
            # print(f"Falha na quantidade de canibais: Esq: {margem_Esq_C} | Dir: {margem_Dir_C}")
            return False

        # não pode haver mais canibais que missionários em qualquer margem:       
        if (margem_Esq_M == 0 or margem_Esq_M >= margem_Esq_C) and (margem_Dir_M == 0 or margem_Dir_M >= margem_Dir_C):
            return True
        
        # print(f"Os canibais comem os missionários: Esq: {margem_Esq_M}M {margem_Esq_C}C | Dir: {margem_Dir_M}M {margem_Dir_C}C")
        return False

    def gerarAcoes(self, estado:Estado, key: str) -> list[Acao]:
        acoes:list[dict[str, int]] = []
        for missionarios in range(self.groupSize):
            for canibais in range(self.groupSize):
                for margens in range(2):
                    mover = {
                        "missionarios": missionarios,
                        "canibais": canibais,
                        "sentido": margens,
                        "custo": 1,
                        "heuristica": 0,
                    }
                    if self.acaoValida(estado, mover):
                        acoes.append(mover)
        
        self.acoes[key] = acoes
        return acoes

    def acoesDisponiveis(self, estado:Estado) -> list[Acao]:
        key = f"{estado['missionarios']}_{estado['canibais']}_{estado['barco']}"

        if (key in self.acoes):
            return self.acoes[key]
        
        return self.gerarAcoes(estado, key)

    def executarAcao(self, estado:Estado, mover:Acao, printInfo:bool = True) -> Estado:
        # print(f"Estado inicial {estado}")

        if estado['barco'] == 1 and mover['sentido'] == 0:
            estado['missionarios'] += mover['missionarios']
            estado['canibais'] += mover['canibais']
            estado['barco'] = 0
            self.acoesRealizadas += 1

        elif estado['barco'] == 0 and mover['sentido'] == 1:
            estado['missionarios'] -= mover['missionarios']
            estado['canibais'] -= mover['canibais']
            estado['barco'] = 1
            self.acoesRealizadas += 1

        else:
            if printInfo: 
                print(f"Ação {mover} => inválida")

        # if printInfo: 
        #     print(f'Ação: {mover} | Final: {estado}')
        return estado

def testarAcoes():
    missao = MCProblem()
    estado = missao.estadoInicial
    acoes = missao.acoesDisponiveis(estado)
    print(f"Ações disponiveis para {estado}: {acoes}")

    for acao in acoes:
        missao.executarAcao(estado.copy(), acao)

def animateResult(path):
    for estado in path:
        LEFT_s = f"__{'M' * estado[0]['missionarios']}{'_' * (5 - estado[0]['missionarios'])}{'C' * estado[0]['canibais']}{'_' * (5 - estado[0]['canibais'])}"
        BOAT_s = f"{'~' * 11}"
        RIGH_s = f"__{'M' * (3 - estado[0]['missionarios'])}{'_' * (2 + estado[0]['missionarios'])}{'C' * (3 - estado[0]['canibais'])}{'_' * (2 + estado[0]['canibais'])}"

        LEFT_m1 = f"__{'M' * estado[2]['missionarios']}{'_' * (5 - estado[2]['missionarios'])}{'C' * estado[2]['canibais']}{'_' * (5 - estado[2]['canibais'])}"
        BOAT_m1 = f"  {'M' * estado[1]['missionarios']}{' ' * (2 - estado[1]['missionarios'])}{'C' * estado[1]['canibais']}{' ' * (2 - estado[1]['canibais'])} ==>>"
        RIGH_m1 = f"__{'M' * (3 - estado[0]['missionarios'])}{'_' * (2 + estado[0]['missionarios'])}{'C' * (3 - estado[0]['canibais'])}{'_' * (2 + estado[0]['canibais'])}"

        LEFT_m2 = f"__{'M' * estado[0]['missionarios']}{'_' * (5 - estado[0]['missionarios'])}{'C' * estado[0]['canibais']}{'_' * (5 - estado[0]['canibais'])}"
        BOAT_m2 = f"<<== {'M' * estado[1]['missionarios']}{' ' * (2 - estado[1]['missionarios'])}{'C' * estado[1]['canibais']}{' ' * (2 - estado[1]['canibais'])}  "
        RIGH_m2 = f"__{'M' * (3 - estado[2]['missionarios'])}{'_' * (2 + estado[2]['missionarios'])}{'C' * (3 - estado[2]['canibais'])}{'_' * (2 + estado[2]['canibais'])}"

        print(f"{LEFT_s} {BOAT_s} {RIGH_s}")

        if estado[1]['sentido'] == 1:
            print(f"{LEFT_m1} {BOAT_m1} {RIGH_m1}\n")
        else:
            print(f"{LEFT_m2} {BOAT_m2} {RIGH_m2}\n")

def buscaProfundidade(): # Busca em Profundidade (Depth-First Search - DFS)
    # lista de estados/acoes já analisados
    estadosAnalisados: dict[str, bool] = {}

    # inicia o problema, já com a situação inicial definida bem como a situação final
    missao = MCProblem()

    path = []

    def dfs(estadoInicial):
        keyState = f"{estadoInicial['missionarios']}_{estadoInicial['canibais']}_{estadoInicial['barco']}"

        # checa se o estado atual já foi analisado
        if keyState in estadosAnalisados:
            return False
        else:
            estadosAnalisados[keyState] = False

        # checa se a missao foi concluída
        if estadoInicial == missao.estadoFinal:
            return True
        
        # pega as ações disponíveis
        acoes = missao.acoesDisponiveis(estadoInicial)

        for acao in acoes:
            estadoAtual = missao.executarAcao(estadoInicial.copy(), acao)
            path.append((estadoInicial, acao, estadoAtual))
            if dfs(estadoAtual):
                estadosAnalisados[keyState] = True
                return True
            else:
                estadosAnalisados[keyState] = False
                path.pop()
        
        # print(f"Executei todas as ações possíveis para {estadoAtual} e não achei a resposta!")
        return False

    # executa a busca em profundidade
    if dfs(missao.estadoInicial):
        print("********************* Missão concluída! *********************")
        # print("Estados/acoes analisados: ", estadosAnalisados)
        # print('Caminho percorrido: ', path)
        print('Acoes realizadas para concluir a missão: ', missao.acoesRealizadas)

        animateResult(path)

def buscaLargura(): # Busca em Largura (Breadth-First Search - BFS)
    # lista de estados/acoes já analisados
    # estadosAnalisados: dict[str, dict[str, tuple[Estado | None, Acao | None]]] = {}
    estadosAnalisados: dict[str, tuple[str | None, Acao | None]] = {}

    # inicia o problema, já com a situação inicial definida bem como a situação final
    missao = MCProblem()

    def bfs(estadoInicial):
        # fila de estados/acoes a serem analisados
        estadosAcoesFila: queue.Queue[Estado] = queue.Queue()
        estadosAcoesFila.put(estadoInicial)
        
        while not estadosAcoesFila.empty():
            estadoAtual = estadosAcoesFila.get()
            keyStateAnterior = f"{estadoAtual['missionarios']}_{estadoAtual['canibais']}_{estadoAtual['barco']}"

            # checa se a missao foi concluída
            if estadoAtual == missao.estadoFinal:
                print("********************* Missão concluída! *********************")
                return keyStateAnterior

            # pega as ações disponíveis
            acoes = missao.acoesDisponiveis(estadoAtual)

            for acao in acoes:
                novoEstado = missao.executarAcao(estadoAtual.copy(), acao)
                keyState = f"{novoEstado['missionarios']}_{novoEstado['canibais']}_{novoEstado['barco']}"

                # checa se o estado atual já foi analisado
                if keyState in estadosAnalisados:
                    continue
                                
                estadosAcoesFila.put(novoEstado)
                estadosAnalisados[keyState] = keyStateAnterior, acao



    # executa a busca em profundidade
    keyState = f"{missao.estadoInicial['missionarios']}_{missao.estadoInicial['canibais']}_{missao.estadoInicial['barco']}"
    estadosAnalisados[keyState] = None, None

    estadoFinal = bfs(missao.estadoInicial)
    print("********************* Missão concluída! *********************")
    print(f"At {estadoFinal}")
    print("Estados/acoes analisados: ", estadosAnalisados)

        # # Exibe o caminho percorrido percorrendo os estados/acoes analisados reversamente
        # lastEstado = None
        # caminho = []

        # for estadoAcao in reversed(estadosAnalisados):
        #     if (lastEstado == None):
        #         lastEstado = estadoAcao[0]
        #         caminho.append([estadoAcao[0], estadoAcao[1], missao.executarAcao(estadoAcao[0], estadoAcao[1], False)])
        #         continue
            
        #     if missao.executarAcao(estadoAcao[0], estadoAcao[1], False) == lastEstado:
        #          lastEstado = estadoAcao[0]
        #          caminho.append([estadoAcao[0], estadoAcao[1], missao.executarAcao(estadoAcao[0], estadoAcao[1], False)])
        #          if estadoAcao[0] == missao.estadoInicial and estadoAcao[1] == acaoInicial:
        #              break
            
        # caminho.reverse()
        # print("Caminho percorrido:")
        # for estadoAcao in caminho:
        #     print(f'Estado: {estadoAcao[0]} | Ação: {estadoAcao[1]} | Estado Final: {estadoAcao[2]}')

if __name__ == "__main__":
    buscaLargura()
    # buscaProfundidade()
    # testarAcoes()