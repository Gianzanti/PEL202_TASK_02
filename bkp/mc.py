import queue

Estado = dict[str, int]
Acao = dict[str, int]

class MissionariosCanibais():

    def __init__(self, tamGrupo:int = 3) -> None:
        # define o tamanho total de cada um dos grupos
        self.tamGrupo = tamGrupo
        
        # define a margem inicial do barco, 0 para esquerda e 1 para direita
        self.estadoInicial = {
            "missionarios": tamGrupo,
            "canibais": tamGrupo,
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
        return f"{estado} => ESQ: {estado['missionarios']}M {estado['canibais']}C | DIR: {self.tamGrupo - estado['missionarios']}M {self.tamGrupo - estado['canibais']}C | Barco: {barco}"

    def acaoValida(self, estado:Estado, mover:Acao) -> bool:
        # existe ao menos um tripulante no barco e no máximo 2:
        tripulantes = mover['missionarios'] + mover['canibais']
        if (tripulantes <= 0) or (tripulantes > 2):
            return False
        
        if mover['sentido'] == estado['barco']:
            return False

        if mover['sentido'] == 1:
            totalMissionarios = estado['missionarios']
            totalCanibais = estado['canibais']

            # a quantidade de missionarios é maior ou igual a quantidade de canibais na margem esquerda:
            qtdMissionariosOK = estado['missionarios'] - mover['missionarios'] >= estado['canibais'] - mover['canibais']

        elif mover['sentido'] == 0:
            totalMissionarios = self.tamGrupo - estado['missionarios']
            totalCanibais = self.tamGrupo - estado['canibais']

            # a quantidade de missionarios é maior ou igual a quantidade de canibais na margem direita:
            qtdMissionariosOK = estado['missionarios'] + mover['missionarios'] >= estado['canibais'] + mover['canibais']

        # missionarios a serem movidos é menor ou igual que o missionarios restantes na margem:
        if mover['missionarios'] > totalMissionarios:
            return False

        # canibais a serem movidos é menor ou igual que o canibais restantes na margem:
        if mover['canibais'] > totalCanibais:
            return False
        
        if qtdMissionariosOK:
            return True
        
        return False

    def gerarAcoes(self, estado:Estado, key: str) -> list[Acao]:
        acoes:list[dict[str, int]] = []
        for missionarios in range(self.tamGrupo):
            for canibais in range(self.tamGrupo):
                for margens in range(2):
                    mover = {
                        "missionarios": missionarios,
                        "canibais": canibais,
                        "sentido": margens
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
        print(f"Estado inicial {estado}")

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

        if printInfo: 
            print(f'Ação: {mover} | Final: {estado}')
        return estado

def testarAcoes():
    missao = MissionariosCanibais()
    estado = missao.estadoInicial
    acoes = missao.acoesDisponiveis(estado)
    print(f"Ações disponiveis para {estado}: {acoes}")

    for acao in acoes:
        missao.executarAcao(estado.copy(), acao)

def buscaProfundidade(): # Busca em Profundidade (Depth-First Search - DFS)
    # lista de estados/acoes já analisados
    estadosAnalisados: dict[str, bool] = {}

    # inicia o problema, já com a situação inicial definida bem como a situação final
    missao = MissionariosCanibais()

    # pega primeira acao disponível
    acoes = missao.acoesDisponiveis(missao.estadoInicial)
    # print(f"Ações disponiveis para {missao.estadoInicial}: {acoes}")
    acaoInicial = acoes[0]

    def dfs(estadoAtual, acaoAtual):
        keyState = f"{estadoAtual['missionarios']}_{estadoAtual['canibais']}_{estadoAtual['barco']}"
        keyAction = f"{acaoAtual['missionarios']}_{acaoAtual['canibais']}_{acaoAtual['sentido']}"

        # checa se o estado atual já foi analisado
        if keyState in estadosAnalisados:
            if keyAction in estadosAnalisados[keyState]:
                # print("Estado/Ação já analisado", [estadoAtual, acaoAtual])
                return False
            else:
                estadosAnalisados[keyState][keyAction] = False
        else:
            estadosAnalisados[keyState] = {keyAction: False}
        
        # executa a ação
        estadoAtual = missao.executarAcao(estadoAtual.copy(), acaoAtual)
        
        # checa se a missao foi concluída
        if estadoAtual == missao.estadoFinal:
            estadosAnalisados[keyState][keyAction] = True
            return True
        
        # pega as ações disponíveis
        acoes = missao.acoesDisponiveis(estadoAtual)
        # print(f"Ações disponiveis para {estadoAtual}: {acoes}")

        for acao in acoes:
            if dfs(estadoAtual, acao):
                # keyState = f"{estadoAtual['missionarios']}_{estadoAtual['canibais']}_{estadoAtual['barco']}"
                # keyAction = f"{acao['missionarios']}_{acao['canibais']}_{acao['sentido']}"
                # estadosAnalisados[keyState][keyAction] = True
                return True
        
        print(f"Executei todas as ações possíveis para {estadoAtual} e não achei a resposta!")
            
        

    # executa a busca em profundidade
    if dfs(missao.estadoInicial, acaoInicial):
        print("********************* Missão concluída! *********************")
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

def buscaLargura(): # Busca em Largura (Breadth-First Search - BFS)
    # lista de estados/acoes já analisados
    estadosAnalisados: dict[str, dict[str, tuple[Estado | None, Acao | None]]] = {}

    # inicia o problema, já com a situação inicial definida bem como a situação final
    missao = MissionariosCanibais()

    # pega as acoes disponíveis
    acoes = missao.acoesDisponiveis(missao.estadoInicial)
    
    # print(f"Ações disponiveis para {missao.estadoInicial}: {acoes}")
    acaoInicial = acoes[0]

    # checa se o estado atual já foi analisado
    keyState = f"{missao.estadoInicial['missionarios']}_{missao.estadoInicial['canibais']}_{missao.estadoInicial['barco']}"
    keyAction = f"{acaoInicial['missionarios']}_{acaoInicial['canibais']}_{acaoInicial['sentido']}"

    estadosAnalisados[keyState] = {keyAction: (None, None)}

    def bfs(estadoAtual, acaoAtual):
        # fila de estados/acoes a serem analisados
        estadosAcoesFila: queue.Queue[tuple[Estado, Acao]] = queue.Queue()
        estadosAcoesFila.put((estadoAtual, acaoAtual))
        
        while not estadosAcoesFila.empty():
            estadoAtual, acaoAtual = estadosAcoesFila.get()
            
            # executa a ação
            estadoAtual = missao.executarAcao(estadoAtual.copy(), acaoAtual)
            
            # checa se a missao foi concluída
            if estadoAtual == missao.estadoFinal:
                return True
            
            # pega as ações disponíveis
            acoes = missao.acoesDisponiveis(estadoAtual)

            for acao in acoes:
                keyState = f"{estadoAtual['missionarios']}_{estadoAtual['canibais']}_{estadoAtual['barco']}"
                keyAction = f"{acao['missionarios']}_{acao['canibais']}_{acao['sentido']}"

                # checa se o estado atual já foi analisado
                if keyState in estadosAnalisados:
                    if keyAction in estadosAnalisados[keyState]:
                        # print("Estado/Ação já analisado", [estadoAtual, acaoAtual])
                        continue
                    else:
                        estadosAnalisados[keyState][keyAction] = (estadoAtual, acao)
                else:
                    estadosAnalisados[keyState] = {keyAction: (estadoAtual, acao)}
                
                estadosAcoesFila.put((estadoAtual, acao))


    # executa a busca em profundidade
    if bfs(missao.estadoInicial, acaoInicial):
        print("********************* Missão concluída! *********************")
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
    # buscaLargura()
    buscaProfundidade()
    # testarAcoes()