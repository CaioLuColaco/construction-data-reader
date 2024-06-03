import os
import glob
import PyPDF2
import csv

nao_processados_path = "nao_processados"
processados_path = "processados"
planilhas_path = "planilhas"

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
        pdfData = get_data_pdf(arquivo)
        
        parsedData = parseData(pdfData)

        buildCSV(parsedData, arquivo)

        moverArquivo(arquivo)

def moverArquivo(arquivo):
      origem_arquivo = os.path.abspath(arquivo)
      destino_arquivo = os.path.abspath(f"{processados_path}/{arquivo.replace(f'{nao_processados_path}', '')}")
      os.rename(origem_arquivo, destino_arquivo)

def get_data_pdf(arquivo):
    pdf_reader = PyPDF2.PdfReader(arquivo)
    allData = []
    for page_num in range(len(pdf_reader.pages)):
            # Obtém o texto da página
            page = pdf_reader.pages[page_num]
            texto_na_pagina = page.extract_text()

            unusedLines = 4
            if page_num == 0:
                 unusedLines = 9

            linhas = texto_na_pagina.splitlines()[unusedLines:]

            for linha in linhas:
                allData.append(linha)

    return allData

def parseData(pdfData):
    dados = [
        ["Cód. Pedido", "Cód. Cliente", "Cliente", "Cód. Produto", "Descr. Produto", "Data", "UND", "Quantidade", "Valor", "Subtotal"]
    ]

    cliente = ""
    pedido = ""
    dataPedido = ""
    codItem = ""
    numCliente = ""
    for line in pdfData:
        if "Totais:" in line or "Total" in line:
            continue

        if "CLIENTE" in line:
            numCliente = line.replace("CLIENTE:", "")[0:6]
            cliente = line.replace("CLIENTE:", "")[6:]
            continue

        lineSplited = line.split(" ")

        if "Pedido" in line:
            pedido = lineSplited[0]
            dataPedido = lineSplited[len(lineSplited) - 1]
            continue

        codItem = lineSplited[0]

        produtoNome = ""
        valores = []
        unidade = ""
        verificadorUnidade = False
        for indice, word in enumerate(lineSplited):
            if indice == 0:
                continue

            if is_numero( word.replace(".", "").replace(",", ".") ):
                valores.append(word)
                verificadorUnidade = True
            else:
                if verificadorUnidade:
                    unidade = word
                    break
                produtoNome += word + " "

        dados.append([pedido, numCliente, cliente, codItem, produtoNome, dataPedido, unidade, valores[0], valores[1], valores[2]])

    return dados

def buildCSV(dados, filename):
    nome_arquivo = filename.replace("pdf", "csv")

    with open(f"{planilhas_path}/{nome_arquivo.replace(f'{nao_processados_path}', '')}", mode='w', newline='') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)

        for linha in dados:
            escritor_csv.writerow(linha)

def is_numero(string):
    try:
        float(string)
        if '.' in string: 
            return True   
    except ValueError:
        return False 

init()