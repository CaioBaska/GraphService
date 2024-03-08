import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

def processar_arquivo_csv(caminho_arquivo_csv):
    # Carregar o CSV especificando a codificação
    df = pd.read_csv(caminho_arquivo_csv, encoding='utf-8')

    columns_to_convert = ['UMIDADE', 'TEMPERATURA', 'POTASSIO', 'PH', 'NITROGENIO', 'FOSFORO', 'LUMINOSIDADE']

    for column in columns_to_convert:
        df[column] = pd.to_numeric(df[column], errors='coerce')
        df[column] = df[column].fillna(0).astype(int)

    # Ordenar o DataFrame pela coluna de data em ordem decrescente
    df = df.sort_values(by='DataFormatada', ascending=True)

    # Plotar gráficos para cada coluna
    plt.figure(figsize=(15, 15))
    for column in columns_to_convert:
        plt.plot(df['DataFormatada'], df[column], label=column, marker='o')

    # Adicionar rótulos e título
    plt.xlabel('Data')
    plt.ylabel('Valores')
    plt.title('Valores medidos ao longo do Tempo')

    # Adicionar legenda
    plt.legend()

    # Ajustar intervalo nos eixos X e Y
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=15))  # Exibir 10 rótulos no eixo X
    plt.ylim(bottom=0)  # Definir o valor mínimo do eixo Y para 0

    # Rotacionar rótulos no eixo X
    plt.xticks(rotation=45)

    # Salvar o gráfico na área de trabalho
    caminho_grafico = os.path.join(os.path.dirname(caminho_arquivo_csv), 'graficos_variaveis.png')
    plt.savefig(caminho_grafico)
    plt.close()

    return caminho_grafico

def gerar_grafico_completo(caminho_arquivo_csv):
    df = pd.read_csv(caminho_arquivo_csv, encoding='utf-8')

    columns_to_convert = ['UMIDADE', 'TEMPERATURA', 'POTASSIO', 'PH', 'NITROGENIO', 'FOSFORO', 'LUMINOSIDADE']

    for column in columns_to_convert:
        df[column] = pd.to_numeric(df[column], errors='coerce')
        df[column] = df[column].fillna(0).astype(int)

    df = df.sort_values(by='DataFormatada', ascending=True)

    plt.figure(figsize=(15, 15))
    for column in columns_to_convert:
        plt.plot(df['DataFormatada'], df[column], label=column, marker='o')

    plt.xlabel('Data')
    plt.ylabel('Valores')
    plt.title('Valores medidos ao longo do Tempo')

    plt.legend()
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=10))
    plt.ylim(bottom=0)
    plt.xticks(rotation=45)

    caminho_grafico = os.path.join(os.path.dirname(caminho_arquivo_csv), 'grafico_completo.png')
    plt.savefig(caminho_grafico)
    plt.close()

    return caminho_grafico

def enviar_email(from_email, password, to_email, subject, body, anexo_path, anexo_csv):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Adicionar anexo do gráfico
    with open(anexo_path, 'rb') as file:
        attachment = MIMEApplication(file.read(), 'octet-stream')
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(anexo_path))
        message.attach(attachment)

    # Adicionar anexo do arquivo CSV
    with open(anexo_csv, 'rb') as file_csv:
        attachment_csv = MIMEApplication(file_csv.read(), 'octet-stream')
        attachment_csv.add_header('Content-Disposition', 'attachment', filename=os.path.basename(anexo_csv))
        message.attach(attachment_csv)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, message.as_string())

def verificar_e_processar_arquivos(diretorio, from_email, password):
    while True:
        try:
            arquivos = [f for f in os.listdir(diretorio) if f.lower().endswith('.csv')]

            if arquivos:
                print("Arquivos encontrados:")
                for arquivo in arquivos:
                    print(arquivo)

                for arquivo in arquivos:
                    caminho_arquivo_csv = os.path.join(diretorio, arquivo)
                    nome_destinatario = os.path.splitext(arquivo)[0]
                    caminho_grafico_completo = gerar_grafico_completo(caminho_arquivo_csv)

                    # Enviar e-mail com o gráfico completo e o arquivo CSV como anexos
                    subject = "Relatório SmartGreen"
                    body = "Em anexo estão o relatório CSV e o gráfico completo gerado."

                    enviar_email(from_email, password, nome_destinatario, subject, body, caminho_grafico_completo, caminho_arquivo_csv)

                    # Remover arquivo CSV e gráfico após o processamento
                    os.remove(caminho_arquivo_csv)
                    os.remove(caminho_grafico_completo)

            time.sleep(10)

        except Exception as ex:
            print(f"Erro: {ex}")
            time.sleep(60)

# Exemplo de uso:
diretorio_relatorios = r'C:\Users\Caio\Documents\TCC\Python\Relatorios'
from_email = "nuggetsaplaysbr@gmail.com"
password = "kipxirewgfwwifsm"

verificar_e_processar_arquivos(diretorio_relatorios, from_email, password)
