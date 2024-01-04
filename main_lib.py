import os
import click
import configparser
import ml_lib
from pdf_lib import PdfUtils
import multiprocessing

#  This is a tool created to help debug our SAA Python scripts.
#  Copyright (C) 2023 João Pedro de S. T. Costa and NOV Flexibles;



path = ''

# ------------------------------------------CLI to debug  ----------------------------------------------- #
def run_function(filename):
    """
    Executa uma função no arquivo especificado.
    Args:
        nome_do_arquivo (str): O nome do arquivo para executar a função.
    """
    print(f"Executando script em: {filename}")

    # pdf to image algorithm

    instance = PdfUtils(filename)
    instance.get_text()
    drawings = instance.get_possible_drwaings()
    combinedimage = instance.create_combined_image(drawings,save=True)
    instance.construct_DWG_image(combinedimage)

    # finished image construction algorithm

    # ---------- trial one: use ml_lib and DETR_RESNET101 ----------- #
    model_instance = ml_lib.MODEL_FACEBOOK_DETR_RESNET_101(instance)
    model_instance.run()


def update_project_path():
    """
    Atualiza o caminho do projeto no arquivo de configuração.
    Este método recupera o diretório de trabalho atual e atualiza o caminho do projeto no arquivo de configuração
    com o diretório de trabalho atual anexado ao nome do projeto. O arquivo de configuração está no formato INI.
    :return: None
    """
    diretorio_atual = os.getcwd()
    config = configparser.ConfigParser()
    config["DEFAULT"] = {"PROJECT_PATH": os.path.join(diretorio_atual, "bs_top")}
    with open("config.txt", "w") as arquivo_config:
        config.write(arquivo_config)

def process_directory(path, prefix=""):
    """
    Processa o diretório e retorna uma lista de arquivos dentro do diretório e subdiretórios.
    Args:
        caminho: Uma string representando o caminho para o diretório.
        prefixo: Uma string opcional representando o prefixo a ser adicionado aos nomes dos arquivos.
    Retorna:
        Uma lista de nomes de arquivos dentro do diretório e subdiretórios, com o prefixo especificado adicionado.
        Se o diretório não existir, uma lista vazia é retornada.
    """
    try:
        entradas = os.listdir(path)
    except FileNotFoundError:
        print(f"Diretório não encontrado: {path}")
        return []
    arquivos = []
    for entrada in entradas:
        if entrada == "venv":
            continue
        caminho_completo = os.path.join(path, entrada)
        if os.path.isfile(caminho_completo):
            arquivos.append(f"{prefix}{entrada}")
        elif os.path.isdir(caminho_completo):
            arquivos.extend(process_directory(caminho_completo, prefix=f"{prefix}{entrada}/"))
    return arquivos

def run_for_all_files(num_files):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(run(), range(1, num_files+1))
@click.command()
def run():
    """
    Método de Execução
    Este método é usado para executar uma série de ações para executar uma função específica em um arquivo selecionado.
    Retorna:
        None
    Exemplo:
        >>> executar()
    """
    update_project_path()
    config = configparser.ConfigParser()
    config.read('config.txt')
    caminho_projeto = config.get('DEFAULT', 'project_path')
    if not os.path.exists(caminho_projeto):
        print(f"Diretório não encontrado: {caminho_projeto}")
        return
    print(f"Procurando arquivos em {caminho_projeto}")
    arquivos = sorted(process_directory(caminho_projeto))
    for i, arquivo in enumerate(arquivos, 1):
        print(f"{i}. {arquivo}")
    numero_arquivo = click.prompt('Digite o número do arquivo', type=int)
    if numero_arquivo < 1 or numero_arquivo > len(arquivos):
        print("Número de arquivo inválido!")
        return
    arquivo_selecionado = arquivos[numero_arquivo - 1]
    print(f"Arquivo selecionado: {arquivo_selecionado}")
    arquivo_selecionado = os.path.join(caminho_projeto, arquivos[numero_arquivo - 1])
    run_function(arquivo_selecionado)
    return path


path = run()

# ----------------------------------------------------------------------------------------------------- #
