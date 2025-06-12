import httpx
from bs4 import BeautifulSoup

def parseSearchResults(resp):
    soup = BeautifulSoup(resp.text, "html.parser")
    results = soup.find_all("a", class_="result__a")
    for idx, result in enumerate(results, 1):
        title = result.get_text(strip=True)
        link = result['href']
        print(f"{idx}. {title}\n {link}\n")

def getRequest(url, headers=None):
    if headers:
        resp = httpx.get(url, headers=headers)
    else: 
        resp = httpx.get(url)

    if "Unusual traffic" in resp.text:
        return None
    else:
        return resp

# For testing
if __name__=="__main__":
    # Headers
    headers = {"User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ",
        "AppleWebKit/537.36 (KHTML, like Gecko) ",
        "Chrome/114.0.0.0 Safari/537.36"
        )
    }
    # Get Query
    query = input("Query: ")
    query.replace(' ', '+') 

    # Get Page Number
    num = input("Page #: ")
    if not num.isdigit:
        print("Please Enter A Valid Number")
        print()
        exit()
    url = "https://html.duckduckgo.com/html/?q="+query+"&num"+num
    # Get Request
    resp = getRequest(url)
    if resp==None:
        print("Error in Request")
    else:
        parseSearchResults(resp)
