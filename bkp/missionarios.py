# classe representando o problema dos missionarios e canibais

class MissionariosCanibais():
    def __init__(self, tamGrupo = 3, margemInicial = 0) -> None:
        # define o tamanho total de cada um dos grupos
        self.tamGrupo = tamGrupo
        
        # define a margem inicial do barco, 0 para esquerda e 1 para direita
        self.estadoInicial = [tamGrupo, tamGrupo, margemInicial]

        self.estadoInicial2 = {
            "missionarios": tamGrupo,
            "canibais": tamGrupo,
            "barco": margemInicial
        }

        # define o estado final do problema
        margemFinal = 1 if margemInicial == 0 else 0
        self.estadoFinal = [0, 0, margemFinal]
        
        self.estadoFinal2 = {
            "missionarios": 0,
            "canibais": 0,
            "barco": 1 if margemInicial == 0 else 0
        }

    def reprEstado(self, estadoAtual:list[int]) -> str:
        mE = estadoAtual[0]
        cE = estadoAtual[1]
        mD = self.tamGrupo - mE
        cD = self.tamGrupo - cE
        barco = "esquerda" if estadoAtual[2] == 0 else "direita"
        return f"{estadoAtual} => ESQ: {mE}M {cE}C | DIR: {mD}M {cD}C | Barco: {barco}"

    def acaoValida(self, estado:list[int], acao:list[int]) -> bool:
        missionarios = estado[0]
        canibais = estado[1]
        barco = estado[2]

        moverMissionarios = acao[0]
        moverCanibais = acao[1]
        sentido = acao[2]

        movMissionarios = False
        movCanibais = False
        qtdMissionariosOK = False

        if sentido == 1 and barco == 0:
            # grupo de missionarios a serem movidos é menor ou igual que o grupo de missionarios restantes na margem esquerda(0):
            movMissionarios = moverMissionarios <= missionarios
            
            # grupo de canibais a serem movidos é menor ou igual que o grupo de canibais restantes na margem esquerda(0):
            movCanibais = moverCanibais <= canibais

            # a quantidade de missionarios é maior ou igual a quantidade de canibais na margem esquerda:
            qtdMissionariosOK = missionarios - moverMissionarios >= canibais - moverCanibais

        elif sentido == 0 and barco == 1:
            # grupo de missionarios a serem movidos é menor ou igual que o grupo de missionarios restantes na margem direita(1):
            movMissionarios = moverMissionarios <= self.tamGrupo - missionarios

            # grupo de canibais a serem movidos é menor ou igual que o grupo de canibais restantes na margem direita(1):
            movCanibais = moverCanibais <= self.tamGrupo - canibais

            # a quantidade de missionarios é maior ou igual a quantidade de canibais na margem direita:
            qtdMissionariosOK = missionarios + moverMissionarios >= canibais + moverCanibais

        # existe ao menos um tripulante no barco e no máximo 2:
        tripulantes = moverMissionarios + moverCanibais > 0 and moverMissionarios + moverCanibais <= 2

        return movMissionarios and movCanibais and tripulantes and qtdMissionariosOK

    def acoesDisponiveis(self, estado:list[int]):
        acoes:list[list[int]] = []
        for missionarios in range(self.tamGrupo):
            for canibais in range(self.tamGrupo):
                for margens in range(2):
                    acao = [missionarios, canibais, margens]
                    if self.acaoValida(estado, acao):
                        acoes.append(acao)
        
        return acoes

    def executarAcao(self, estadoAtual:list[int], acao:list[int], printInfo:bool = True):
        missionarios = estadoAtual[0]
        canibais = estadoAtual[1]
        barco = estadoAtual[2]

        moverMissionarios = acao[0]
        moverCanibais = acao[1]
        sentido = acao[2]

        # if printInfo: 
        #     print('Estado Inicial:', self.reprEstado(estadoAtual))
        
        if barco == 1 and sentido == 0:
            missionarios += moverMissionarios
            canibais += moverCanibais
            barco = 0
            # if printInfo: 
            #     print(f"Ação {acao} => Movendo {acao[0]} missionários e {acao[1]} canibais para a margem esquerda")

        elif barco == 0 and sentido == 1:
            missionarios -= moverMissionarios
            canibais -= moverCanibais
            barco = 1
            # if printInfo: 
            #     print(f"Ação {acao} => Movendo {acao[0]} missionários e {acao[1]} canibais para a margem direita")
        else:
            if printInfo: 
                print(f"Ação {acao} => inválida")

        estadoAposAcao = [missionarios, canibais, barco]
        # if printInfo: 
        #     print('Estado Final:', self.reprEstado(estadoAposAcao))

        if printInfo: 
            print(f'Inicial: {estadoAtual} | Ação: {acao} | Final: {estadoAposAcao}')
        return estadoAposAcao



# Busca em Profundidade (Depth-First Search - DFS)

def main():
    # lista de estados/acoes já analisados
    estadosAnalisados:list[list[int]] = []

    # inicia o problema, já com a situação inicial definida bem como a situação final
    missao = MissionariosCanibais()

    # pega primeira acao disponível
    acoes = missao.acoesDisponiveis(missao.estadoInicial)
    # print(f"Ações disponiveis para {missao.estadoInicial}: {acoes}")
    acaoInicial = acoes[0]

    def dfs(estadoAtual, acaoAtual):
        # checa se o estado atual já foi analisado
        if [estadoAtual, acaoAtual] in estadosAnalisados:
            # print("Estado/Ação já analisado", [estadoAtual, acaoAtual])
            return False

        # adiciona o estado atual na lista de estados analisados
        estadosAnalisados.append([estadoAtual, acaoAtual])

        # executa a ação
        estadoAtual = missao.executarAcao(estadoAtual, acaoAtual)
        
        # checa se a missao foi concluída
        if estadoAtual == missao.estadoFinal:
            return True
        
        # pega as ações disponíveis
        acoes = missao.acoesDisponiveis(estadoAtual)
        # print(f"Ações disponiveis para {estadoAtual}: {acoes}")

        for acao in acoes:
            if dfs(estadoAtual, acao):
                return True

    # executa a busca em profundidade
    if dfs(missao.estadoInicial, acaoInicial):
        print("********************* Missão concluída! *********************")
        print("Estados/acoes analisados: ", estadosAnalisados)

        # Exibe o caminho percorrido percorrendo os estados/acoes analisados reversamente
        lastEstado = None
        caminho = []

        for estadoAcao in reversed(estadosAnalisados):
            if (lastEstado == None):
                lastEstado = estadoAcao[0]
                caminho.append([estadoAcao[0], estadoAcao[1], missao.executarAcao(estadoAcao[0], estadoAcao[1], False)])
                continue
            
            if missao.executarAcao(estadoAcao[0], estadoAcao[1], False) == lastEstado:
                 lastEstado = estadoAcao[0]
                 caminho.append([estadoAcao[0], estadoAcao[1], missao.executarAcao(estadoAcao[0], estadoAcao[1], False)])
                 if estadoAcao[0] == missao.estadoInicial and estadoAcao[1] == acaoInicial:
                     break
            
        caminho.reverse()
        print("Caminho percorrido:")
        for estadoAcao in caminho:
            print(f'Estado: {estadoAcao[0]} | Ação: {estadoAcao[1]} | Estado Final: {estadoAcao[2]}')

    



if __name__ == "__main__":
    main()