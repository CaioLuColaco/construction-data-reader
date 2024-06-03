import os
import glob
import PyPDF2

nao_processados_path = "nao_processados"
processados_path = "processados"
separados_path = "separados"

def init():
    print('Iniciando leitor de dados...')

    padrao_pdf = os.path.join(nao_processados_path, '*.pdf')
    arquivos_pdf = glob.glob(padrao_pdf)

    if(len(arquivos_pdf) == 0):
        print("Nenhum arquivo para ser processado")
    else:
        processar_arquivos(arquivos_pdf)

def processar_arquivos(arquivos):
    print("Iniciando processador de PDF's")

    for arquivo in arquivos:
        print("Processando arquivo: " + arquivo)
        processar_pdf(arquivo)
        moverArquivo(arquivo)

def moverArquivo(arquivo):
      origem_arquivo = os.path.abspath(arquivo)
      destino_arquivo = os.path.abspath(f"{processados_path}/{arquivo.replace(f'{nao_processados_path}', '')}")
      os.rename(origem_arquivo, destino_arquivo)

def processar_pdf(arquivo):
    pdf_reader = PyPDF2.PdfReader(arquivo)

    for page_num in range(len(pdf_reader.pages)):
            # Obtém o texto da página
            page = pdf_reader.pages[page_num]
            texto_na_pagina = page.extract_text()

            print(texto_na_pagina)

            # linhas = texto_na_pagina.splitlines()
            # nome_linha = linhas[11]

            # # Cria um novo PDF com uma única página
            # nome_final = tratarNome(nome_linha)
            # novo_pdf = f"{separados_path}/{nome_final}.pdf"

            # output = PyPDF2.PdfWriter()
            # output.add_page(pdf_reader.pages[page_num])
            # with open(novo_pdf, "wb") as outputStream:
            #      output.write(outputStream)