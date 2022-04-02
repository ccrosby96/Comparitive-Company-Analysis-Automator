# Calvin Crosby
# 3/15/2022
# Intepreter Class for CCA Model

from types import NoneType


class Interpreter():
    '''This class serves to map cells found in the excel spreadsheet to expressions of their respective values
        in terms of JSON tag elements scraped from the eod historical API. Each element in the JSON object
        is assigned an integer mapping, and excel values are mapped to an expression of these integers.
        The Intepreter class bridges this gap and is able to compute the correct value for any cell value
        with a mapping, given a JSON object.
        
         '''
    def __init__(self) -> None:
        self.income_items = ["Sales", "COGS", "Gross Profit", "SG&A", "Other Expense / (Income)", "EBIT", "Interest Expense",
            "Pre-tax Income", "Income Taxes", "Net Income"]
        
        self.income_tags = ["totalRevenue", "costOfRevenue", "grossProfit", "sellingGeneralAdministrative",
         "totalOperatingExpenses", "ebit", "interestExpense", "incomeBeforeTax", "incomeTaxExpense", "netIncome"]
        
        self.income_expressions = ["1", "2", "3", "4", "5 -4", "6", "7", "8", "9", "10"]

        self.balance_expressions = ["1", "2", "3", "6 -1 -2 -3","6","7","8 +9","12 -7 -8 -9","6 +12","13",
                                    "14","16 -13 -14","16","14 +7","18 -17", "16 +18", "19", "20", "24", "25"]

        self.balance_items = ["Cash and Cash Equivalents", "Accounts Receivable", "Inventories",
            "Prepaids and Other Current Assets", "Total Current Assets", "Property, Plant, and Equipment, net",
            "Goodwill and Intangible Assets", "Other Assets", "Total Assets","Accounts Payable", "Short Term Debt",
            "Other Current Liabilities", "Total Current Liabilities", "Total Debt", "Other Long-Term Liabilities",
                "Total Liabilities", "Noncontrolling Interest", "Preferred Stock","Shareholders' Equity", 
                "Total Liabilities and Equity"]

        self.tags = ['cash', 'netReceivables', 'inventory', 'shortTermInvestments', 'otherCurrentAssets', 'totalCurrentAssets',
         'propertyPlantAndEquipmentNet', 'goodWill', 'intangibleAssets','longTermInvestments', 'nonCurrentAssetsOther', 
         'nonCurrentAssetsTotal', 'accountsPayable', 'shortTermDebt','otherCurrentLiab',
          'totalCurrentLiabilities','longTermDebtTotal', 'nonCurrentLiabilitiesTotal',
           'noncontrollingInterestInConsolidatedEntity', 'preferredStockTotalEquity',
           'commonStock','retainedEarningsTotalEquity', "accumulatedOtherComprehensiveIncome",
           'totalStockholderEquity', 'liabilitiesAndStockholdersEquity']

        
        self.balance_tag_lookup = {}
        
        for i in range(1,len(self.tags)+1):
            self.balance_tag_lookup[i] = self.tags[i-1]
               
        self.balance_cell_dict = dict(zip(self.balance_items, self.balance_expressions))

    
    def interpret_value(self,key, json_data): # using this for balance sheet only so far
        # pass in the key from the cell_dict
        equation = self.balance_cell_dict[key] # key example: "Total Liabilities"

        result = 0

        operations = equation.split(sep = " ")
        for expression in operations:
            val = 0
            num = int(expression)
            raw = json_data[self.balance_tag_lookup[abs(num)]]
            if raw is not NoneType and raw is not None and raw != "null":
                val = float(json_data[self.balance_tag_lookup[abs(num)]])
            if num < 0:
                result += 0 if val is None else val*-1
            else:
                result += 0 if val is None else val
        
        return result
    
    def viewDicts(self):
        print(self.balance_cell_dict)
        print(self.balance_tag_lookup)



if __name__ == "__main__":
    test = Interpreter()

    test.viewDicts()




