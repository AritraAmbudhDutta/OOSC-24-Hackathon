import requests
from bs4 import BeautifulSoup
import json

# Function to extract links from the main page
def extract_and_inspect_links(url):
    try:
        with requests.Session() as session:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = session.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            anchor_tags = soup.find_all('a', href=True)
            links = [requests.compat.urljoin(url, a['href']) for a in anchor_tags if a['href'].startswith(('http', '/'))]
            
            print(f"Total links extracted: {len(links)}")
            return links
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# Function to extract <p> tag content from each URL
def extract_paragraphs(url):
    try:
        with requests.Session() as session:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = session.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            paragraph_texts = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
            
            return paragraph_texts
    except requests.RequestException as e:
        print(f"Request error for {url}: {e}")
        return []
    except Exception as e:
        print(f"Error for {url}: {e}")
        return []

# Main function to orchestrate the process
def main(main_url):
    links = extract_and_inspect_links(main_url)
    all_paragraphs = []

    for link in links:
        print(f"Extracting paragraphs from {link}...")
        paragraphs = extract_paragraphs(link)
        all_paragraphs.extend(paragraphs)
    
    combined_paragraph = ' '.join(all_paragraphs)
    
    data = {
        'combined_paragraph': combined_paragraph
    }
    
    with open('extracted_data.json', 'w') as file:
        json.dump(data, file, indent=4)
    
    print(f"Extracted paragraphs combined into one and saved to extracted_data.json")

# Main URL to scrape
main_url = input("Please input the URL : ")

# Run the main function
main(main_url)
