import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup


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


def read_epub(book_name):
    
    capitulos = []  # Lista para armazenar os capítulos do livro
    result = []    
        
        
    book = epub.read_epub(f"src/books/{book_name}.epub")
    
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:# Aqui eu estou filtrando os itens do livro que são documentos.html
            soup = BeautifulSoup(item.get_content(), 'html.parser') # Como o arquivo é HTML, eu uso o BeautifulSoup para fazer o parse do conteúdo
            text = soup.get_text()
            dividir_capitulos(text,1000)
            capitulos.append(text)
    
    for capitulo in capitulos:
        result += dividir_capitulos(capitulo, 5000)
        
    return result


read_epub('poor_folk')