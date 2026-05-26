import csv
import os

class SaveCSV:
    #teste
    def __init__(self, caminho_saida: str = "resultado_lattes.csv"):
        self.caminho_saida = caminho_saida
        self.cabecalho_escrito = os.path.exists(caminho_saida)

    #teste
    def montar_linha(self, foto, identificacao, endereco, formacao, formacao_complementar, atuacao):
        linha = {
            "foto": foto or "",
            "nome": identificacao.get("nome", ""),
            "nome_citacoes": identificacao.get("nome_citacoes", ""),
            "pais_nascimento": identificacao.get("pais_nascimento", ""),
            "endereco": endereco.get("endereco", ""),
            "formacao_academica": self._serializar_lista(formacao),
            "formacao_complementar": self._serializar_lista(formacao_complementar),
            "atuacao_profissional": self._serializar_lista(atuacao),
        }
        return linha

    #teste
    def serializar_lista(self, lista: list) -> str:
        return " | ".join(f"{ano}: {info}" for ano, info in lista) if lista else ""

    #teste
    def salvar(self, foto, identificacao, endereco, formacao, formacao_complementar, atuacao):
        linha = self.montar_linha(foto, identificacao, endereco, formacao, formacao_complementar, atuacao)

        with open(self.caminho_saida, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=linha.keys())

            if not self.cabecalho_escrito:
                writer.writeheader()
                self.cabecalho_escrito = True

            writer.writerow(linha)

        print("[CSV] Salvo")