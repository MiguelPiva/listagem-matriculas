import json
import os
import re
import requests


def key_acentos(nome:str) -> str:
    if nome.startswith(("Á", "Â")):
        return "A" + nome[1:]
    
    elif nome.startswith(("É", "Ê")):
        return "E" + nome[1:]
    
    elif nome.startswith(("Í",)):
        return "I" + nome[1:]
    
    elif nome.startswith(("Ó", "Ô")):
        return "O" + nome[1:]
    
    elif nome.startswith(("Ú",)):
        return "U" + nome[1:]
    
    else:
        return nome


def extrair_dados(url:str) -> list[dict]:
    resposta = requests.get(url, verify=False)
    conteudo_json = resposta.text.strip().rstrip(";")
    conteudo_json = conteudo_json.replace("todasDisciplinas=", "")
    dados = json.loads(conteudo_json)
    return dados


def nome_para_id(nome:str, id_cursos:dict) -> int:
    for chave, valor in id_cursos.items():
        if valor.lower() == nome.lower():
            return chave


def listar_turmas(id_curso:int, turmas:list[dict], tipo:str) -> list[dict]:
    lista_turmas = list()
    for dicionario in turmas:
        for obrigatoriedade in dicionario["obrigatoriedades"]:
            if obrigatoriedade["curso_id"] == id_curso and obrigatoriedade["obrigatoriedade"] == tipo:
                 lista_turmas.append(dicionario)
    return lista_turmas


def filtrar_listagem(id_curso:int, turmas:list[dict]) -> list[dict]:
    lista_filtradas = list()
    for dicionario in turmas:
        aux = False
        for obrigatoriedade in dicionario["obrigatoriedades"]:
            if obrigatoriedade["curso_id"] == id_curso and obrigatoriedade["obrigatoriedade"] == "obrigatoria":
                aux = True
                break
        lista_filtradas.append(dicionario) if not aux else None
    return lista_filtradas


def imprimir_disciplinas(turmas:list[str], filtro:bool, id_filtro:int) -> None:
    set_disciplinas = set()
    if filtro:
        turmas_filtradas = filtrar_listagem(id_filtro, turmas)
        for dicionario in turmas_filtradas:
            nome_disciplina = re.sub(r" \b\w{1,3}-\w+ \(\w+ \w+\)$", "", dicionario["nome"])
            set_disciplinas.add(nome_disciplina.title())
    else:
        for dicionario in turmas:
            nome_disciplina = re.sub(r" \b\w{1,3}-\w+ \(\w+ \w+\)$", "", dicionario["nome"])
            set_disciplinas.add(nome_disciplina.title())
    for item in sorted(set_disciplinas, key=key_acentos):
        print(">> ", item)


def listar_cursos_disciplina(dados:list[dict], id_cursos:dict, disciplina:str) -> None:
    for dicionario in dados:
        if disciplina in dicionario["nome"]:
            nome = re.sub(r" \b\w{1,3}-\w+ \(\w+ \w+\)$", "", dicionario["nome"])
            print(f"Disciplina: {nome.title()}")
            for obrigatoriedade in dicionario["obrigatoriedades"]:
                print(f">> {id_cursos[obrigatoriedade['curso_id']]}: {obrigatoriedade['obrigatoriedade']}")
            break


def listar_id_cursos(dicionario:dict) -> None:
    for chave, valor in dicionario.items():
        print(f"{chave}: {valor}")


def dicionario_id_cursos() -> dict:
    cursos = {
                73: 'Bacharelado em Ciência e Humanidades',
                74: 'Bacharelado em Ciências e Tecnologia',
                242: 'Bacharelado em Ciências Biológicas',
                243: 'Bacharelado em Física',
                244: 'Bacharelado em Química',
                245: 'Licenciatura em Ciências Biológicas',
                246: 'Licenciatura em Física',
                247: 'Licenciatura em Química',
                248: 'Bacharelado em Filosofia',
                249: 'Bacharelado em Engenharia Ambiental e Urbana',
                250: 'Licenciatura em Filosofia',
                251: 'Bacharelado em Engenharia de Energia',
                252: 'Bacharelado em Engenharia de Informação',
                253: 'Bacharelado em Engenharia de Instrumentação, Automação e Robótica',
                254: 'Bacharelado em Engenharia de Materiais',
                255: 'Bacharelado em Engenharia Aeroespacial',
                256: 'Bacharelado em Engenharia Biomédica',
                257: 'Bacharelado em Engenharia de Gestão',
                258: 'Bacharelado em Ciências Econômicas',
                259: 'Bacharelado em Planejamento Territorial',
                260: 'Bacharelado em Relações Internacionais',
                261: 'Bacharelado em Políticas Públicas',
                262: 'Bacharelado em Neurociência',
                263: 'Bacharelado em Matemática',
                264: 'Licenciatura em Matemática',
                265: 'Bacharelado em Ciência da Computação',
                339: 'Bacharelado em Biotecnologia',
                346: 'Licenciatura em Ciências e Humanidades',
                347: 'Licenciatura em Ciências Naturais e Exatas',
                406: 'Engenharias'
            }
    return cursos


