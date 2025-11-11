#!/usr/bin/env python3
"""Quick script to check the structure of the editions API."""

import json
import requests

url = "https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions.json"
print(f"Fetching {url}...")
response = requests.get(url)
data = response.json()

print(f"\nData type: {type(data)}")
if isinstance(data, dict):
    print(f"Keys: {data.keys()}")
    print("\nFirst few items:")
    for key in list(data.keys())[:5]:
        print(f"  {key}: {data[key]}")
elif isinstance(data, list):
    print(f"Length: {len(data)}")
    print("\nFirst few items:")
    for item in data[:5]:
        print(f"  Type: {type(item)}, Value: {item}")

# Search for Somali
print("\n" + "="*60)
print("Searching for Somali editions...")
print("="*60)
if isinstance(data, dict):
    for key, value in data.items():
        if 'somali' in key.lower() or (isinstance(value, str) and 'somali' in value.lower()):
            print(f"Found: {key} = {value}")
