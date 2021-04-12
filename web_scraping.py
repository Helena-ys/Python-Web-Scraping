import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Part A.
# driver = webdriver.Chrome(ChromeDriverManager().install())
DRIVER_PATH = "C:\\Users\\flaca\\PycharmProjects\\chromedriver.exe"
URL = "https://canada.michaels.com/"

browser = webdriver.Chrome(DRIVER_PATH)
browser.get(URL)

# Give the browser time to load all content.
time.sleep(3)
# Find the search input.
searchKeyword = "thread"
search = browser.find_element_by_css_selector("#q")
search.send_keys(searchKeyword)

# Find the search button - this is only enabled when a search query is entered
button = browser.find_element_by_css_selector("#mobile-searchgo")
button.click()  # Click the button.

# Product Information Class
class ProductInfo:
    productName = ""
    price = 0
    options =""
    storePickup = ""
    reviewRate = 0.0
    numOfReviews = 0

    def __init__(self, productName, price, options, storePickup, reviewRate, numOfReviews):
        self.productName    = productName
        self.price          = price
        self.options        = options
        self.storePickup    = storePickup
        self.reviewRate     = reviewRate
        self.numOfReviews   = numOfReviews

    def showDetail(self):
        print("Product Name: " + self.productName)
        print("Price: $" + str(self.price))
        print("Options: " + self.options)
        print("Store Pickup: " + self.storePickup)
        print("Review Rate: " + str(self.reviewRate) + " (out of 5)")
        print("# of Reviews: "+ str(self.numOfReviews))
        print("")

# Set page number and a list for product list
pageNum = 1
productList = []
for idx in range(0,3):
    content = browser.find_elements_by_css_selector(".product-tile")

    for e in content:
        textContent = e.get_attribute('innerHTML')

        # Beautiful soup removes HTML tags from our content if it exists.
        soup = BeautifulSoup(textContent, features="lxml")
        # Beautiful soup div.decompose() removes specific class
        # promotional messages
        for div in soup.find_all("div", {'class': 'product-promo'}):
            div.decompose()
        # clearance text
        for div in soup.find_all("div", {'class': 'clearance-badge'}):
            div.decompose()
        # standard price on sale items
        for div in soup.find_all("span", {'class': 'product-standard-price'}):
            div.decompose()

        rawString = soup.get_text().strip()

        # Remove hidden characters for tabs and new lines.
        rawString = re.sub(r"[\n\t]*", "", rawString)

        # Replace two or more consecutive empty spaces with '*'
        rawString = re.sub('[ ]{2}', ' ', rawString)
        rawString = re.sub('[ ]{2,}', '*', rawString)

        rawString = rawString.replace("Quickview", "*")
        rawString = rawString.replace("$", "*")
        rawString = rawString.replace(" - ", "")
        rawString = rawString.replace("*★★★★★*★★★★★*", "*")
        rawString = rawString.replace("stars. Read reviews for ", "stars*Read reviews for ")
        rawString = rawString.replace("Free Store Pickup", "Free Store Pickup*")
        rawString = rawString.replace("(", "")
        rawString = rawString.replace(")", "")

        productArray = rawString.split('*')
        lastIdx = len(productArray) - 1
        IDX_Option = 0

        # Set indexes for Product Name, Price, Review Rate
        # Get Store Pickup data
        if productArray[1]== "Free Store Pickup":
            IDX_Name = 2
            IDX_Price = 3
            IDX_Rate = 4
            productPickup = productArray[1].strip()
        else:
            # In case of no store pickup value
            IDX_Name = 1
            IDX_Price = 2
            IDX_Rate = 3
            productPickup = "N/A"

        # Product Options, Name, and Price
        productOption   = "N/A" if productArray[IDX_Option].strip() == "" else productArray[IDX_Option]
        productName     = productArray[IDX_Name].strip().title()
        productPrice    = float(productArray[IDX_Price])

        # Review Rate and Number of Reviews
        # In case of no review rate: length of the arrary is less than 4
        if lastIdx > 4:
            # In case of price range
            # Check if review rate in the [IDX_Rate] index
            # If the another product price in the [IDX_Rate] index
            # then the next index will be the review rate
            if productArray[IDX_Rate].find("star") != -1:
                productRate = productArray[IDX_Rate].strip()
            else:
                productRate = productArray[IDX_Rate + 1].strip()
            productRate = productRate.replace(' out of 5 stars', '')
            # Get Number of Reviews
            try:
                productReviews = int(productArray[lastIdx])
            except:
                productReviews = 0
        else:
            productRate = "N/A"
            productReviews = 0

        # Create class object and append it to the product list
        product = ProductInfo(productName, productPrice, productOption, productPickup, productRate, productReviews)
        productList.append(product)

    # Display the information of page loading
    print("*** Page " + str(pageNum) + " Loaded ***")
    # Next Page
    pageNum += 1
    URLNext = "https://canada.michaels.com/en/shop-categories/categories?q="+searchKeyword+"&page="
    URLNext = URLNext + str(pageNum)
    browser.get(URLNext)

    time.sleep(3)

