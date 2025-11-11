#!/usr/bin/env python3
"""
Fetch complete Qur'an in Somali (Abdullah Hasan Jacob translation) with Arabic text.
Outputs JSON in the required format with all 114 surahs.
"""

import json
import requests
import sys

def fetch_json(url):
    """Fetch JSON data from URL."""
    print(f"Fetching: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_surah_names():
    """Get Arabic surah names."""
    # Fetch info about surahs
    url = "https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/info.json"
    data = fetch_json(url)

    surah_names = {}
    for surah in data.get('chapters', []):
        surah_names[surah['chapter']] = surah['name']

    return surah_names

def main():
    print("="*70)
    print("Qur'an Somali Translation Fetcher")
    print("Translation: Abdullah Hasan Jacob (Classic)")
    print("="*70)

    # Available Somali editions
    somali_editions = {
        '1': {'key': 'som-abdullahhasanja', 'name': 'Abdullah Hasan Jacob (Classic)'},
        '2': {'key': 'som-mahmudmuhammada', 'name': 'Mahmud Muhammad Abduh'},
        '3': {'key': 'som-shaykhmahmoodmu', 'name': 'Shaykh Mahmood Muhammad Abdu'}
    }

    print("\nAvailable Somali translations:")
    for num, info in somali_editions.items():
        print(f"  {num}. {info['name']}")

    # Default to classic translation (Abdullah Hasan Jacob)
    selected = '1'
    edition_key = somali_editions[selected]['key']
    edition_name = somali_editions[selected]['name']

    print(f"\nUsing: {edition_name}")

    # Fetch Arabic text
    print("\n" + "-"*70)
    print("Step 1: Fetching Arabic text...")
    print("-"*70)
    arabic_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/ara-quransimple.json"
    arabic_data = fetch_json(arabic_url)

    # Fetch Somali translation
    print("\n" + "-"*70)
    print("Step 2: Fetching Somali translation...")
    print("-"*70)
    somali_url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{edition_key}.json"
    somali_data = fetch_json(somali_url)

    # Fetch surah names
    print("\n" + "-"*70)
    print("Step 3: Fetching surah names...")
    print("-"*70)
    surah_names = get_surah_names()

    # Format the data
    print("\n" + "-"*70)
    print("Step 4: Formatting data...")
    print("-"*70)

    formatted_quran = []

    # Data is a flat list of verses with chapter/verse numbers
    arabic_verses_list = arabic_data['quran']
    somali_verses_list = somali_data['quran']

    # Create dictionaries indexed by chapter and verse
    arabic_dict = {}
    for verse in arabic_verses_list:
        chapter = verse['chapter']
        verse_num = verse['verse']
        if chapter not in arabic_dict:
            arabic_dict[chapter] = {}
        arabic_dict[chapter][verse_num] = verse['text']

    somali_dict = {}
    for verse in somali_verses_list:
        chapter = verse['chapter']
        verse_num = verse['verse']
        if chapter not in somali_dict:
            somali_dict[chapter] = {}
        somali_dict[chapter][verse_num] = verse['text']

    total_verses = 0

    # Process all 114 surahs
    for surah_num in range(1, 115):
        surah_name = surah_names.get(surah_num, f"Surah {surah_num}")

        verses = []

        # Get all verses for this surah
        if surah_num in arabic_dict:
            max_verse = max(max(arabic_dict.get(surah_num, {}).keys() or [0]),
                          max(somali_dict.get(surah_num, {}).keys() or [0]))

            for verse_num in range(1, max_verse + 1):
                arabic_text = arabic_dict.get(surah_num, {}).get(verse_num, "")
                somali_text = somali_dict.get(surah_num, {}).get(verse_num, "")

                verses.append({
                    "verse_number": verse_num,
                    "arabic_text": arabic_text,
                    "somali_translation": somali_text
                })
                total_verses += 1

            formatted_quran.append({
                "surah_number": surah_num,
                "surah_name": surah_name,
                "verses": verses
            })

            print(f"  Processed Surah {surah_num}: {surah_name} ({len(verses)} verses)")
        else:
            print(f"  WARNING: Surah {surah_num} not found in data!")

    # Save to file
    print("\n" + "-"*70)
    print("Step 5: Saving to file...")
    print("-"*70)

    output_file = "quran_somali_complete.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(formatted_quran, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*70}")
    print("SUCCESS!")
    print("="*70)
    print(f"File saved: {output_file}")
    print(f"Total Surahs: {len(formatted_quran)}/114")
    print(f"Total Verses: {total_verses}")
    print(f"Translation: {edition_name}")
    print("="*70)

    # Show sample
    if formatted_quran:
        print("\nSample - Al-Fatihah, Verse 1:")
        print("-"*70)
        sample = formatted_quran[0]['verses'][0]
        print(f"Arabic: {sample['arabic_text']}")
        print(f"Somali: {sample['somali_translation']}")
        print("-"*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
