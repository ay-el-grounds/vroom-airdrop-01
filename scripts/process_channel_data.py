import os
import polars as pl
import json

def process_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    base = data["data"]["FarcasterChannels"]["FarcasterChannel"]

    processed_data = []

    participant_id = 1

    participant_channels = {}

    for channel in base:
        channel_id = channel["channelId"]
        user_data = channel["participants"]

        for participant_data in user_data:
            participant = participant_data["participant"]

            fid = int(participant.get("fid", 0))
            profile_name = participant.get("profileName", "")
            follower_count = int(participant.get("followerCount", 0))
            power_user = participant.get("isFarcasterPowerUser", False)

            user_address = participant.get("userAddress", "")
            user_associated_addresses = [
                addr for addr in participant.get("userAssociatedAddresses", []) if addr != user_address and addr.startswith("0x")
            ]

            if fid not in participant_channels:
                participant_channels[fid] = {
                    "id": participant_id,
                    "fid": fid,
                    "profileName": profile_name,
                    "followerCount": follower_count,
                    "isFarcasterPowerUser": power_user,
                    "userAddress": ','.join(user_associated_addresses),
                    "memberOf": set()
                }
                participant_id += 1

            participant_channels[fid]["memberOf"].add(channel_id)

    for participant in participant_channels.values():
        participant["memberOf"] = ','.join(sorted(participant["memberOf"]))
        processed_data.append(participant)

    return processed_data

def convert_to_csv(json_file_path, output_csv_path):
    processed_data = process_json_file(json_file_path)
    
    schema = {
        "id": pl.Int64,
        "fid": pl.Int64,
        "profileName": pl.Utf8,
        "followerCount": pl.Int64,
        "isFarcasterPowerUser": pl.Boolean,
        "userAddress": pl.Utf8,
        "memberOf": pl.Utf8
    }

    df = pl.DataFrame(processed_data, schema=schema)
    
    df.write_csv(output_csv_path)
    print(f"Data successfully processed and saved to {output_csv_path}.")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    raw_data_path = os.path.join(current_dir, "../data/raw/FarcasterChannels.json")
    processed_data_path = os.path.join(current_dir, "../data/processed/farcaster_channel_data.csv")
    
    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)

    convert_to_csv(raw_data_path, processed_data_path)
