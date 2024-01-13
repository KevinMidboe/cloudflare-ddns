# Cloudflare ddns

Execute to check relative public IP address and compare to update Cloudflare to sync change.

## Configuration

Create a lock environment file:
```
cp .env.example .env
```

Fill inn `API_TOKEN` and `ZONE_ID`. 

`API_TOKEN` should be generated from [https://cloudflare.com/profile/generate-token](https://dash.cloudflare.com/profile/api-tokens) and have access to all zones you wish to  update. 

`ZONE_ID` should be the zone where a `addr` A record that will be compared to actual address to see if it should be updated. 

## Setup

Prefered way to Build using dockerfile:
```
(sudo) docker build -t cloudflare-ddns .
docker run --rm -it cloudflare-dns
```

(Optional Installing python dependencies and running:)
```
virtualenv
source -p $(which python3) env/bin/activate

pip install -r requirements.txt
python main.py
```

## Kubernetes

I am currenly running in kubernetes cluster as a cronjob checking periodically. Substitute `${IMAGE}` in `job.yml` manually or using CI script similar to: https://github.com/KevinMidboe/cloudflare-ddns/blob/main/.drone.yml#L49-L51. 

After job is created you also want to set environment variables from kubernetes secret, example `.kuberenetes/secret.yml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-env-values
  namespace: cloudflare-ddns
type: Opaque
data:
  API_KEY: BASE_64_ENCODED_CLOUDFLARE_API_KEY
  DDNS_ZONE: BASE64_ENCODED_CLOUDFLARE_ZONE_ID
```

```
kubectl apply -f .kuberenetes/secret.yml
```
