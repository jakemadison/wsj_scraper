from __future__ import print_function


def parse_csv():

    sql = ("insert into history.eod (symbolid, day, open, high, low, close, volume, aopen, ahigh, alow, "
           "aclose, avolume) values ((select symbolid from history.symbol where symbol = '{sym}'), '{day}', "
           "{open}, {high}, {low}, {close}, {vol}, {open}, {high}, {low}, {close}, {vol}); -- insert number: {i}")

    with open('./outfile - outfile.csv', 'rb') as f:
        for i, each_line in enumerate(f):
            if i == 0:
                continue

            rd = each_line.strip().split(',')

            day = rd[0]

            if day == '6/10/1983':
                # break
                pass

            openp = float(rd[3]) or 'null'
            high = float(rd[4]) or 'null'
            low = float(rd[5]) or 'null'
            close = float(rd[1]) or 'null'
            vol = int(rd[6]) or 'null'

            print(sql.format(sym='GIS', day=day, open=openp, high=high, low=low, close=close, vol=vol, i=i))


if __name__ == '__main__':
    parse_csv()