# Part A. d) Display the product list
print("Search Result in " + searchKeyword)
print("==================================")
for product in productList:
    product.showDetail()

# Part A. f) and g)
# Create a dictionary from each row of product list and append it to a dataframe
# Write the dataframe to a CSV file and read the CSV file
DRIVER_PATH = "/Users/flaca/PycharmProjects/pythonProject/Dataset/"
CSV_FILE = "scrapping.csv"
dataSet = { 'Product Name': [], 'Price': [], 'Options': [],
            'Store Pickup': [], 'Review Rate': [], 'Reviews': []}

df = pd.DataFrame(dataSet, columns= ['Product Name', 'Price', 'Options', 'Store Pickup', 'Review Rate', 'Reviews'])
for product in productList:
    dicPro = {"Product Name":product.productName, "Price":product.price,
              "Options":product.options, "Store Pickup":product.storePickup,
              "Review Rate":product.reviewRate, "Reviews":product.numOfReviews}
    df = df.append(dicPro, ignore_index=True)

# Convert type of df['Reviews'] to int
df['Reviews'] =df['Reviews'].astype(int)

# Delimiter: Tab, specify the index for the first column - index_col=[0]
df.to_csv(DRIVER_PATH + CSV_FILE, sep='\t')
dfIn        = pd.read_csv(DRIVER_PATH + CSV_FILE, sep='\t', index_col=[0], keep_default_na=False)
print("*** The first two of products ***")
print(dfIn.head(2))
print("\n*** The last two of products ***")
print(dfIn.tail(2))

# Part B. ======================================================================================
URL = "https://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
# Scraping table element
stat_table = soup.find_all('table')
stat_table = stat_table[0]

# Get table heading (Column names)
heading = stat_table.find('tr')
colList = []
for element in heading.find_all('th'):
    colList.append(element.text)

currencyChange = []
tempList = []
# Get text from all the tr, th, ad td
for row in stat_table.find_all('tr'):
    for cell in row.find_all('th'):
        tempList.append(cell.text)
    for cell in row.find_all('td'):
        tempList.append(cell.text)

dataSet = { 'Currency':[], colList[1]:[], colList[2]:[], colList[3]:[], colList[4]:[], colList[5]:[] }
df = pd.DataFrame(dataSet, columns=['Currency',colList[1], colList[2],colList[3],colList[4],colList[5]])

startIdx = 6
for j in range(0, 23):
    endIdx = startIdx + 6
    data = tempList[startIdx:endIdx]
    dtSet = {colList[0]: tempList[startIdx], colList[1]: tempList[startIdx + 1],
             colList[2]: tempList[startIdx + 2], colList[3]: tempList[startIdx + 3],
             colList[4]: tempList[startIdx + 4], colList[5]: tempList[startIdx + 5]}
    df = df.append(dtSet, ignore_index=True)
    startIdx += 6

# Set selection of currencies for line charts
currencyList = ['European euro', 'UK pound sterling', 'US dollar', 'South Korean won']
# Line styles: Red dotted, cyan solid, magenta dashed, green dash-dot, and yellow dotted line styles
# with circle marker
styleList = ['r:o', 'c-o', 'm--o', 'g-.o', 'y:o']
dateList = colList[2:]      # Get Dates for x-axis labels
dicChange = {}

# Calculate percentage change
def getPtcChange(start, end, decimal=2):
    PtcChange = round((end - start)/start * 100, decimal)
    return PtcChange

# Build percentage chage of currency data for chart
for idx in range(0, len(df)):
    currency = df.iloc[idx][colList[0]]
    if currency in str(currencyList):
        tempList = []
        for j in range(1,6):
            if j < 5:
                pctChange = getPtcChange(float(df.iloc[idx][j]), float(df.iloc[idx][j+1]))
                tempList.append(pctChange)
        dicChange[currency] = tempList

fig = plt.figure(figsize=(9,6))
ax = plt.subplot(111)
for idx in range(0, len(dicChange)):
    line = ax.plot(dateList, dicChange[currencyList[idx]], styleList[idx], label=currencyList[idx])
    for a, b in zip(dateList, dicChange[currencyList[idx]]):
        # label = "{:.2f}".format(b)
        plt.annotate(b,  # this is the text
                     (a, b),  # this is the point to label
                     textcoords="offset points",  # how to position the text
                     xytext=(0, 10),  # distance from text to points (x,y)
                     ha='center')

plt.ylim(ymin=-0.7, ymax=0.7)  # Set's y axis between -0.7 and 0.7.
plt.xlabel("Dates")
plt.ylabel("Percentage Change (%)")
plt.title('Daily Exchange Rates', fontsize=16, color='navy')

# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8 , box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1.03, 0.5), fancybox=True, shadow=True)

plt.show()