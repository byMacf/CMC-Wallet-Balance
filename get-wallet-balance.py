#!/usr/bin/python3

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def GetWalletBalance():
    TotalWalletValue = 0

    CoinsAndBalances = GetCoinsAndBalances('#FILE PATH TO balance.json HERE#')

    ValueOfCoinsInGBP = {Symbol:ConvertCoinAmountToGBP(Symbol, AmountHeld) for Symbol, AmountHeld in CoinsAndBalances.items()}

    for Symbol, CoinAmountHeldTotalValue in ValueOfCoinsInGBP.items():
        TotalWalletValue = TotalWalletValue + CoinAmountHeldTotalValue[1]

    print('\nYour total wallet balance is £{:.2f}\n'.format(TotalWalletValue))
    print('Breakdown:\n')
    for Symbol, CoinAmountHeldTotalValue in ValueOfCoinsInGBP.items():
        print('{}: £{:.2f}'.format(Symbol, CoinAmountHeldTotalValue[1]))

def GetCoinsAndBalances(file):
    with open(file) as BalanceData:
        CoinsAndAmountHeld = json.load(BalanceData)

    CoinsAndBalancesDict = {Symbol:Balance['AmountHeld'] for Symbol, Balance in CoinsAndAmountHeld['Balance'].items()}
    
    return CoinsAndBalancesDict
                
def ConvertCoinAmountToGBP(symbol, amount):
    endpoint = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'

    parameters = {
    'amount': amount,
    'symbol': symbol,
    'convert': 'GBP'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '#YOUR API KEY HERE#',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(endpoint, params=parameters)
        data = json.loads(response.text)
        Symbol = symbol
        CoinValue = data['data']['quote']['GBP']['price']
        return Symbol, CoinValue
    except (ConnectionError, Timeout, TooManyRedirects) as ErrorMesage:
        return ErrorMessage

GetWalletBalance()