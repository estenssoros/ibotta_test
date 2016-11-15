from __future__ import division
import psutil
import os
from time import sleep
import psycopg2
from fake_data import *
from progressbar import ProgressBar, Counter, Bar


def test_for_process(process):
    processes = set()
    for i in psutil.pids():
        try:
            name = psutil.Process(i).name()
            processes.add(name)
        except:
            pass
    if process in processes:
        return True
    else:
        return False


def test_postgres():
    if not test_for_process('postgres'):
        try:
            os.system("open /Applications/Postgres.app")
            sleep(2)
        except Exception as e:
            print e
            raise ValueError('postgress server not detected')


def connect_postgres():
    conn = psycopg2.connect(dbname='ibotta', user='postgres', host='/tmp')
    curr = conn.cursor()
    return conn, curr


def clear_postgres():
    conn, curr = connect_postgres()
    with open('queries/create_tables.txt', 'r') as f:
        query = f.read()
    print 'tables created!'
    curr.execute(query)
    conn.commit()
    conn.close()


def populate_postgres():
    test_postgres()
    clear_postgres()
    conn, curr = connect_postgres()

    customers = 500
    receipts = customers * 5
    receipt_items = 8

    # reciept
    with open('queries/receipt_query.txt', 'r') as f:
        query = f.read()
    bar = ProgressBar()
    for i in bar(range(receipts)):
        curr.execute(query, fake_receipts(customers))
    conn.commit()

    # receipt items
    with open('queries/receipt_items_query.txt', 'r') as f:
        query = f.read()
    ttl_items = receipts * receipt_items
    bar = ProgressBar(widgets=[Counter(), '/{}'.format(ttl_items), Bar()])
    for i in bar(range(ttl_items)):
        curr.execute(query, fake_receipt_items(receipts))
    conn.commit()

    # customers
    with open('queries/customer_query.txt', 'r') as f:
        query = f.read()
    bar = ProgressBar()
    for i in bar(range(customers)):
        curr.execute(query, fake_customer())
    conn.commit()
    conn.close()


def main():
    populate_postgres()


if __name__ == '__main__':
    main()
