## 📄 `README.md`

```markdown
# 📚 Leitor de EPUB com FastAPI

Este projeto é um pequeno servidor construído com **FastAPI**, que lê arquivos `.epub` da pasta `books`, extrai os capítulos do livro e os divide em partes menores com base em um limite de caracteres. Ele pode ser usado para construir um front-end que consome livros de forma paginada, por exemplo.

```

### 🚀 Como funciona


Este é o arquivo principal que sobe a API usando o **FastAPI**.


```python
# server.py

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from reader import read_epub

app = FastAPI()

origins = ["*"]  # Libera o CORS para qualquer origem

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/books")
async def main(name: str):
    data = read_epub(name)
    return {"good_read": data}
````

### Endpoint principal:

* `GET /books?name=poor_folk`
  Lê o arquivo `poor_folk.epub` da pasta `/books` e retorna um JSON com os blocos de texto. </br>
  Certifique-se de trocar 'poor_folk' pelo nome do livro que deseja 
---

## 📖 `reader.py`

Este módulo contém duas funções principais:

### 📌 `dividir_capitulos(texto: str, limite: int)`

Essa função divide um texto grande em partes menores com base em um **limite de caracteres**, sem quebrar palavras no meio.

#### 🧠 Como funciona:

1. Recebe um texto e um número máximo de caracteres.
2. Divide o texto em palavras com `split(' ')`.
3. Percorre as palavras, acumulando-as até atingir o limite.
4. Quando o limite é atingido, a parte atual é adicionada ao array final.
5. Garante que nenhuma palavra fique fora e que a última parte também seja salva.

#### Código:

```python
def dividir_capitulos(texto: str, limite: int):
    palavras = texto.split(' ')
    partes = []
    palavra_atual = ''

    for palavra in palavras:
        if len((palavra_atual + ' ' + palavra).strip()) > limite:
            partes.append(palavra_atual.strip())
            palavra_atual = palavra
        else:
            palavra_atual += ' ' + palavra

    if palavra_atual:
        partes.append(palavra_atual.strip())

    return partes 
```

> 🔍 Detalhe: `.strip()` é usado para remover espaços extras no início e fim da string antes de verificar seu tamanho.

---
## 📝 Observação sobre a função de divisão

> Aqui temos uma função que recebe como parâmetro o texto (string) e um limite (number) de letras que retorna um array.

> A primeira variável (palavras) pega o texto e cria um array com cada palavra a cada espaço em branco. A variável `partes` é um array no formato string que começa vazio, e a let `palavra_atual` recebe uma string vazia.

> A cada palavra do array `palavras`:
>
> * Se o total de `palavra_atual + palavra` for maior que o limite, empurra no array e reinicia.
> * Se não, adiciona a nova palavra.
> * No final, garante que tudo que restou seja incluído no array final.

> Assim, nunca quebramos palavras no meio, e temos blocos legíveis.

---



### 📌 `read_epub(book_name: str)`

Essa função recebe o nome de um arquivo EPUB (sem extensão) e:

1. Lê o arquivo da pasta `/books`.
2. Filtra apenas os conteúdos HTML dos capítulos.
3. Extrai o texto puro com `BeautifulSoup`.
4. Usa `dividir_capitulos()` para quebrar o conteúdo em blocos menores.
5. Retorna uma lista de partes (strings) com no máximo 5000 caracteres cada.

#### Código:

```python
def read_epub(book_name):
    capitulos = []
    result = []

    book = epub.read_epub(f"./books/{book_name}.epub")
    
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text = soup.get_text()
            capitulos.append(text)

    for capitulo in capitulos:
        result += dividir_capitulos(capitulo, 5000)

    return result
```

---

## ▶️ Como rodar o servidor

### 1. Instale as dependências:

```bash
pip install fastapi ebooklib beautifulsoup4
```

### 2. Coloque seus livros `.epub` na pasta `books/`

> Exemplo: `books/poor_folk.epub`

### 3. Rode o servidor:

```bash
fastapi dev server.py
```

Acesse em:

```
http://localhost:8000/books?name=poor_folk
```

---

## 🧪 Teste de exemplo

Com o livro `poor_folk.epub` na pasta `/books`, faça uma requisição:

```http
GET http://localhost:8000/books?name=poor_folk
```

Resposta (exemplo resumido):

```json
{
  "good_read": [
    [0...99], # Aqui está divido os index de 0 a 99 com cada index tendo no maximo 5k palavras
    [100...199],
    [200...299],
    ...
    ]
}
```

---


## 📌 Futuras melhorias

* Criar paginação para a API (ex: `/books?page=1`)
* Aceitar limite como parâmetro de query
* Salvar os blocos cacheados
* Gerar áudio com TTS baseado nos blocos



---

# 🐍 Ambiente de Desenvolvimento Python
Por que usar um ambiente virtual?
O ambiente virtual (venv) isola os pacotes que você instala para um projeto específico. Isso evita conflitos de versões entre diferentes projetos Python no mesmo computador. Assim, cada projeto pode ter suas próprias dependências, sem afetar os outros.

## Como criar e ativar o ambiente virtual

### 🔧 Criando o ambiente virtual

Se você tiver múltiplas versões do Python instaladas, especifique o caminho desejado:

````
python3.10 -m venv env
````

Isso criará uma pasta chamada `env` contendo um ambiente Python isolado.

### ⚙️ Ativando o ambiente virtual

* **Linux/macOS/WSL**:

  ```bash
  source env/bin/activate
  ```

* **Windows (cmd)**:

  ```cmd
  env\Scripts\activate.bat
  ```

* **Windows (PowerShell)**:

  ```powershell
  env\Scripts\Activate.ps1
  ```

Você saberá que deu certo se o nome do ambiente aparecer no início da linha, como por exemplo:

```bash
(env) seu-usuario@seu-pc:~/meu-projeto$
```

### ❓ Por que usar um ambiente virtual?

* Evita conflitos entre bibliotecas de projetos diferentes.
* Garante que outras pessoas (ou você no futuro) consigam reproduzir o ambiente facilmente.
* Mantém seu sistema limpo, sem instalar dependências globalmente.



---

## 🧠 Conclusão

Esse projeto é um ótimo ponto de partida para apps que lidam com leitura, conversão de texto em áudio, leitores de e-book web/mobile ou APIs de conteúdo textual baseado em EPUBs. Ele já cuida da extração e organização dos dados para você focar na interface.

---

Feito por Avelino e meu amigo GePeTo é claro 😎
