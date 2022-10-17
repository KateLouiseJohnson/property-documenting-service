# property-documenting-service

A property documenting service that exposes an api for maintaining property data

### Swimlanes diagram
I like having a high level view of the flow of a service. So I created a swimlanes diagram which can be viewed [here](https://swimlanes.io/#vVVNb+IwED3jX+Fz1FUPvUWrIgqhsKKACD3sCUwy0EhOnNpOpajLf99xTCBJAxtpV+tDkGbGb57n46EjzcGlSylSkDqnIxFkMSQ6Sg7UB/kRBUDIxqWO47MPY0zLyJBp5jiEDHmE8fTbYxmPaAt/Te9PkREoQhKhwSWO88NfzOmS5Vyw0HUcSrbbLfkklGYKpBeziLtUaYmJ7tCo8xTRBsvBav3izdebp9fpbDSdP9Nf1MefmbcZD16ms5+byeLV9+5Ij4WhBKVcaiB7CASgq4CUWts8i3cg6x6WMqnN062zX/fuuRDGlhROawsindejUqE040MRQjMr0w1TILJEy9zGjjx80mCNn+HEuI/mwzSG7zIN5XvODJ+yiIeI1LcOdJ0PPTFc7F+TSKsG40rY0RJDFA5jFkc8nwhsQgtkT71nTMJYCM0O0EBsPzsIpRCxGppHdrhxtK4Dk2UGzrEYn/TKjQBLYat/Qr4WWKP+Jx5mSFW9S1+IljxDSCo86xX750mtWYOULID/m7b4BCI2Y6cqO3EsNpecVt5s/xJn/yANaLH+NZ2gIWjcbRSCMqqmFz6uR6YomlORKLgFu484pEy//QWi/9CkaEARyX/ojGFFryXGSiUwGbx1Vctnr4NY4t1SKt8zkHm5pqdjZa3f2tCq5LVHmFVq91wE7crNi4r1v8rY+ZzV/Yxy8R5vD1NRHVUU9EqvV7catKp3ZgWYHTr/kTVac/99Onq8xdP6u7M0o1i52BjATg/7DQ==).

## Startup

```bash
pip install -r requirements.txt
docker compose up
uvicorn run:app --reload
```

### Handy curl command for local testing

```bash
curl --request POST \
  --url http://127.0.0.1:8000/properties \
  --header 'Content-Type: multipart/form-data' \
  --form 'form={
	"address": { "street": "street name" }
}' \
  --form 'files=@<YOUR_FILEPATH_HERE>' \
  --form 'files=@<YOUR_FILEPATH_HERE>'
```

## Quick links to helpful docs

- [FastAPI](https://fastapi.tiangolo.com/)
- [Psycopg](https://www.psycopg.org/docs/)