# listagem-matriculas
Programa para auxiliar na identificação de disciplinas limitadas e obrigatórias sendo ofertadas no período de matrícula/ajuste/reajuste da UFABC

---
Algumas observações:

1. Além do Python, para que o código funcione, será necessário instalar separadamente o módulo **requests**, caso você não o tenha. Basta digitar ``` pip install requests ``` no seu terminal (tutorial [aqui](https://youtu.be/r29uzZpIlWI?si=yQawakwkg-6VGRhS)) para instalar o módulo ou ``` pip list ``` para verificar se ele já está instalado. Os módulos **json**, **os** e **re** já vêm instalados no Python por padrão.

2. Caso não queira que as disciplinas obrigatórias de um curso interdisciplinar sejam listadas juntas das obrigatórias de curso específico, basta ativar a opção 5 e inserir o id do curso interdisciplinar.

Ao executar o programa, ele poderá levar alguns segundos para coletar e processar os dados. Ao finalizar o processamento, será impressa no terminal a interface abaixo, e assim, basta digitar o número da opção que você quiser e confirmar pressionando Enter:

```
///////////////////////////OPÇÕES///////////////////////////
1 - Listar limitadas de um curso
2 - Listar obrigatórias de um curso
3 - Listar limitadas e obrigatórias de um curso
4 - Listar disciplinas em comum entre dois cursos
5 - Filtrar obrigatórias [DESLIGADO]
6 - Exibir relação de uma disciplinas com os cursos
7 - Exibir ids de cursos
8 - Sair
////////////////////////////////////////////////////////////
Escolha uma opção:
```
