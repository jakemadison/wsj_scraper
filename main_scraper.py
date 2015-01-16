from __future__ import print_function
from bs4 import BeautifulSoup
import sys
from datetime import datetime, timedelta
import time
import requests
import pickle


failed_dates = []


# Temp Functions to test response content with:
def pickle_content(content):
    with open('./temp_parsed_page.data', 'wb') as pickle_file:
        pickle.dump(content, pickle_file)

    return True


def get_pickled_content():
    with open('./temp_parsed_page.data', 'r') as pickle_file:
        file_contents = pickle.load(pickle_file)

    return file_contents


def get_basic_prices(parsed_page):

    basic_prices = {}

    # get the price:
    font_array = parsed_page.findAll('font', {"color": "000000", "size": '1'})

    for i, each in enumerate(font_array):
        if i == 0:
            continue
        if i == 5:
            break

        if i == 1:  # get high data
            try:
                high = float(each.get_text().strip())
                basic_prices['high'] = high
            except Exception, e:
                basic_prices['high'] = None
                continue

        if i == 2:  # get low data
            try:
                low = float(each.get_text().strip())
                basic_prices['low'] = low
            except Exception, e:
                basic_prices['low'] = None
                continue

        if i == 3:  # get vol data
            try:
                volume = int(each.get_text().strip().replace(',', ''))
                basic_prices['volume'] = volume
            except Exception, e:
                basic_prices['volume'] = None
                continue

        if i == 4:  # get price data
            try:
                price = float(each.find('b').get_text().strip())
                basic_prices['price'] = price
            except Exception, e:
                basic_prices['price'] = None
                continue

    return basic_prices




def parse_page_response(response):

    parsed_page = BeautifulSoup(response.content, from_encoding=response.encoding)

    basic_prices = get_basic_prices(parsed_page)

    print('\n\n basic prices: {0}'.format(basic_prices))

    return True


def get_page(date):

    """take in a date, create a link, get request to give us the html content"""

    base_url = ('http://custom.gtm.idmanagedsolutions.com/custom/wsjie/wsjbb-historical.asp'
                '?symb=gis&close_date={0}&x=0&y=0')
    base_url = base_url.format(date)

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    print('attempting to get page now: {0}'.format(base_url))

    try:
        resp = requests.get(base_url, headers=headers, timeout=10)
        resp.raise_for_status()  # <- no-op if status!=200

    except Exception, e:
        print('i died while requesting the link :<', e)
        failed_dates.append(date)
        return False

    return resp


def date_generator(start_date, end_date):

    """Simple Generator to keep getting the next day until end date.
        Might as well just return them as strings here, hey?
    """

    while True:

        if start_date <= end_date:
            if start_date.weekday() > 4:  # skip weekends.
                start_date += timedelta(1)
                continue

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
        start_date = '01/02/1970'
        end_date = '01/01/1984'

    start_date = datetime.strptime(start_date, '%m/%d/%Y')
    end_date = datetime.strptime(end_date, '%m/%d/%Y')
    print('received the following symbol: {0}, start: {1}, end: {2}'.format(symbol, start_date, end_date))

    responses = get_pickled_content()

    for i, each_response in enumerate(responses):
        if i == 0:
            continue
        parse_page_response(each_response)






    # responses = []

    # for i, each_day in enumerate(date_generator(start_date, end_date)):
    #     print('processing call number: {0}'.format(i))
        # request_response = get_page(each_day)
        # responses.append(request_response)
        # time.sleep(1)

        # parse_page_response()

        # if i == 10:
            # pickle_content(responses)
            # break
        # time.sleep(1)


if __name__ == '__main__':
    main()
    print('........ done!')