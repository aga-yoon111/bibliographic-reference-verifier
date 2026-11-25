from pathlib import Path

from parser.bibtex_parser import load_bibtex_file
from enrichment.bibtex_writer import write_enriched_bibtex

def main():

    input_path = Path("data/leon-ai-safety.bib")

    output_path = Path("output/leon-ai-safety-processed.bib")

    library, records = load_bibtex_file(input_path)

    print("Arquivo lido com sucesso!")

    print("Total de referências:", len(records))

    for record in records:
        print("\nReferência:", record["key"])
        print("Tipo:", record["entry_type"])
        print("Título:", record["fields"].get("title"))

                                #o get previne de dar KeyError, porque se o título não existir, retorna None

        approved_updates = {

        "ahn2019a": {

          "x-p1-test-field": "Teste de integração"

        }

    }

    result = write_enriched_bibtex(
        library = library,
        approved_updates=approved_updates,
        output_path=output_path, #onde o arquivo será salvo
        input_path=input_path
    )

    print("\nArquivo gerado com sucesso!")
    print("Local:", result)

if __name__ =="__main__":
    main()
    