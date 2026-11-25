from pathlib import Path #biblioteca que ajuda a acessar e manipular arquivos e pastas
from typing import Any #ajuda a trabalhar com anotações de tipo. nesse caso, o Any retorna qualquer tipo de dado sem especificar qual.

import bibtexparser

class BibtexReadError(Exception): #cria uma classe com nome e tipo Exception, que já existe no python
    """Erro relacionado à leitura de um arquivo Bibtex.""" #docstring que explica o que a classe faz
    pass #ainda não tem função

def load_bibtex_file( #função "carregar arquivos bibtex"
        file_path: str | Path) -> tuple[Any, list[dict[str, Any]]]:
                      #ou    #retorna         #lista de dicionarios
    path = Path(file_path) #aqui converto o caminho que recebo em objeto tipo Path


            #extensão do arquivo em minústiculo, tipo .bib
    if path.suffix.lower()!=".bib": #verficar se é arquivo bibtex mesmo
        raise ValueError(
            "O arquivo precisa possuir a extensão .bib :(("
        )

    
    #verificar se arquivo existe e corresponde
    if not path.is_file():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {path}"
        )


    try:                        #parse=interpretar/analisar, então usar bibtextparser para interpretar arquivo e guardar o resultado na variável library
        library = bibtexparser.parse_file( #ler o arquivo usando o bibtexparser
            str(path),
            encoding = "utf-8"
        )  
    except Exception as error: #caso dê errado
        raise BibtexReadError(
            f"Não foi possível interpretar o arquivo: {error}") from error

    if library.failed_blocks: #ver se existem blocos que não puderam ser interpretados
        errors = [] #block =bloco atual que não pode ser interpretado
        for block in library.failed_blocks:
            errors.append(
                f"Linha {block.start_line}: {block.error}"
            )                  #indica em qual linha o bloco começa
        raise BibtexReadError(
            "O arquivo possui entradas com problemas:\n" +"\n".join(errors))

    if not library.entries: #verifica se existem referencias
        raise BibtexReadError("Nenhuma referência bibliográfica foi encontrada.")
    
    records = [] #lista pra armazenar registros organizadinhos
        #entrada
    for entry in library.entries: #percorre entradas = referencias

        fields = {} #organizar campos em um dicio

        for field in entry.fields:#percorre os campos de CADA referência
            fields[field.key] = str(field.value) 
        
        record = { #organizar registros
            "key": entry.key,
            "entry_type": entry.entry_type,
            "fields": fields
        }  
        
        records.append(record)  #colocar registro na lista
        
    return library, records #retorna arquivo bibtex interpretado e lista com dicionários 