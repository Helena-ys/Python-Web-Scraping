# Python-Web-Scraping
This application scrapes uniform rows of content and table content from websites.

## Part A: Scrapes uniform rows of content from three pages of a site
- URL: https://canada.michaels.com/
- Framework: Selenium, Webdriver-manager, and ChromeDriver

#### Creates a class that has properties to store the cleansed data once you have extracted it. 
```
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
```
#### After scaping all pages, loop through the list and use a function of the custom class to display the content of each object in the list in a nicely formatted manner.
```
# Part A. d) Display the product list
print("Search Result in " + searchKeyword)
print("==================================")
for product in productList:
    product.showDetail()
```
![Display the result](https://github.com/Helena-ys/Python-Web-Scraping/blob/main/result_1.PNG?raw=true)

#### Build a data frame from the list
```
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
```
![Display the data frame](https://github.com/Helena-ys/Python-Web-Scraping/blob/main/result_2.PNG?raw=true)

![Image of Plot](https://github.com/Helena-ys/Python-Web-Scraping/blob/main/plot_currency_change.png?raw=true)
