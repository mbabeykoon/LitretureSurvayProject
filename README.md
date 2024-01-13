# Academic Paper Search Tool

## Overview

This Flask application provides a simple interface for searching academic papers from various sources, including Google Scholar, PubMed, IEEE Xplore, arXiv, and potential university repositories. Users can select a source, enter a topic and keywords, and receive a list of relevant papers.

## Features

- Search academic papers from multiple sources.
- Easy-to-use web interface.
- Results include titles and links to the papers.

## Installation

To set up the project locally, follow these steps:

1. **Clone the Repository**
   - git clone https://github.com/mbabeykoon/LitretureSurvayProject.git
   - cd LitretureSurvayProject
   

2. **Set Up the Conda Environment:**
   - conda env create -f environment.yml
   - conda activate ge_research

## Environment Configuration

- Set your email in the search_pubmed function for the Entrez API.
- Provide your IEEE Xplore API key in the search_ieee_xplore function.

## Usage

Run the Flask application:
flask run

Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Contributing
Contributions to this project are welcome. Please fork the repository and submit a pull request.



   





