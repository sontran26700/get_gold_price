import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def get_gold_price(date_str):
    url = f'https://www.24h.com.vn/gia-vang-hom-nay-c425.html?d={date_str}'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("kết nối thành công - stastus code : ", response.status_code)
            soup = BeautifulSoup(response.text, 'html.parser')
            # TIM BANG CHUA GIA TRI CUA VANG
            gold_table = soup.find('table', class_='gia-vang-search-data-table')
            # TAO MANG LUU GIA TRI
            gold_price = []
            # PHAN TICH DE LAY THONG TIN GIA VANG
            rows = gold_table.find_all('tr')
            for row in rows[1:]:
                cells = row.find_all('td')
                
                filtercell = []
                
                for cell in cells:
                    if cell.find('span', class_=['colorRed', 'colorGreen']):
                        continue
                    filtercell.append(cell)
                
                gold_name = filtercell[0].text.strip()
                gold_buy_price = filtercell[1].text.strip()
                gold_buy_sell = filtercell[2].text.strip()
            
                # append vao mang da tao
                gold_price.append({'date': date_str, 'name': gold_name, 'buy_price': gold_buy_price, 'sell_price': gold_buy_sell})
            return gold_price
        else:
            print("kết nối không thành công - stastus code : ", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print(e)
        return None

def get_gold_prices_month(year, month):
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    current_date = start_date
    all_gold_prices = []
    
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        gold_price = get_gold_price(date_str)
        if gold_price:
            all_gold_prices.extend(gold_price)
        current_date += timedelta(days=1)
    return all_gold_prices

year = 2023
month = 5
gold_prices = get_gold_prices_month(year, month)

if gold_prices:
    print("Thông tin giá vàng trong tháng {}/{}:".format(month, year))
    for gold in gold_prices:
        print(gold['date'], gold['name'], "-", "Mua:", gold['buy_price'], "-", "Bán:", gold['sell_price'])
        
    csv_file = f'gold_prices_{year}_{month}.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['date', 'name', 'buy_price', 'sell_price']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for gold in gold_prices:
            writer.writerow(gold)

    print(f"Dữ liệu đã được xuất vào file '{csv_file}'.")