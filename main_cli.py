import os
from urllib.parse import urljoin
import click
import requests
from bs4 import BeautifulSoup


def scrape_glencore_publications():
    # Website to scrape
    glencore_url = "https://www.glencore.com/publications"

    # Create folder for PDFs
    os.makedirs("pdfs", exist_ok=True)

    # Get HTML content
    response = requests.get(glencore_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all links ending with .pdf
    pdf_links = []
    for link in soup.find_all("a", href=True):
        href = link['href']
        if href.lower().endswith(".pdf"):
            full_url = urljoin(glencore_url, href)  # handle relative URLs 
            pdf_links.append(full_url)
            filename = full_url.split("/")[-1].lower()  # get file name part
            
            # ✅ Check if filename contains BOTH "annual" and "report"
            if "annual" in filename and "report" in filename:
                pdf_links.append(full_url)

    print(f"Found {len(pdf_links)} matching PDFs")
    
    # Download PDFs
    for pdf_url in pdf_links:
        filename = pdf_url.split("/")[-1]
        filepath = os.path.join("pdfs", filename)
        
        # Skip if already downloaded
        if os.path.exists(filepath):
            print(f"Skipping {filename}, already exists.")
            continue
        
        print(f"Downloading {filename}...")
        pdf_response = requests.get(pdf_url)
        with open(filepath, "wb") as f:
            f.write(pdf_response.content)
        print(f"Saved to {filepath}")
        
        
if __name__ == "__main__":
    scrape_glencore_publications()