from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser import iniciar_browser

class Scrapper:
    def __init__(self):
        self.driver = iniciar_browser()
        self.wait = WebDriverWait(self.driver, 10)

    def acessar_lattes(self, url):
        self.driver.get(url)
        # Aguarda a página carregar completamente
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//a[@name="Identificacao"]')))

    def _texto_seguro(self, xpath):
        """Tenta pegar o texto de um elemento, retorna None se não encontrar."""
        try:
            return self.driver.find_element(By.XPATH, xpath).text.strip()
        except:
            return None

    def obter_identificacao(self):
        """
        A seção de identificação fica dentro de:
        <a name="Identificacao"> ... </a>
        
        Os campos seguem o padrão de grid:
        - layout-cell-3 text-align-right → label (ex: "Nome em citações bibliográficas")
        - layout-cell-9                  → valor (ex: "MIRANDA FILHO, R.;...")
        
        Para pegar o NOME do pesquisador, ele fica dentro de um <h2> ou <div>
        logo após o <a name="Identificacao">.
        
        Para campos como "Nome em citações" e "País de nascimento", usamos o
        seguinte truque XPath:
          1. Achamos o <div> que contém o texto do label
          2. Subimos para o pai (../..)
          3. Pegamos a coluna ao lado (layout-cell-9)
        """

        # NOME: fica num elemento próprio logo após a âncora Identificacao
        nome = self._texto_seguro(
            '//a[@name="Identificacao"]/following-sibling::div[contains(@class,"title-wrapper")]//h2'
        )

        # NOME EM CITAÇÕES BIBLIOGRÁFICAS
        # Lógica: acha o <b> com o texto do label → sobe para o pai (layout-cell-pad-5)
        # → sobe mais um (layout-cell-3) → pega o irmão seguinte (layout-cell-9)
        nome_citacoes = self._texto_seguro(
            '//b[contains(text(),"Nome em cita")]'      # acha o label
            '/ancestor::div[contains(@class,"layout-cell-3")]'  # sobe até a coluna label
            '/following-sibling::div[contains(@class,"layout-cell-9")]'  # pega a coluna valor
        )

        # PAÍS DE NASCIMENTO — mesma lógica, texto do label diferente
        pais_nascimento = self._texto_seguro(
            '//b[contains(text(),"País de nascimento")]'
            '/ancestor::div[contains(@class,"layout-cell-3")]'
            '/following-sibling::div[contains(@class,"layout-cell-9")]'
        )

        return {
            "nome": nome,
            "nome_citacoes": nome_citacoes,
            "pais_nascimento": pais_nascimento,
        }

    def obter_endereco_profissional(self):
        """
        A seção fica após <a name="EnderecosProfissionais">.
        Mesma lógica de grid: label na col-3, valor na col-9.
        """

        # Instituição (geralmente o primeiro campo da seção)
        instituicao = self._texto_seguro(
            '//a[@name="EnderecosProfissionais"]'
            '/ancestor::div[contains(@class,"title-wrapper")]'
            '/following-sibling::div[contains(@class,"data-cell")]'
            '//b[contains(text(),"Instituição")]'
            '/ancestor::div[contains(@class,"layout-cell-3")]'
            '/following-sibling::div[contains(@class,"layout-cell-9")]'
        )

        # Endereço completo
        endereco = self._texto_seguro(
            '//a[@name="EnderecosProfissionais"]'
            '/ancestor::div[contains(@class,"title-wrapper")]'
            '/following-sibling::div[contains(@class,"data-cell")]'
            '//b[contains(text(),"Endereço")]'
            '/ancestor::div[contains(@class,"layout-cell-3")]'
            '/following-sibling::div[contains(@class,"layout-cell-9")]'
        )

        return {
            "instituicao": instituicao,
            "endereco": endereco,
        }

    def obter_formacao_academica(self):
        """
        Formação acadêmica fica em <a name="FormacaoAcademicaTitulacao">.
        Cada curso é um bloco separado dentro da seção.
        Aqui iteramos sobre todos os blocos e extraímos os dados de cada um.
        """
        formacoes = []

        try:
            # Pega todos os blocos de formação (cada <div class="layout-cell layout-cell-12 data-cell">
            # dentro da seção de formação)
            secao = self.driver.find_element(
                By.XPATH,
                '//a[@name="FormacaoAcademicaTitulacao"]/ancestor::div[contains(@class,"title-wrapper")]'
                '/following-sibling::div[contains(@class,"data-cell")]'
            )

            # Dentro da seção, cada formação é um novo bloco de dados
            blocos = secao.find_elements(By.XPATH, './/div[contains(@class,"layout-cell-9")]')

            for bloco in blocos:
                texto = bloco.text.strip()
                if texto:
                    formacoes.append(texto)

        except Exception as e:
            print(f"Erro ao obter formação acadêmica: {e}")

        return formacoes

    def obter_todas_informacoes(self):
        return {
            "identificacao": self.obter_identificacao(),
            "endereco_profissional": self.obter_endereco_profissional(),
            "formacao_academica": self.obter_formacao_academica(),
        }

    def fechar_browser(self):
        self.driver.quit()