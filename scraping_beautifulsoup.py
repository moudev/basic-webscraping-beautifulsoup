# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


"""Busqueda en Google

 Para obtener los primeros 10 resultados de
 la busqueda en la web, extrayendo la url de cada resultado.
 
 Debido a que Google ya tiene su estructura HTML de cada resultado,
 solo se define de que etiquetas se quiere obtener el texto.

 Se obtiene la url como la interpreta Google, es decir no es la url
 definitiva del sitio de resultado, si no que es la url sin redireccionar.
 
"""

"""
Parameters
----------
busqueda : str
    Palabra con lo que se desea buscar, como fuera en el navegador
    ejem. 'que es la programación?'

Returns
-------
list
    list con cada uno de los resultados, [urls, titulo_url, numero_url]
"""
def buscarEnGoogle(busqueda):
    query = busqueda.encode('utf-8')
    url_google = 'https://www.google.com/search?q={}'.format(query)
    print(url_google)
    try:
        r_google = requests.get(url_google)
        code_res = r_google.status_code
        print code_res
        if code_res == 200:
            content_search = BeautifulSoup(r_google.content, 'html.parser')
            divs = content_search.find_all('h3', attrs={'class':'r'})
            divl = ' '.join(str(e) for e in divs)
            hrefs = BeautifulSoup(divl, 'html.parser')
            hrefl = hrefs.find_all('a')
            list_url  = []
            title_url = []
            n_urls = 0
            for element_dom in hrefl:
                element_url = 'https://www.google.com' + element_dom['href']
                element_txt = element_dom.text
                list_url.append(element_url)
                title_url.append(element_txt.encode('utf-8', 'ignore').decode('utf-8'))
                n_urls = n_urls + 1
            print '[log][info] Resultados de busqueda encontrados'
            return [list_url, title_url, n_urls]
    except Exception as error_scraping:
        print '[log][error] Error al ejecutar la busqueda en linea'
        return error_scraping

        
"""Obtener información de una web especifica

 Extrae el texto de una página web, recibiendo como parámetro la url
 del sitio.

 Para extraer la información hay un incoveniente con los anuncios que tiene
 el sitio, por lo tanto hay que hacer validaciones que se busque solamente
 en etiquetas que podrían tener información de interés, por ejemplo el título
 y el contenido del tema buscado, teniendo en cuenta que el sitio sigue
 los standares normales de las etiquetas que se deben de usar en cada
 de contenido, por el <h1> que se sabe que es para títulos, y <article>
 para contenido de artículos, es el único inconveniente que si la página
 no sigue ningún standar general, la información obtenida no puede
 tener coherencia.

 Solo se toma como párrafos de información a las cadenas de texto que tengan
 más de un largo especificado, además de limpiarlo de saltos de línea.
 
"""

"""
Parameters
----------
url : str
    Url para realizar la extracción de información

Returns
-------
str
    string con la información obtenida del sitio
"""
def cargarWeb(url):
    try:
        req_scraping = requests.get(url)
        req_scraping.encoding = 'utf-8'
        code_response_scraping = req_scraping.status_code
        if (code_response_scraping == 200):
            content_scraping = BeautifulSoup(req_scraping.text, 'html.parser')
            listado_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'span', 'article', '']
            divs_information = content_scraping.find_all(listado_tags)
            divs_text = [div for div in divs_information if len(div.get_text()) > 100]
            string_sintetizador = ""
            for x in divs_text:
                # Limpiando de saltos de linea
                clean = x.get_text()
                clean = clean.replace('\n', '').replace('\t', '').replace('\r', '')
                string_sintetizador += ' ' + clean
            print '[log][info] Scraping finalizado'
            return string_sintetizador

        elif (code_response_scraping == 404):
            print '[log][error] Error 404'
        else:
            print '[log][error] Error request scraping'
    except Exception as error_scraping:
        print '[log][error] Error en el Scraping'
        print error_scraping
