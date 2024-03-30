import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
import pandas as pd

class InvestmentManager:
    def __init__(self) -> None:
        load_dotenv()
    def download(self,url, xpath):
        options = Options()
        options.add_argument('--window-size=1920,1080')
        options.add_experimental_option("prefs", {
            "download.default_directory": os.getcwd(),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        })
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(20)
        button = driver.find_element(By.XPATH,xpath)
        # Click the button
        button.click()
        time.sleep(20)
        driver.quit()

    def getCurrency(self):
        options = Options()
        options.add_argument('--window-size=1920,1080')
        options.add_experimental_option("prefs", {
            "download.default_directory": os.getcwd(),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        

        driver = webdriver.Chrome(options=options)

        # Open the website you want to extract information from
        url = 'https://kur.doviz.com/serbest-piyasa/amerikan-dolari'
        driver.get(url)

        # Use XPath to locate the specific element you want
        # For example, let's say you want to extract the text of a specific paragraph with class "content"
        currencies = {}
        currencies["Current Dolar"] = driver.find_element(By.XPATH, "//div[@class='text-xl font-semibold text-white']")
        currencies["Current Dolar"] = float(currencies["Current Dolar"].text.replace(",", "."))
        dolarCurrency = driver.find_element(By.XPATH, "//body/div[contains(@class,'wrapper')]/div[@class='kur-page']/div[@class='article-content']/div[@class='evergreen']/div[@class='summary row-flex']/div[2]").text

        dolarCurrency = dolarCurrency.replace(",", ".").split("\n")
        currencies["Montly Dolar Change"] = float(dolarCurrency[3][1:])/100
        currencies["Yearly Dolar Change"] = float(dolarCurrency[5][1:])/100

        url = 'https://kur.doviz.com/serbest-piyasa/euro'
        driver.get(url)
        currencies["Current Euro"] = driver.find_element(By.XPATH, "//div[@class='text-xl font-semibold text-white']").text.replace(",", ".")
        currencies["Current Euro"] = float(currencies["Current Euro"])
        
        euroCurrency = driver.find_element(By.XPATH, "(//div[@class='summary row-flex'])").text
        
        euroCurrency = euroCurrency.replace(",", ".").split("\n")
        currencies["Montly Euro Change"] = float(euroCurrency[7][1:])/100
        currencies["Yearly Euro Change"] = float(euroCurrency[9][1:])/100
        # Close the browser
        driver.quit()

        return currencies

    def delete(self,loc):
        try:
            os.remove(os.path.join(os.getcwd(),loc))
            print("deleted successfully")
            return True
        except:
            #raise exception
            raise Exception("File not found " + loc)
            return False

    def updateStocks(self):
        df = pd.read_excel("Hisseler.xlsx")
        links = df["tradingView Linki"].values

        options = Options()
        options.add_argument('--window-size=1920,1080')
        options.add_experimental_option("prefs", {
            "download.default_directory": os.getcwd(),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        driver = webdriver.Chrome(options=options)

        info = []
        for link in links:
            if link.startswith("https:"):
                # Open the website you want to extract information from
                driver.get(link)
                time.sleep(10)
                price = driver.find_element(By.XPATH, "//div[@class='quotesRow-pAUXADuj']").text.split("\n")[0]
                info.append(float(price[:-3]))

        driver.quit()
        
        # Make sure info and df have the same length
        if len(info) < len(df):
            info.extend([None] * (len(df) - len(info)))

        df["Güncel Fiyat"] = info
        df["Güncel Değer"] = df["Güncel Fiyat"]*df["Adet"]
        df["Kar(TL)"] = (df["Güncel Fiyat"]-df["Alış Fiyatı"])*df["Adet"]
        df["Kar(%)"] = df["Kar(TL)"]/(df["Alış Fiyatı"]*df["Adet"])
        df["Gün"] = (pd.to_datetime('today') - df['Tarih']).dt.days
        df["Ortalama Aylık Getiri"] = df["Kar(%)"]/ (df["Gün"]/30)

        df.to_excel("Hisseler.xlsx",index=False)

    def wait(self):
        time.sleep(5)

    def getCurrentFons(self):
            df = pd.read_excel("Portföyüm.xlsx")
            
            return df['Fon Kodu'].values

    def getPrices(self,currentFons):
        #open fon fiyatları
        df = pd.read_excel("Takasbank TEFAS  Tarihsel Veriler.xlsx",skiprows=1)

        prices = []
        # Specify the Fon Kodu you want to retrieve the Fiyat for
        for target_fon_kodu in currentFons: 
            if str(target_fon_kodu) != 'nan':
                # Filter the DataFrame based on the Fon Kodu
                filtered_df = df.loc[df['Fon Kodu'] == target_fon_kodu]

                # Retrieve the Fiyat information from the filtered DataFrame
                prices.append( filtered_df['Fiyat'].values[0])
        return prices

    def updatePrices(self,prices):
        df = pd.read_excel("Portföyüm.xlsx")
        df['CURRENT PRICE'] = prices
        df.to_excel("Portföyüm.xlsx",index=False)

    def rankFunds(self,currentFons):
        df = pd.read_excel("Takasbank TEFAS  Fon Karşılaştırma.xlsx", skiprows=1)
        group = df.groupby('Şemsiye Fon Türü')

        ranks = group['1 Ay (%)'].rank(ascending=False)
        ranks_df = df.loc[df['Fon Kodu'].isin(currentFons), ['Fon Kodu']]
        ranks_df['Rank'] = ranks

        return ranks_df

    def updatePortfoy(self,prices):

        self.updatePrices(prices)
        df = pd.read_excel("Portföyüm.xlsx")
        df['TOTAL PRICE'] = df['CURRENT PRICE'] * df['QUANTITY']
        df['CURRENT PROFIT'] = df['TOTAL PRICE'] - df['COST']
        df['CURRENT PROFIT (%)'] = df['CURRENT PROFIT'] / df['COST']
        df['HOW LONG'] = (pd.to_datetime('today') - df['DATE']).dt.days
        df['Ortalama Aylık Getiri'] = df['CURRENT PROFIT (%)'] / (df['HOW LONG'] / 30)

        newRanks = self.rankFunds(df['Fon Kodu'].values)
        # Specify suffix '_y' for duplicate columns during merge
        df = df.merge(newRanks, on='Fon Kodu', how='left', suffixes=('', '_y'))

        # Take 'Rank_y' column and drop the duplicate 'Rank' column
        df['Rank'] = df['Rank_y']
        df.drop(columns='Rank_y', inplace=True)

        df.to_excel("Portföyüm.xlsx", index=False)

        result = {}
        result["Current Profit"] = df['CURRENT PROFIT'].sum()
        result["Total Price"] = df['TOTAL PRICE'].sum()
        result["Average Montly Profit"] = (df["Ortalama Aylık Getiri"] * df["COST"]).mean()
        result["Average Montly Profit(%)"] = (df["Ortalama Aylık Getiri"]).mean()

        return result

    def updateKurKoruma(self,df,currencies):
        for account in ["Kur Koruma-I","Kur Koruma-II","Kur Koruma-III"]:
            df.loc[df["Yatırım Aracı"] == account,"Anlık Değer"] = currencies["Current Dolar"]*df.loc[df["Yatırım Aracı"] == account,"Döviz"]
            df.loc[df["Yatırım Aracı"] == account,"Total Getiri"] = df.loc[df["Yatırım Aracı"] == account,"Anlık Değer"] - df.loc[df["Yatırım Aracı"] == account,"Değeri"]
            df.loc[df["Yatırım Aracı"] == account,"Aylık Kar Oranı"] = currencies["Montly Dolar Change"]
            df.loc[df["Yatırım Aracı"] == account,"Aylık Getirisi"] = currencies["Montly Dolar Change"] * df.loc[df["Yatırım Aracı"] == account,"Döviz"]

    def updateCurrency(self,df,currencies):
        for account in ["Dolar", "Dolar - II"]:
            df.loc[df["Yatırım Aracı"] == account,"Anlık Değer"] = currencies["Current Dolar"]*df.loc[df["Yatırım Aracı"] == account,"Döviz"]
            df.loc[df["Yatırım Aracı"] == account,"Total Getiri"] = df.loc[df["Yatırım Aracı"] == account,"Anlık Değer"] - df.loc[df["Yatırım Aracı"] == account,"Değeri"]
            df.loc[df["Yatırım Aracı"] == account,"Aylık Kar Oranı"] = currencies["Montly Dolar Change"]
            df.loc[df["Yatırım Aracı"] == account,"Aylık Getirisi"] = currencies["Montly Dolar Change"] * df.loc[df["Yatırım Aracı"] == account,"Döviz"]

        for account in ["Euro", "Euro - II"]:
            df.loc[df["Yatırım Aracı"] == account,"Anlık Değer"] = currencies["Current Euro"]*df.loc[df["Yatırım Aracı"] == account,"Döviz"]
            df.loc[df["Yatırım Aracı"] == account,"Total Getiri"] = df.loc[df["Yatırım Aracı"] == account,"Anlık Değer"] - df.loc[df["Yatırım Aracı"] == account,"Değeri"]
            df.loc[df["Yatırım Aracı"] == account,"Aylık Kar Oranı"] = currencies["Montly Euro Change"]
            df.loc[df["Yatırım Aracı"] == account,"Aylık Getirisi"] = currencies["Montly Euro Change"] * df.loc[df["Yatırım Aracı"] == account,"Döviz"]

    def updateHisseler(self,df):
        dfhisse = pd.read_excel("Hisseler.xlsx")
        df.loc[df["Yatırım Aracı"] == "Hisse Senetleri","Anlık Değer"] = dfhisse["Güncel Değer"].sum()
        totalprofit = dfhisse["Kar(TL)"].sum()
        df.loc[df["Yatırım Aracı"] == "Hisse Senetleri","Total Getiri"] = totalprofit
        
        # Calculate mean and sum for 'Hisse Senetleri' rows in dfhisse
        mean_aylik_getiri =  dfhisse["Ortalama Aylık Getiri"].mean()
        dfhisse['Alış'] = dfhisse['Adet'] * dfhisse['Alış Fiyatı']
        sum_alis_fiyati = dfhisse["Alış"].sum()

        # Update 'Aylık Kar Oranı' and 'Aylık Getirisi' columns in df
        df.loc[df["Yatırım Aracı"] == "Hisse Senetleri", "Aylık Kar Oranı"] = mean_aylik_getiri
        df.loc[df["Yatırım Aracı"] == "Hisse Senetleri", "Aylık Getirisi"] = mean_aylik_getiri * sum_alis_fiyati
        df.loc[df["Yatırım Aracı"] == "Hisse Senetleri", "Değeri"] = sum_alis_fiyati
        dfhisse = dfhisse.drop("Alış", axis=1)


    def updateYatirimlar(self,portfoyPerformance,currencies):
        df = pd.read_excel("Yatırımlar.xlsx")
        df.loc[df["Yatırım Aracı"] == "Fon","Anlık Değer"] = portfoyPerformance["Total Price"]
        df.loc[df["Yatırım Aracı"] == "Fon","Total Getiri"] = portfoyPerformance["Current Profit"]
        df.loc[df["Yatırım Aracı"] == "Fon","Aylık Kar Oranı"] = portfoyPerformance["Average Montly Profit(%)"]
        df.loc[df["Yatırım Aracı"] == "Fon","Aylık Getirisi"] = portfoyPerformance["Average Montly Profit"]

        self.updateKurKoruma(df,currencies)
        self.updateCurrency(df,currencies)
        self.updateHisseler(df)

        df.to_excel("Yatırımlar.xlsx",index=False)

    def update(self,currencies):

        #get current fon codes
        currentFons = self.getCurrentFons()

        #get their prices
        prices = self.getPrices(currentFons)

        #update their portfoy
        portfoyPerformance = self.updatePortfoy(prices)
        #update yatırımlar.xlsx

        #update stocks
        self.updateStocks()

        #update report 
        self.updateYatirimlar(portfoyPerformance,currencies)

    def download_Fund_Info(self):
        if(self.delete("Takasbank TEFAS  Fon Karşılaştırma.xlsx")):
            self.download('https://www.tefas.gov.tr/FonKarsilastirma.aspx','//button[@title="Tüm satırları ve görünen sütunları Excel biçeminde indirir"]')
        
        #download fon fiyatları
        if(self.delete("Takasbank TEFAS  Tarihsel Veriler.xlsx")):
             self.download("https://www.tefas.gov.tr/TarihselVeriler.aspx",'//button[@title="Tüm satırları ve görünen sütunları Excel biçeminde indirir"]')            
    
    def start_update(self):
        currencies = self.getCurrency()
        self.update(currencies)

    def start(self):
        self.download_Fund_Info()       
        self.start_update()