from bs4 import BeautifulSoup

def njuskalo_scrape():
    print("Njuskalo scrape")
   
    with open('njuskalo/njuskalo_auti.html', 'r', encoding='utf-8') as f:
        contents = f.read()

    soup = BeautifulSoup(contents, 'html.parser')

    all_li_elements = soup.find_all('li', class_='EntityList-item--Regular')
    for li_element in all_li_elements:
        title = li_element.find('h3') 
        if title:
            print(title.get_text())
