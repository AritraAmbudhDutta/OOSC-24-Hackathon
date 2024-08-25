import requests
from bs4 import BeautifulSoup
import json

# Function to extract links from the main page
def extract_and_inspect_links(url):
    try:
        # Use a session to manage cookies
        with requests.Session() as session:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = session.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            
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
        # Use a session to manage cookies
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
    # Extract and inspect links from the main URL
    links = extract_and_inspect_links(main_url)
    
    # Store the data in a list of dictionaries
    data = []
    
    for link in links:
        print(f"Extracting paragraphs from {link}...")
        paragraphs = extract_paragraphs(link)
        data.append({
            'url': link,
            'paragraphs': paragraphs
        })
    
    # Save the extracted data to a JSON file
    with open('extracted_data.json', 'w') as file:
        json.dump(data, file, indent=4)
    
    print(f"Extracted data from {len(links)} links and saved to extracted_data.json")

# Main URL to scrape
main_url=input("Please input the URL: ")
#main_url = 'https://www.geeksforgeeks.org/'  # Replace with the actual URL

# Run the main function
main(main_url)