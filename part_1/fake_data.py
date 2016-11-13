from __future__ import division
from faker import Faker
from numpy import random
import os


def fake_receipts(customers):
    fake = Faker()
    data = []
    data.append(random.randint(0, customers))  # customer_id
    data.append(random.choice(['ocr', 'turk', 'admin', 'tlog']))  # validation type
    data.append(fake.random_int() / 100)  # total
    data.append(random.choice(['invalid_receipt', 'complete']))  # processing_state
    data.append(random.choice(['ocr_unmatched', 'turk_matched', 'turk_unmatched']))  # validations
    data.append(fake.latitude().to_eng_string())  # lat
    data.append(fake.longitude().to_eng_string())  # lon
    data.append(fake.date_time_this_year())  # created_at
    data.append(fake.random_int())  # store_id
    data.append(random.randint(1, 200))  # retailer_id
    data.append(random.randint(0, 4))  # turk submit count
    data.append(random.choice(['', '1']))  # invalid_receipt
    data.append(fake.random_int())  # ref number
    data.append(fake.random_int())  # appr_code
    data.append(fake.random_int())  # receipt_doce
    data.append(fake.name())  # cashier
    data.append(" ")  # payment_trans_id
    data.append(random.choice(['iphone', 'android']))  # phone_data
    data.append(random.choice(['', '1']))  # verified_total
    data.append(fake.date_time_this_year())  # pending acceptance at
    data.append(fake.date_time_this_year())  # pending_credit at
    data.append(random.choice(['', '1']))  # store_number
    data.append(" ")  # receipt_scan_contents
    data.append(random.choice(['', 'fraud']))  # fraud
    return tuple(data)


def fake_receipt_items(num_receipts):
    fake = Faker()
    data = [random.randint(0, 100)]  # product_number
    data.append(fake.random_int() / 100)  # price
    data.append(round(random.rand(), 2))  # discount
    data.append(random.randint(1, 15))  # quanitity
    data.append(random.choice(['ocr', 'ocr-old-exact', 'turk', 'ocr-exact', 'ocr-fuzz', 'admin', 'non_item', 'turk-multiple', 'tlog']))  # validation type
    data.append(random.randint(1, num_receipts))  # receipt_id
    data.append(fake.random_int())  # retailer_product_id
    data.append(fake.date_time_this_year())  # created at
    data.append(fake.date_time_this_year())  # matched with offer at
    data.append(fake.random_int())  # matched customer offer ir
    data.append(random.randint(1, 50))  # ext price
    data.append(random.choice(['', 'complete']))  # status
    return tuple(data)


def fake_customer():
    fake = Faker()
    data = [fake.email()]  # email
    data.append(fake.zipcode())  # zip
    data.append(random.choice(['m', 'f']))  # gender
    data.append(fake.random_int())  # household income
    data.append(random.randint(1, 5))  # children in house
    data.append(random.randint(1, 3))  # adults in house
    data.append(random.choice(['Hispanic', 'Black', 'Caucasian', 'Asian']))  # ehtnicity
    data.append(random.choice(['Highschool', 'University', 'Grad School']))  # education
    data.append(fake.random_int())  # udid
    data.append(fake.phone_number())  # phone number
    data.append(fake.address().split()[0])  # address
    data.append(fake.city())  # city
    data.append(fake.state())  # staet
    data.append(fake.first_name())  # first name
    data.append(fake.last_name())  # last name
    data.append(fake.date_time_this_year())  # last_login
    data.append(fake.date_time_this_year())  # created at
    data.append(fake.date_time_this_year())  # updated at
    data.append(fake.password())  # encrypted password
    data.append(os.urandom(6).encode('hex'))  # reset passwrod token
    data.append(fake.date_time_this_year())  # reset sent at
    data.append(fake.date_time_this_year())  # remember created at
    data.append(random.randint(1, 10))  # sign in count
    data.append(fake.date_time_this_year())  # current sign in at
    data.append(fake.date_time_this_year())  # last sign in at
    data.append(fake.ipv4())  # current sign in ip
    data.append(fake.ipv4())  # last sign in ip
    data.append(os.urandom(6).encode('hex'))  # authenticatin token
    data.append(random.choice(['0', '1']))  # active
    data.append(os.urandom(6).encode('hex'))  # confirmation token
    data.append(fake.date_time_this_year())  # confirmed at
    data.append(fake.date_time_this_year())  # confirmation sent at
    data.append(fake.email())  # unconfirmed email
    data.append(random.randint(1, 3))  # failed attempts
    data.append(os.urandom(6).encode('hex'))  # unlock token
    data.append(fake.date_time_this_year())  # locked at
    data.append(os.urandom(6).encode('hex'))  # invitation token
    data.append(fake.latitude().to_eng_string())  # lat
    data.append(fake.longitude().to_eng_string())  # lon
    data.append(fake.date())  # birth date
    data.append("default")  # roles
    data.append(fake.date_time_this_year())  # referall
    data.append(fake.date_time_this_year())  # last sweep
    data.append(fake.url())  # url
    data.append(fake.date_time_this_year())  # last notification
    data.append(14)  # online_delay
    data.append(random.choice(['verizon', 'att', 'sprint', 't-mobile']))  # carrier
    data.append(round(random.rand(), 2))  # credit conversion ratio
    data.append(" ")  # register source
    return tuple(data)
