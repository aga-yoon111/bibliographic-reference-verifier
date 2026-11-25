import bibtexparser

#criar caminho do arquivo
caminho = "data/text.bib" #vai pra cá

biblioteca = bibtexparser.parse_file(caminho) #lê o arquivo (do caminho) em bibtex e devolve em objeto chamado biblioteca

#mostra quantas referências achou
print("Total de referências", len(biblioteca.entries))

#mostra cada referência com for
for entrada in biblioteca.entries:
    print("Chave:", entrada.key)
    print("Tipo:", entrada.entry_type)

    for campo in entrada.fields: #mnostra os campos das entradas
        print(campo.key, "=", campo.value)

    print("-------------------")
