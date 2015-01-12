from __future__ import print_function
from bs4 import BeautifulSoup
import sys
from datetime import datetime, timedelta
import time


def date_generator(start_date, end_date):

    """Simple Generator to keep getting the next day until end date.
        Might as well just return them as strings here, hey?
    """

    while True:
        if start_date <= end_date:
            yield start_date.strftime('%m/%d/%Y')
            start_date += timedelta(1)

        else:
            raise StopIteration


def main():

    """
        # Problem Definition:
        #1:36> still trying to get the historical data for GIS between 1970 and 1983
        #1:36> turns out the Wall Street Journal has it through Interactive Data
        #1:36> Catch is.... http://custom.gtm.idmanagedsolutions.com/custom/wsjie/
        # wsjbb-historical.asp?symb=gis&close_date=1%2F2%2F1970&x=0&y=0
        #1:36> they only show one day at a time
        #1:37> any script we can write to scam that data from them?
            take in a symbol, start date, enddate, and scrape that shit from wsj
    """

    # parse out init params:
    print('entered function main....')

    if len(sys.argv) == 4:
        symbol = sys.argv[1]
        start_date = sys.argv[2]
        end_date = sys.argv[3]

    else:
        symbol = 'GIS'
        start_date = '01/01/1970'
        end_date = '01/01/1984'

    start_date = datetime.strptime(start_date, '%m/%d/%Y')
    end_date = datetime.strptime(end_date, '%m/%d/%Y')
    print('received the following symbol: {0}, start: {1}, end: {2}'.format(symbol, start_date, end_date))

    # for each_day in date_generator(start_date, end_date):
    #     print(each_day)
    #     time.sleep(1)


if __name__ == '__main__':
    main()