from datetime import datetime
import random
import urllib3
import json
import time
from bs4 import BeautifulSoup
import csv




# Creating a PoolManager instance for sending requests.
# default_headers = urllib3.make_headers(proxy_basic_auth='brd-customer-hl_9d5c0427-zone-data_center:mhz69dt2jqyc')
# http = urllib3.ProxyManager("https://brd.superproxy.io:22225", proxy_headers=default_headers)
default_headers = urllib3.make_headers(proxy_basic_auth='brd-customer-hl_0ba0faa8-zone-data_center:9rc2myrrez3k')
http = urllib3.ProxyManager("https://brd.superproxy.io:22225", proxy_headers=default_headers)
headersfile = open("./user_agents.txt", "r")
headers = headersfile.read()
headers = eval(headers)
global filenameread
global filenamewrite
global startLine
    


def random_delay():
    random_delay = random.uniform(1, 5)
    print(f"Sleeping for {random_delay:.2f} seconds...")
    time.sleep(random_delay) 

def fetch(url, headerNumber):
    default_headers = urllib3.make_headers(proxy_basic_auth='brd-customer-hl_9d5c0427-zone-data_center:mhz69dt2jqyc')
    http = urllib3.ProxyManager("https://brd.superproxy.io:22225", proxy_headers=default_headers)
    response = http.request("GET", url, headers=headers[headerNumber])

    while BeautifulSoup(response.data.decode("utf-8"), "html.parser").findAll("title")[0].text == "ShieldSquare Captcha":
        print("gotCaptcha")
        default_headers = urllib3.make_headers(proxy_basic_auth='brd-customer-hl_9d5c0427-zone-data_center:mhz69dt2jqyc')
        http = urllib3.ProxyManager("https://brd.superproxy.io:22225", proxy_headers=default_headers)
        print("Resuming...")
        headerNumber= headerNumber + 1
        response = http.request("GET", url, headers=headers[headerNumber])
    return response, headerNumber

def listingFetchParse(url, headerNumber):
    # Get a random User-Agent string
    headerNumber = headerNumber
    response, headerNumber = fetch(url, headerNumber)

    if response.status == 200:
       listingjson = parseListing(response)
    else:
        print(f"Failed to fetch the page. Status code: {response.status}")
    return listingjson, headerNumber

def getListingInfo(headerNumber):

    with open(filenameread, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        line_count = 0
        for row in reader:
            if line_count == 0:
                line_count += 1
            else:
                if row[0] >= startLine and row[1].__contains__("https://www.njuskalo.hr/auti/"):
                    headerNumber = parseListingsAndToCsv(headerNumber,row[0], row[1])
                    print("processed linenum: ",row[0])
                line_count += 1
        print(f'Processed {line_count} lines.')

def parseListing(response):
    html_content = response.data.decode("utf-8")
    listingjson = {
        "price": "",
        "lat": "",
        "lng": "",
        "flatBuildingtype": "",
        "flatFloorCount": "",
        "numberOfRooms": "",
        "buildingFloorPosition": "",
        "livingArea": "",
        "url": "",
        "bathrooms with toilet": "",
        "toilets": ""
    }

    #with open("saved_webpage.html", "w", encoding="utf-8") as file:
     #   file.write(html_content)
    soup = BeautifulSoup(response.data.decode("utf-8"), "html.parser")
    pricet = soup.findAll("dd")
    for index, price in enumerate(pricet):
        if ("class" in price.attrs):
            if ("ClassifiedDetailSummary-priceDomestic" in price["class"]):
                listingjson["price"] = price.text.rsplit("/")[0].strip().split(",")[0].strip()
    

    divz = soup.findAll("div")
    for index, div in enumerate(divz):
        if ("class" in div.attrs):
            if ("content-main" in div["class"]):
                scripts = div.findAll("script")
            if ("ClassifiedDetailPropertyGroups--standard" in div["class"]):
                grijanje = div.findAll("section")
                for index, grija in enumerate(grijanje):
                    divuli = grija.findAll("div")[0].findAll("ul")[0]
                    if grija.findAll("h3")[0].text == "Kupaonica i WC":
                        listingjson["bathrooms with toilet"] = divuli.findAll("li")[0].text.rsplit(":")[1].strip()
                        if len(divuli.findAll("li"))>1:
                            listingjson["toilets"] = divuli.findAll("li")[1].text.rsplit(":")[1].strip()
    for index, script in enumerate(scripts):
        jsona = script.text.rsplit("app.boot.push(")[1].strip().split(");")[0].strip()
        jsonl = json.loads(jsona)
        if (("values" in jsonl.keys()) and isinstance(jsonl["values"], dict) and 
            ("mapData" in jsonl["values"].keys()) and isinstance(jsonl["values"]["mapData"], dict)
                and ("defaultMarker" in jsonl["values"]["mapData"].keys())):
            
            defmark = jsonl["values"]["mapData"]["defaultMarker"]

            listingjson["lat"] = defmark["lat"]
            listingjson["lng"] = defmark["lng"]
    
    spans = soup.findAll("span")
    i = 0
    for index, span in enumerate(spans):
        if ("data-qa" in span.attrs):
            if ("location" in span["data-qa"]):
                listingjson["location"] = span.text.rsplit(",")[1].strip()
            elif ( "flatBuildingType" in span["data-qa"]):
                listingjson["flatBuildingtype"] = span.text
            elif ("flatFloorCount" in span["data-qa"]):
                listingjson["flatFloorCount"] = span.text
            elif ("numberOfRooms" in span["data-qa"]):
                listingjson["numberOfRooms"] = span.text
            elif ("buildingFloorPosition" in span["data-qa"]):
                listingjson["buildingFloorPosition"] = span.text
            elif ("livingArea" in span["data-qa"]):
                listingjson["livingArea"] = span.text.rsplit(",")[0].strip()
    return listingjson

def parseListingsAndToCsv(headerNumber, linenum, url):
    with open(filenamewrite, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if headerNumber < 999:
            headerNumber += 1
        else:
            headerNumber = 0
        print(url)
        rowToWrite, headerNumber = listingFetchParse(url, headerNumber)  
        rowToWrite["url"] = url
        rowToWrite = (linenum, rowToWrite["price"], rowToWrite["lat"], rowToWrite["lng"], rowToWrite["location"], rowToWrite["flatBuildingtype"], rowToWrite["flatFloorCount"], rowToWrite["numberOfRooms"], rowToWrite["buildingFloorPosition"], rowToWrite["livingArea"], rowToWrite["url"], rowToWrite["bathrooms with toilet"], rowToWrite["toilets"])
        if(rowToWrite):
            writer.writerow(rowToWrite)
    return headerNumber



if __name__ == "__main__":
    now = datetime.now()

    filenameread = 'csvovi/bentley/njuskalo_scrape_listing_links_bentley_18-12-2023_13-16-20.csv'
    startLine = 0

    # dd/mm/YYH:M:S
    dt_string = now.strftime("_%d-%m-%Y_%H-%M-%S")
    print("date and time =", dt_string)
    filenamewrite = filenameread.split(".csv")[0] + "obrađena(početak obrade u "+dt_string+")" + ".csv"
    with open(filenamewrite, 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["linenum","price", "lat", "lng", "location", "flatBuildingtype", "flatFloorCount", "numberOfRooms", "buildingFloorPosition", "livingArea", "url", "bathrooms with toilet", "toilets"])       
    
    getListingInfo(0)
    headersfile.close()
