# main.py
from scrapping import Scrapper
import csv

def get_ids():
    caminho_arquivo_csv = 'C:\\Users\\kaypi\\Downloads\\Web-Scrapping-Lattes\\id_lattes.csv'
    ids = []
    with open(caminho_arquivo_csv, newline='') as arquivo_csv:
        lattesIDs = list(csv.reader(arquivo_csv))
        for linha in lattesIDs:
            if len(linha) > 0:
                ids.append(linha[0].strip())
    return ids

def main():
    scrapper = Scrapper()
    
    ids = get_ids()
    for id_lattes in ids:
        url = f"http://lattes.cnpq.br/{id_lattes}"
        print(f"\nAcessando: {url}")
        
        scrapper.acessar_lattes(url)
        input("enter depois de resolver captcha")
        foto = scrapper.obter_foto()
        identificacao = scrapper.obter_identificacao()
        endereco = scrapper.obter_endereco()
        formacao = scrapper.obter_demais_infos("FormacaoAcademicaTitulacao")
        formacao_complementar = scrapper.obter_demais_infos("FormacaoComplementar")

        print("=== IDENTIFICAÇÃO ===")
        for campo, valor in identificacao.items():

            print(f"{campo}: {valor}")

        print("\n=== ENDEREÇO ===")
        for campo, valor in endereco.items():
            print(f"{campo}: {valor}")

        print("\n=== URL DA FOTO ===")
        print(foto)
    
        print("\n=== FORMAÇÃO ACADÊMICA ===")
        for ano, informacao in formacao:
            print(f"{ano}: {informacao}")
            print("\n")
        
        print("\n=== FORMAÇÃO COMPLEMENTAR ===")
        for ano, informacao in formacao_complementar:
            print(f"{ano}: {informacao}")
            print("\n")
            
    scrapper.fechar_browser()

if __name__ == "__main__":
    main()