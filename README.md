# Cloudflare ddns

Execute to check relative public IP address and compare to update Cloudflare to sync change.

## Configuration

Create a lock environment file:
```
cp .env.example .env
```

Fill inn `API_TOKEN` and `ZONE_ID`. 

`API_TOKEN` should be generated from https://cloudflare.com/profile/generate-token and have access to all zones you wish to  update. 

`ZONE_ID` should be the zone where a `addr` A record that will be compared to actual address to see if it should be updated. 

## Setup

Prefered way to Build using dockerfile:
```
(sudo) docker build -t cloudflare-ddns .
docker run --rm cloudflare-dns
```

(Optional Installing python dependencies and running:)
```
virtualenv
source -p $(which python3) env/bin/activate

pip install -r requirements.txt
python main.py
```