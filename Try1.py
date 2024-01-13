from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from Bio import Entrez
from xml.etree import ElementTree

app = Flask(__name__)

def search_google_scholar(query):
    url = "https://scholar.google.com/scholar"
    params = {"q": query, "hl": "en"}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    papers = []
    for entry in soup.find_all("h3", class_="gs_rt"):
        title = entry.text
        link = entry.a['href'] if entry.a else 'No link available'
        papers.append({"title": title, "link": link})

    return papers


def search_pubmed(query):
    # Use your email here
    Entrez.email = "email.com" # Replace with your email
    
    # Search in PubMed
    handle = Entrez.esearch(db="pubmed", term=query, retmax=10)
    record = Entrez.read(handle)
    handle.close()

    # Fetch details of the articles
    idlist = record['IdList']
    papers = []
    
    if idlist:
        handle = Entrez.efetch(db="pubmed", id=idlist, retmode="xml")
        articles = Entrez.read(handle)['PubmedArticle']

        for article in articles:
            title = article['MedlineCitation']['Article']['ArticleTitle']
            # Construct URL for the article
            url = f"https://pubmed.ncbi.nlm.nih.gov/{article['MedlineCitation']['PMID']}/"
            papers.append({"title": title, "link": url})

        handle.close()

    return papers



def search_ieee_xplore(query):
    api_key = 'your_api_key_here'  # Replace with your IEEE Xplore API key
    url = "http://ieeexploreapi.ieee.org/api/v1/search/articles"
    params = {
        "querytext": query,
        "apikey": api_key,
        "format": "json",
        "max_records": 10  # Limit the number of records in response
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []

    data = response.json()
    papers = []

    for article in data.get('articles', []):
        title = article.get('title')
        link = article.get('pdf_url')  # or another appropriate field for the link
        papers.append({"title": title, "link": link})

    return papers


import requests
from xml.etree import ElementTree

def search_arxiv(query):
    # arXiv API endpoint
    url = 'http://export.arxiv.org/api/query'

    # Parameters for the search query
    params = {
        'search_query': query,
        'start': 0,
        'max_results': 10
    }

    # Sending a GET request to arXiv API
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []

    # Parse the response using ElementTree
    root = ElementTree.fromstring(response.content)
    namespace = {'arxiv': 'http://arxiv.org/schemas/atom'}
    
    papers = []
    for entry in root.findall('arxiv:entry', namespace):
        title = entry.find('arxiv:title', namespace).text.strip()
        link = entry.find('arxiv:link[@title="pdf"]', namespace).attrib['href']
        papers.append({"title": title, "link": link})

    return papers


def search_university_repository(query):
    # Implementation for University Repository
    pass

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topic = request.form['topic']
        keywords = request.form['keywords']
        source = request.form['source']

        query = f"{topic} {keywords}"

        if source == 'google_scholar':
            papers = search_google_scholar(query)
        elif source == 'pubmed':
            papers = search_pubmed(query)
        elif source == 'ieee_xplore':
            papers = search_ieee_xplore(query)
        elif source == 'arxiv':
            papers = search_arxiv(query)
        elif source == 'university_repository':
            papers = search_university_repository(query)
        # Add more conditions for other sources as needed

        return render_template('results.html', papers=papers)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
