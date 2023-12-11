from bs4 import BeautifulSoup

def olx_scrape():
    print("Olx scrape")
    with open('olx/olx_auti.html', 'r', encoding='utf-8') as f:
        contents = f.read()

    soup = BeautifulSoup(contents, 'html.parser')

    list_items = soup.find_all('li')
    for item in list_items:
        print(item.get_text())
        
    