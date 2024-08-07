# $VROOM Airdrop

This repository contains all the necessary scripts and data for the $VROOM airdrop. The airdrop targets specific addresses based on their activity on Farcaster channels and ownership of certain NFTs.

## Repository Structure

- **data/**: Contains raw and processed data files.
- **notebooks/**: Jupyter notebooks for data processing and analysis.
- **scripts/**: Python scripts for data processing and analysis.
- **results/**: Contains results and plots.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/$VROOM-Airdrop.git
cd $VROOM-Airdrop
```

2. Install required packages:
```bash
Copy code
pip install -r requirements.txt
```
## Acquireing Raw Data

All queries were run on Airstack on the following Farcaster channels:
- cars
- drift
- f1
- velocity vibes

### Get Participants of Farcaster Channels
You can fetch all the followers of a Farcaster channel by using FarcasterChannelParticipants by providing the channel ID (e.g. /farcaster channel ID is "farcaster") to $channelId variable and specify channelActions to "follow" value:

```
query getFarcasterChannels {
  FarcasterChannels(
    input: {blockchain: ALL, filter: {channelId: {_in: ["cars", "drift", "f1", "velocityvibes"]}}}
  ) {
    FarcasterChannel {
      channelId
      followerCount
      participants {
        participant {
          userAddress
          profileName
          fid: userId
          userAssociatedAddresses
          followerCount
          followingCount
          isFarcasterPowerUser
        }
        lastActionTimestamp
        lastCastedTimestamp
        lastRepliedTimestamp
        channelActions
        lastFollowedTimestamp
      }
    }
  }
}
```

## Remaining items
- [ ] create a graph of the scripts and dataflow
