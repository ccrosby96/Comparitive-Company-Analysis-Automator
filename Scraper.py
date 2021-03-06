import requests
from io import StringIO
import key 
import json
import time
import pandas as pd
import sqlite3
import smtplib
from datetime import datetime
from balance_sheet import BalanceSheet
from excel_wrangler import ExcelWrangler
from openpyxl import Workbook
import openpyxl


api_token = key.key



class Scraper():
    def __init__(self,key = api_token) -> None:
        self.session = requests.Session()
        self.key = key
        self.base_url = "https://eodhistoricaldata.com/api/fundamentals?api_token={}".format(self.key)
        self.raw_data = None

    def generate_filter_string(self, ticker):
        t = str(ticker).upper() + '.' + "US"
        url = "https://eodhistoricaldata.com/api/fundamentals/{}?api_token={}".format(t,self.key)
        return url

    def get_financials(self,string):
        '''This method makes a call to the eod API using a string generated by
            the generate_filter_string method. A json object is returned containg 
            the 3 financial statements of the company'''
        if self.session is None:
            self.session = requests.Session()
        url = string
        
        r = self.session.get(url)
        if r.status_code == requests.codes.ok:

            json_data = json.loads(r.text)
            self.raw_data = json_data
            return json_data
        else:
            raise Exception(r.status_code, r.reason, url)
    
    def get_balance_sheets(self,json):
        balance_sheet = json['Financials']['Balance_Sheet']['yearly']
        balance_sheet = list(balance_sheet.values())

        #cash_cash_equivalents
        print(balance_sheet[0]["cash"])
        return balance_sheet[0:2]
        #print(firstKey)

    
    def extract_tickers(self):
        '''This method extracts the ticker symbols from the JSON object response from the eod API. It then 
            stores them in the candidates.txt file'''
        tickers = []
        with open('candidates.txt') as json_file:
            data = json.load(json_file)
            for p in data['data']:
                tickers.append(p["code"])
        return tickers
    def get_tickers(self):
        '''This method  extracts the ticker symbols from the JSON object response from the eod API. A list
            of them is then returned. No write operations are made with this method'''
        tickers = []
        #API called here
        data = self.get_candidates()
        for ticker in data['data']:
            tickers.append((ticker["code"],ticker["name"]))
        return tickers


def main():
    apple = None
    with open('apple.json', 'r') as f:
        apple = json.load(f)

    file = "cca_test.xlsx"
    wb = openpyxl.load_workbook(file, read_only = False)

    scraper = Scraper()
    bsheets = scraper.get_balance_sheets(apple)
    print(bsheets[0])
    print('\n')
    print(bsheets[1])
    wrangler = ExcelWrangler(wb)
    wrangler.insert_balance_sheet(bsheets)
    wb.save('test1.xlsx')

    #balance_obj = BalanceSheet(apple_2021)
    #print(balance_obj2021.getItems())

if __name__ == "__main__":
    main()



