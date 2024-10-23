import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup


def table_parser(table):
    data = {}
    rows = table.find_all('tr')
    title = table.find('caption').text.strip()

    for tr in rows:
        for th in tr.find_all('th'):
            data[th.text.strip()] = []

    for i, k in enumerate(data):
        for row in rows[1:]:
            cols = row.find_all('td')
            raw_value = cols[i].text.strip()
            if raw_value == 'N/A' or raw_value == 'NA':
                raw_value = ''

            value = raw_value.split()
            parsed_value = value[0].replace('%', '').replace(',', '') if len(value) else None

            if type(parsed_value) is str:
                try:
                    data[k].append(float(parsed_value))
                except:
                    pass
            else:
                data[k].append(parsed_value)

    if 'Source' in data:
        del data['Source']

    if 'Method' in data:
        del data['Method']

    return {
        'title': title,
        'data': data
    }


def table_render(data):
    title = data['title']
    index_key = next(iter(data['data']))
    df = pd.DataFrame(data['data'])
    df_melted = df.melt(id_vars=index_key, var_name='Platform', value_name='Percentage')
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_melted, x=index_key, y='Percentage', hue='Platform', marker='o')
    plt.title(title)
    plt.grid()


url = "https://en.wikipedia.org/wiki/Usage_share_of_operating_systems"
page = requests.get(url)

text = page.text
soup = BeautifulSoup(text, "html.parser")
tables = soup.find_all('table')

device_os = tables[1]
smartphone_shipments = tables[3]
mobile_web = tables[10]

device_os_data = table_parser(device_os)
smartphone_shipments_data = table_parser(smartphone_shipments)
mobile_web_data = table_parser(mobile_web)

table_render(device_os_data)
table_render(smartphone_shipments_data)
table_render(mobile_web_data)

plt.show()
