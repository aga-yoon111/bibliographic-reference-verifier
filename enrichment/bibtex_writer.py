from pathlib  import Path
from copy import deepcopy #função que copia todos os objetos aninhados dentro dele sem alterar o original
from typing import Any

import bibtexparser
from bibtexparser.model import Field # importa a classe Field, onde cada campo é representado como um objeto Field com chave e valor

class BibtexWriteError(Exception):
    """Erro relacionado à geração do arquivo Bibtex."""
    pass

def write_enriched_bibtex(
    library: Any,
    approved_updates: dict, #dicionario onde cada chave é a chave de citação (identificador de cada referência) 
    #e o valor é outro dcionário com campos para atualizar
    output_path: str | Path, #onde o arquivo será guardado, aceita str e Path
    input_path: str | Path | None=None #caminho para caminho original, é opcional
 ) -> Path:  #o retorno será um objeto Path
    destination = Path(output_path)

    #Verificar se o destino tem extensão .bib
    if destination.suffix.lower() != ".bib":
        raise ValueError(
            "O arquivo de saída precisa ser extensão .bib"
        )


    if input_path is not None: #se o caminho original foi informado
        source = Path(input_path) #caminho original

        if destination.resolve()==source.resolve(): #.resolve transforma o caminho em um caminho completo/absoluto
            raise ValueError(
                "O arquivo original não pode ser sobrescrito." #para garantir que o novo não substituirá o antigo
            )


    updated_library = deepcopy(library) #copia biblioteca original para não modificar original

    #Organiza as entradas por chave em dicionário, onde a chave de cada coisa é a chave da referência e o valor é a referência (o objeto)
    entries_by_key = {} #facilita localizar referências que precisam mudar
    for entry in updated_library.entries:
        entries_by_key[entry.key] = entry


    unknown_keys = ( #armazena chaves recebidas para serem mudadas, mas que não foram encontradas na biblioteca
        set(approved_updates.keys())- set(entries_by_key.keys())   
    )   
                                #retorna elementos que estão no primeiro conjunto mas nao no segundo
    if unknown_keys:
        raise BibtexWriteError(
            f"Referências não encontradas: {unknown_keys}"
        )

    #Parte 2: fazendo as alterações aprovadas nas referências
    for citation_key, changes in approved_updates.items(): #para cada chave e a alteração
        if not isinstance(changes, dict): #se as alterações não forem um dicionário
            raise BibtexWriteError(
                f"Alterações inválidas para {citation_key}"
            )
        entry = entries_by_key[citation_key]  #procura uma chave que seja igual a citation_key

        for field_name, new_value in changes.items():#percorre campos
            if not isinstance(field_name, str) or not field_name.strip(): #verifica se o campo não é texto ou estiver vazio
                raise BibtexWriteError(
                    "Nome de campo inválido."
                )

            field_name = field_name.strip()
                                #dentro de, é
            if field_name.lower() in {"key", "entry_type"}:
                raise BibtexWriteError(
                    f"Não é permitido alterar {field_name}."
                )       

            if new_value is None:
                continue

            value = str(new_value).strip() #transforma novo valor em texto

            if value == "":
                continue

                        #coloca novo valor no campo certo da referência
            entry.set_field( #set_field=método do objeto entry, define campo na referência
                Field(
                    key=field_name,
                    value=value
                )
            )

    destination.parent.mkdir( #mkdir=método usado para criar pasta
        parents=True,#pode criar pastas anteriores que não existem ainda
        exist_ok=True #se existir, continua normalmente
    )

    #escreve em um novo arquivo .bib
    bibtexparser.write_file(
        str(destination),
        updated_library,
        encoding="utf-8"
    )
    return destination #retorna o caminho do arquivo novo











