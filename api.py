import requests

url = "https://api.themoviedb.org/3/authentication"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ZWM1Y2FlNDBlODMzOTgyMjA1M2UzYTM0MzY0MTlmZiIsIm5iZiI6MTczMjA2OTQ3MS40OTA3MTA3LCJzdWIiOiI2NzNkNDI4ZTg3OTE3MDc4ZDAxMDc5MGUiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.nODIzarm1UhM-_6SsEzOcyIx2gYTnrzxb3nYss7zdko"
}

response = requests.get(url, headers=headers)

print(response.text)