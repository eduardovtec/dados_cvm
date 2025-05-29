from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import pandas as pd
import string


chromedriver_autoinstaller.install()

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

letras = list(string.ascii_uppercase) + [str(n) for n in range(10)]

dados = []

for letra in letras:
    url = f'https://cvmweb.cvm.gov.br/swb/sistemas/scw/cpublica/ciaab/FormBuscaCiaAbOrdAlf.aspx?LetraInicial={letra}'
    driver.get(url)

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//table[@id="dlCiasCdCVM"]')))
    except:
        continue

    linhas = driver.find_elements(By.XPATH, '//table[@id="dlCiasCdCVM"]/tbody/tr')

    for linha in linhas:
        if linha.find_elements(By.TAG_NAME, 'b'):
            continue
        
        colunas = linha.find_elements(By.TAG_NAME, 'td')
        colunas = [col.text.strip() for col in colunas]
        dados.append(colunas)

        print(colunas)

driver.quit()

df = pd.DataFrame(dados, columns=['CNPJ', 'NOME', 'TIPO DE PARTICIPANTE', 'CÓDIGO CVM', 'SITUAÇÃO REGISTRO'])
df.to_excel("dados_cvm.xlsx", index=False)

print('Dados salvos na planilha')