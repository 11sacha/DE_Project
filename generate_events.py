from confluent_kafka import Producer
import json
import time
import random
from faker import Faker

fake = Faker()

KAFKA_BROKER = 'localhost:9092'  
IMPRESSION_TOPIC = 'ad_impressions'
CLICK_TOPIC = 'ad_clicks'

producer = Producer({'bootstrap.servers': KAFKA_BROKER})

campaign_ids = ['camp-1', 'camp-2']
ads = ['ad-1', 'ad-2']
devices = ['mobile', 'desktop']
browsers = ['chrome', 'firefox', 'safari']

def create_impression():
    timestamp = int(time.time() * 1000)
    impression_id = f"imp-{random.randint(10000,99999)}"
    return {
        "impression_id": impression_id,
        "user_id": fake.uuid4(),
        "campaign_id": random.choice(campaign_ids),
        "ad_id": random.choice(ads),
        "device_type": random.choice(devices),
        "browser": random.choice(browsers),
        "event_timestamp": timestamp,
        "cost": round(random.uniform(0.01, 0.10), 2)
    }

def create_click(impression_id, user_id):
    timestamp = int(time.time() * 1000) + random.randint(0, 30000)
    return {
        "click_id": f"click-{random.randint(10000,99999)}",
        "impression_id": impression_id,
        "user_id": user_id,
        "event_timestamp": timestamp
    }

while True:
    
    imp = create_impression()
    producer.produce(IMPRESSION_TOPIC, key=imp["impression_id"], value=json.dumps(imp))
    print(f"Sent impression: {imp['impression_id']}")

    
    if random.random() < 0.5:
        click = create_click(imp["impression_id"], imp["user_id"])
        producer.produce(CLICK_TOPIC, key=click["click_id"], value=json.dumps(click))
        print(f"Sent click: {click['click_id']}")

    producer.flush()
    time.sleep(1)

