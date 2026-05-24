from selenium.webdriver.common.by import By
from browser import iniciar_browser
import time

class Scrapper:
    def __init__(self):
        self.driver = iniciar_browser()
        self.driver.implicitly_wait(25)

    def acessar_lattes(self, url):
        self.driver.get(url)
        time.sleep(2)

    def obter_valor_por_label(self, label: str, secao: str = None) -> str:
        try:
            if secao:
                prefixo = (
                    f'//a[@name="{secao}"]/ancestor::div[contains(@class,"title-wrapper")]'
                    f'/following-sibling::div[contains(@class,"data-cell")]'
                )
            else:
                prefixo = ''

            valor = self.driver.find_element(
                By.XPATH,
                f"{prefixo}//b[contains(text(), \"{label}\")]"
                "/ancestor::div[contains(@class,\"layout-cell-3\")]"
                "/following-sibling::div[contains(@class,\"layout-cell-9\")]"
            ).text.strip()
            return valor
        except Exception as e:
            print(f"  [AVISO] Label '{label}' não encontrado: {e}")
            return None
    
    def obter_foto(self):
        try:
            elemento_foto = self.driver.find_element(By.XPATH,
                '//img[@class="foto"]')
            link_foto = elemento_foto.get_attribute("src")
            return link_foto
        
        except Exception as e:
            print(f"Erro ao obter link da foto: {e}")
            return None
        
    def obter_identificacao(self):
        return {
            "nome": self.obter_valor_por_label("Nome"),
            "nome_citacoes": self.obter_valor_por_label("Nome em cita"),
            "pais_nascimento": self.obter_valor_por_label("País de Nacionalidade"),
        }
    
    def obter_endereco(self):
        return {
            "endereco": self.obter_valor_por_label("Endereço Profissional")
        }
    
    def obter_demais_infos(self, secao: str):
        formacao = []
        try:
            if self.driver.find_elements(By.XPATH, f'//a[@name="{secao}"]'):
                print(secao, " encontrada")

                anos = self.driver.find_elements(
                By.XPATH,
                f'//a[@name="{secao}"]/../div[contains(@class,"data-cell")]//div[contains(@class,"layout-cell-3")]//div[contains(@class,"layout-cell-pad-5")]//b'
                )

                informacoes = self.driver.find_elements(
                    By.XPATH,
                    f'//a[@name="{secao}"]/../div[contains(@class,"data-cell")]//div[contains(@class,"layout-cell-9")]//div[contains(@class,"layout-cell-pad-5")]'
                )

            #print(f"[DEBUG] Anos encontrados: {len(anos)}")
            #print(f"[DEBUG] Informações encontradas: {len(informacoes)}")

            for ano, info in zip(anos, informacoes):
                chave = ano.text.strip()
                valor = info.text.strip()
                if chave and valor:
                    formacao.append((chave, valor))
                else:
                    print(secao, " não encontrado")

        except Exception as e:
            print(f"Erro ao obter informação: {e}")

        return formacao

    def fechar_browser(self):
        self.driver.quit()