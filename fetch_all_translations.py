#!/usr/bin/env python3
"""
Fetch all three Somali Qur'an translations and save them with proper labels.
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
    url = "https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/info.json"
    data = fetch_json(url)
    surah_names = {}
    for surah in data.get('chapters', []):
        surah_names[surah['chapter']] = surah['name']
    return surah_names

def format_quran_json(arabic_data, translation_data, surah_names):
    """Format the Quran data according to the required structure."""
    formatted_quran = []

    arabic_chapters = arabic_data['quran']
    translation_chapters = translation_data['quran']

    # Create dictionaries indexed by chapter and verse
    arabic_dict = {}
    for verse in arabic_chapters:
        chapter = verse['chapter']
        verse_num = verse['verse']
        if chapter not in arabic_dict:
            arabic_dict[chapter] = {}
        arabic_dict[chapter][verse_num] = verse['text']

    translation_dict = {}
    for verse in translation_chapters:
        chapter = verse['chapter']
        verse_num = verse['verse']
        if chapter not in translation_dict:
            translation_dict[chapter] = {}
        translation_dict[chapter][verse_num] = verse['text']

    total_verses = 0

    # Process all 114 surahs
    for surah_num in range(1, 115):
        surah_name = surah_names.get(surah_num, f"Surah {surah_num}")
        verses = []

        if surah_num in arabic_dict:
            max_verse = max(max(arabic_dict.get(surah_num, {}).keys() or [0]),
                          max(translation_dict.get(surah_num, {}).keys() or [0]))

            for verse_num in range(1, max_verse + 1):
                arabic_text = arabic_dict.get(surah_num, {}).get(verse_num, "")
                translation_text = translation_dict.get(surah_num, {}).get(verse_num, "")

                verses.append({
                    "verse_number": verse_num,
                    "arabic_text": arabic_text,
                    "somali_translation": translation_text
                })
                total_verses += 1

            formatted_quran.append({
                "surah_number": surah_num,
                "surah_name": surah_name,
                "verses": verses
            })

            print(f"  Processed Surah {surah_num}: {surah_name} ({len(verses)} verses)")

    return formatted_quran, total_verses

def main():
    translations = [
        {
            'key': 'som-abdullahhasanja',
            'name': 'Abdullah Hasan Jacob',
            'filename': 'quran_somali_AbdullahHasanJacob.json',
            'description': 'Classic Somali Translation'
        },
        {
            'key': 'som-mahmudmuhammada',
            'name': 'Mahmud Muhammad Abduh',
            'filename': 'quran_somali_MahmudMuhammadAbduh.json',
            'description': 'Modern Somali Translation'
        },
        {
            'key': 'som-shaykhmahmoodmu',
            'name': 'Shaykh Mahmood Muhammad Abdu',
            'filename': 'quran_somali_ShaykhMahmoodMuhammadAbdu.json',
            'description': 'Contemporary Somali Translation'
        }
    ]

    print("=" * 80)
    print("FETCHING ALL SOMALI QUR'AN TRANSLATIONS")
    print("=" * 80)
    print()

    # Fetch Arabic text once
    print("Fetching Arabic text...")
    print("-" * 80)
    arabic_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/ara-quransimple.json"
    arabic_data = fetch_json(arabic_url)
    print("✓ Arabic text loaded\n")

    # Fetch surah names once
    print("Fetching surah names...")
    print("-" * 80)
    surah_names = get_surah_names()
    print("✓ Surah names loaded\n")

    # Fetch each translation
    for idx, translation in enumerate(translations, 1):
        print("=" * 80)
        print(f"TRANSLATION {idx}/3: {translation['name']}")
        print(f"Description: {translation['description']}")
        print("=" * 80)

        translation_url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{translation['key']}.json"
        translation_data = fetch_json(translation_url)

        print("\nFormatting data...")
        print("-" * 80)
        formatted_quran, total_verses = format_quran_json(arabic_data, translation_data, surah_names)

        output_file = translation['filename']
        print(f"\nSaving to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(formatted_quran, f, ensure_ascii=False, indent=2)

        print(f"✓ Saved: {output_file}")
        print(f"  Translator: {translation['name']}")
        print(f"  Total Surahs: {len(formatted_quran)}/114")
        print(f"  Total Verses: {total_verses}")
        print()

    print("=" * 80)
    print("ALL TRANSLATIONS DOWNLOADED SUCCESSFULLY!")
    print("=" * 80)
    print("\nFiles created:")
    print("  1. quran_somali_AbdullahHasanJacob.json")
    print("     Abdullah Hasan Jacob (Classic)")
    print("  2. quran_somali_MahmudMuhammadAbduh.json")
    print("     Mahmud Muhammad Abduh (Modern)")
    print("  3. quran_somali_ShaykhMahmoodMuhammadAbdu.json")
    print("     Shaykh Mahmood Muhammad Abdu (Contemporary)")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("ERROR: requests module not installed")
        print("Please run: pip3 install requests")
        sys.exit(1)

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