def imprimir_interface(filtro:bool) -> None: 
    os.system("cls")
    print("OPÇÕES".center(60, "/"))
    print("1 - Listar limitadas de um curso"
        +"\n2 - Listar obrigatórias de um curso"
        +"\n3 - Listar limitadas e obrigatórias de um curso"
        +f"\n4 - Filtrar obrigatórias [{'LIGADO' if filtro else 'DESLIGADO'}]"
        +"\n5 - Exibir relação de uma disciplinas com os cursos"
        +"\n6 - Exibir ids de cursos"
        +"\n7 - Sair")
    print("/"*60)


def entrada_id_curso(id_cursos:dict) -> int:
    while True:
        try:
            entrada = int(input("Digite o id do curso: "))
            if entrada in id_cursos:
                return entrada
            else:
                print("Não há um curso com esse id.")

        except ValueError:
            print("Entrada inválida.")


if __name__ == "__main__":
    dados = extrair_dados("https://matricula.ufabc.edu.br/cache/todasDisciplinas.js")
    id_cursos = dicionario_id_cursos()
    filtro = False
    id_filtro = 0

    while True:
        imprimir_interface(filtro)
        opcao = input("Escolha uma opção: ")
        match opcao:

            # 1 - Listar limitadas de um curso
            case "1":
                id_curso = entrada_id_curso(id_cursos)
                print(f"\nDISCIPLINAS LIMITADAS DE {id_cursos[id_curso].upper()}:")
                disciplinas_lim = listar_turmas(id_curso=id_curso, turmas=dados, tipo="limitada")
                imprimir_disciplinas(disciplinas_lim, False, id_filtro)

            # 2 - Listar obrigatórias de um curso
            case "2":
                id_curso = entrada_id_curso(id_cursos)
                print(f"\nDISCIPLINAS OBRIGATÓRIAS DE {id_cursos[id_curso].upper()}:")
                disciplinas_obr = listar_turmas(id_curso=id_curso, turmas=dados, tipo="obrigatoria")
                imprimir_disciplinas(disciplinas_obr, filtro, id_filtro)
            
            # 3 - Listar limitadas e obrigatórias de um curso
            case "3":
                id_curso = entrada_id_curso(id_cursos)
                print(f"\nDISCIPLINAS LIMITADAS DE {id_cursos[id_curso].upper()}:")
                disciplinas_lim = listar_turmas(id_curso=id_curso, turmas=dados, tipo="limitada")
                imprimir_disciplinas(disciplinas_lim, False, id_filtro)

                print(f"\nDISCIPLINAS OBRIGATÓRIAS DE {id_cursos[id_curso].upper()}:")
                disciplinas_obr = listar_turmas(id_curso=id_curso, turmas=dados, tipo="obrigatoria")
                imprimir_disciplinas(disciplinas_obr, filtro, id_filtro)

            # 4 - Filtrar obrigatórias
            case "4":
                if filtro:
                    filtro = False
                    print("\nFiltro de obrigatórias desligado.")
                else:
                    filtro = True
                    print("\nFiltro de obrigatórias ligado. Escolha um curso para filtrar.")
                    id_filtro = entrada_id_curso(id_cursos)

            # 5 - Exibir relação de uma disciplinas com os cursos
            case "5":
                disciplina = input("Digite o nome da disciplina: ").upper()
                print()
                listar_cursos_disciplina(dados=dados, id_cursos=id_cursos, disciplina=disciplina)

            # 6 - Exibir ids de cursos
            case "6":
                print()
                listar_id_cursos(dicionario=id_cursos)

            # 7 - Sair
            case "7":
                break
            
            # Opção inválida
            case _:
                print("\nOpção inválida")

        input("Pressione Enter para continuar...")
