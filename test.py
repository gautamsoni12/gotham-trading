import requests

def getFinancialNews():
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey=FD84XWAC8MLSCKM4'
    r = requests.get(url)
    data = r.json()

    print(data)

if __name__ == "__main__":
    getFinancialNews()