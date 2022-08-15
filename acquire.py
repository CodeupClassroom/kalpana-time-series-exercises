'''
Module to encapsulate data acquisition.

Primary functions to use are

- get_store_item_demand_data()
- get_opsd_data()

If you want to get the individual datasets from the store item demand data you
can do so with

- get_items_data
- get_stores_dat
- get_sales_data
'''
import os
import requests
import pandas as pd

def get_store_data_from_api():
    response = requests.get('https://python.zgulde.net/api/v1/stores')
    data = response.json()
    stores = pd.DataFrame(data['payload']['stores'])
    stores = pd.DataFrame(stores)
    return stores

def get_items_data_from_api():
    domain = 'https://python.zgulde.net'
    endpoint = '/api/v1/items'
    items = []
    while True:
        url = domain + endpoint
        response = requests.get(url)
        data = response.json()
        print(f'\rGetting page {data["payload"]["page"]} of {data["payload"]["max_page"]}: {url}', end='')
        items.extend(data['payload']['items'])
        endpoint = data['payload']['next_page']
        if endpoint is None:
            break
    items = pd.DataFrame(items)
    return items

def get_sales_data_from_api():
    base_url = 'https://python.zgulde.net/api/v1/sales?page='
    sales = []
    url = base_url + str(1)
    response = requests.get(url)
    data = response.json()
    max_page = data['payload']['max_page']
    sales.extend(data['payload']['sales'])
    page_range = range(2, max_page + 1)

    for page in page_range:
        url = base_url + str(page)
        print(f'\rFetching page {page}/{max_page} {url}', end='')
        response = requests.get(url)
        data = response.json()
        sales.extend(data['payload']['sales'])
    sales = pd.DataFrame(sales)
    return sales

def get_stores_data():
    if os.path.exists('stores.csv'):
        return pd.read_csv('stores.csv')
    df = get_store_data_from_api()
    df.to_csv('stores.csv', index=False)
    return df

def get_items_data():
    if os.path.exists('items.csv'):
        return pd.read_csv('items.csv')
    df = get_items_data_from_api()
    df.to_csv('items.csv', index=False)
    return df

def get_sales_data():
    if os.path.exists('sales.csv'):
        return pd.read_csv('sales.csv')
    df = get_sales_data_from_api()
    df.to_csv('sales.csv', index=False)
    return df

def get_store_item_demand_data():
    sales = get_sales_data()
    stores = get_stores_data()
    items = get_items_data()

    sales = sales.rename(columns={'store': 'store_id', 'item': 'item_id'})
    df = pd.merge(sales, stores, how='inner', left_on='store_id', right_on='store_id')
    df = pd.merge(df, items, how='inner', left_on='item_id', right_on='item_id')

    return df

def get_opsd_data():
    if os.path.exists('opsd.csv'):
        return pd.read_csv('opsd.csv')
    df = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    df.to_csv('opsd.csv', index=False)
    return df