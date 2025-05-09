from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker('pt_BR')

def generate_customer_data(num_records=1000):
    data = []
    for _ in range(num_records):
        join_date = fake.date_between(start_date='-5y', end_date='today')
        data.append({
            "customer_id": fake.uuid4(),
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address().replace("\n", ", "),
            "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
            "join_date": join_date.strftime('%Y-%m-%d'),
            "last_purchase": fake.date_between(start_date=join_date, end_date='today').strftime('%Y-%m-%d'),
            "total_purchases": random.randint(0, 500),
            "total_spent": round(random.uniform(0, 10000), 2),
            "segment": random.choice(['A', 'B', 'C', 'D'])
        })
    return data

def save_to_txt(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        
        headers = data[0].keys()
        f.write("|".join(headers) + "\n")
        
        
        for row in data:
            values = [str(row[field]) for field in headers]
            f.write("|".join(values) + "\n")

if __name__ == "__main__":
    print("Generating customer data...")
    customer_data = generate_customer_data(5000)
    save_to_txt(customer_data, "data/raw/customers_20230515.txt")
    print("Data generated successfully in data/raw/customers_20230515.txt")