import json
import os

def count_unique_user_addresses(raw_data_path):
    with open(raw_data_path, 'r') as file:
        data = json.load(file)
    
    user_addresses = set()
    for channel in data['data']['FarcasterChannels']['FarcasterChannel']:
        for participant in channel['participants']:
            user_address = participant['participant']['userAddress']
            user_addresses.add(user_address)
    
    return len(user_addresses)

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    raw_data_path = os.path.join(current_dir, "../data/raw/FarcasterChannels.json")
    
    unique_count = count_unique_user_addresses(raw_data_path)
    print(f'Number of unique user addresses: {unique_count}')
