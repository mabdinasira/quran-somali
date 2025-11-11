#!/usr/bin/env python3
"""
Query Qur'an Somali Translation
Supports multiple query modes:
  - Get entire surah by number
  - Get specific verse (surah:verse)
  - Get multiple specific verses
  - Get range of verses (surah:verse-verse)
  - Get range across surahs
"""

import json
import sys
import argparse

def load_quran(translation='jacob'):
    """Load the Quran JSON file for specified translation."""
    # Map short names to full filenames
    translation_files = {
        'jacob': 'quran_somali_AbdullahHasanJacob.json',
        'abduh': 'quran_somali_MahmudMuhammadAbduh.json',
        'abdu': 'quran_somali_ShaykhMahmoodMuhammadAbdu.json'
    }

    filename = translation_files.get(translation)
    if not filename:
        print(f"ERROR: Unknown translation '{translation}'")
        print("Available translations: jacob, abduh, abdu")
        sys.exit(1)

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: {filename} not found!")
        print("Make sure you're running this script from the quran_somali folder.")
        print("\nAvailable translations: jacob, abduh, abdu")
        sys.exit(1)
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON file!")
        sys.exit(1)

def get_surah_by_number(quran, surah_num):
    """Get entire surah by number (1-114)."""
    if not 1 <= surah_num <= 114:
        print(f"ERROR: Surah number must be between 1 and 114 (got {surah_num})")
        return None

    return quran[surah_num - 1]

def get_verse(quran, surah_num, verse_num):
    """Get a specific verse."""
    surah = get_surah_by_number(quran, surah_num)
    if not surah:
        return None

    if not 1 <= verse_num <= len(surah['verses']):
        print(f"ERROR: Verse {verse_num} not found in Surah {surah_num} (max: {len(surah['verses'])})")
        return None

    return {
        'surah_number': surah['surah_number'],
        'surah_name': surah['surah_name'],
        'verse': surah['verses'][verse_num - 1]
    }

def get_verse_range(quran, surah_num, start_verse, end_verse):
    """Get a range of verses from the same surah."""
    surah = get_surah_by_number(quran, surah_num)
    if not surah:
        return None

    if not 1 <= start_verse <= len(surah['verses']):
        print(f"ERROR: Start verse {start_verse} not found in Surah {surah_num}")
        return None

    if not 1 <= end_verse <= len(surah['verses']):
        print(f"ERROR: End verse {end_verse} not found in Surah {surah_num}")
        return None

    if start_verse > end_verse:
        print(f"ERROR: Start verse ({start_verse}) must be <= end verse ({end_verse})")
        return None

    return {
        'surah_number': surah['surah_number'],
        'surah_name': surah['surah_name'],
        'verses': surah['verses'][start_verse - 1:end_verse]
    }

def get_multiple_verses(quran, verse_refs):
    """Get multiple specific verses. verse_refs is list of (surah, verse) tuples."""
    results = []
    for surah_num, verse_num in verse_refs:
        verse_data = get_verse(quran, surah_num, verse_num)
        if verse_data:
            results.append(verse_data)
    return results

def print_surah(surah_data, show_verse_numbers=True):
    """Print formatted surah."""
    print("\n" + "=" * 80)
    print(f"SURAH {surah_data['surah_number']}: {surah_data['surah_name']}")
    print(f"Total Verses: {len(surah_data['verses'])}")
    print("=" * 80)

    for verse in surah_data['verses']:
        print()
        if show_verse_numbers:
            print(f"[Verse {verse['verse_number']}]")
        print(f"Arabic:  {verse['arabic_text']}")
        print(f"Somali:  {verse['somali_translation']}")
        print("-" * 80)

def print_verse(verse_data):
    """Print formatted single verse."""
    print("\n" + "=" * 80)
    print(f"SURAH {verse_data['surah_number']}: {verse_data['surah_name']}")
    print(f"Verse {verse_data['verse']['verse_number']}")
    print("=" * 80)
    print(f"\nArabic:  {verse_data['verse']['arabic_text']}")
    print(f"Somali:  {verse_data['verse']['somali_translation']}")
    print("=" * 80 + "\n")

def print_verses(data):
    """Print formatted verse range."""
    print("\n" + "=" * 80)
    print(f"SURAH {data['surah_number']}: {data['surah_name']}")
    if len(data['verses']) > 1:
        print(f"Verses {data['verses'][0]['verse_number']}-{data['verses'][-1]['verse_number']}")
    else:
        print(f"Verse {data['verses'][0]['verse_number']}")
    print("=" * 80)

    for verse in data['verses']:
        print()
        print(f"[Verse {verse['verse_number']}]")
        print(f"Arabic:  {verse['arabic_text']}")
        print(f"Somali:  {verse['somali_translation']}")
        print("-" * 80)
    print()

def print_multiple_verses(verses_data):
    """Print multiple verses from potentially different surahs."""
    print("\n" + "=" * 80)
    print(f"MULTIPLE VERSES ({len(verses_data)} total)")
    print("=" * 80)

    for verse_data in verses_data:
        print()
        print(f"Surah {verse_data['surah_number']}: {verse_data['surah_name']} - Verse {verse_data['verse']['verse_number']}")
        print(f"Arabic:  {verse_data['verse']['arabic_text']}")
        print(f"Somali:  {verse_data['verse']['somali_translation']}")
        print("-" * 80)
    print()

def parse_query(query_str):
    """
    Parse query string and return query type and parameters.

    Formats:
      - "5" -> Get entire surah 5
      - "5:10" -> Get surah 5, verse 10
      - "5:10-20" -> Get surah 5, verses 10-20
      - "5:10,5:15,5:20" -> Get multiple specific verses
    """
    query_str = query_str.strip()

    # Check for multiple verses (comma-separated)
    if ',' in query_str:
        verse_refs = []
        for part in query_str.split(','):
            part = part.strip()
            if ':' not in part:
                return None, "ERROR: Multiple verse format requires 'surah:verse' (e.g., 5:10,5:15)"

            try:
                surah, verse = part.split(':')
                verse_refs.append((int(surah), int(verse)))
            except ValueError:
                return None, f"ERROR: Invalid format in '{part}'"

        return ('multiple', verse_refs), None

    # Check for range (contains hyphen after colon)
    if ':' in query_str and '-' in query_str.split(':')[1]:
        try:
            surah_part, verse_part = query_str.split(':')
            surah_num = int(surah_part)
            start_verse, end_verse = verse_part.split('-')
            return ('range', (surah_num, int(start_verse), int(end_verse))), None
        except ValueError:
            return None, "ERROR: Invalid range format. Use 'surah:start-end' (e.g., 5:10-20)"

    # Check for single verse
    if ':' in query_str:
        try:
            surah, verse = query_str.split(':')
            return ('verse', (int(surah), int(verse))), None
        except ValueError:
            return None, "ERROR: Invalid verse format. Use 'surah:verse' (e.g., 5:10)"

    # Must be surah number only
    try:
        surah_num = int(query_str)
        return ('surah', surah_num), None
    except ValueError:
        return None, f"ERROR: Invalid query format: '{query_str}'"

def save_to_file(data, filename):
    """Save query results to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Saved to: {filename}\n")

def main():
    parser = argparse.ArgumentParser(
        description='Query Qur\'an Somali Translation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 1                    # Get entire Surah Al-Fatihah
  %(prog)s 2:255                # Get Ayat Al-Kursi (Surah 2, Verse 255)
  %(prog)s 18:1-10              # Get first 10 verses of Surah Al-Kahf
  %(prog)s "1:1,2:255,112:1-4"  # Get multiple specific verses (use quotes)
  %(prog)s 36 -o yaseen.json    # Save Surah Yaseen to file
  %(prog)s 67:1-5 --arabic-only # Show only Arabic text
  %(prog)s 55 --somali-only     # Show only Somali translation
  %(prog)s 1 -t abduh           # Use Mahmud Muhammad Abduh translation
  %(prog)s 1 -t abdu            # Use Shaykh Mahmood Muhammad Abdu translation
        """
    )

    parser.add_argument('query', help='Query: surah number, surah:verse, surah:verse-verse, or comma-separated verses')
    parser.add_argument('-o', '--output', help='Save results to JSON file')
    parser.add_argument('-t', '--translation',
                       choices=['jacob', 'abduh', 'abdu'],
                       default='jacob',
                       help='Translation to use: jacob (default/classic), abduh (modern), abdu (contemporary)')
    parser.add_argument('--arabic-only', action='store_true', help='Show only Arabic text')
    parser.add_argument('--somali-only', action='store_true', help='Show only Somali translation')
    parser.add_argument('--no-verse-numbers', action='store_true', help='Hide verse numbers')

    args = parser.parse_args()

    # Translation names for display
    translation_names = {
        'jacob': 'Abdullah Hasan Jacob (Classic)',
        'abduh': 'Mahmud Muhammad Abduh (Modern)',
        'abdu': 'Shaykh Mahmood Muhammad Abdu (Contemporary)'
    }

    # Load Quran
    quran = load_quran(args.translation)

    # Show translation being used if not the default
    if args.translation != 'jacob':
        print(f"\n[Using translation: {translation_names[args.translation]}]\n")

    # Parse query
    result, error = parse_query(args.query)
    if error:
        print(error)
        sys.exit(1)

    query_type, params = result

    # Execute query
    data = None
    if query_type == 'surah':
        data = get_surah_by_number(quran, params)
        if data:
            print_surah(data, show_verse_numbers=not args.no_verse_numbers)

    elif query_type == 'verse':
        surah_num, verse_num = params
        data = get_verse(quran, surah_num, verse_num)
        if data:
            print_verse(data)

    elif query_type == 'range':
        surah_num, start_verse, end_verse = params
        data = get_verse_range(quran, surah_num, start_verse, end_verse)
        if data:
            print_verses(data)

    elif query_type == 'multiple':
        verse_refs = params
        data = get_multiple_verses(quran, verse_refs)
        if data:
            print_multiple_verses(data)

    # Save to file if requested
    if data and args.output:
        save_to_file(data, args.output)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Qur'an Somali Translation Query Tool")
        print("=" * 60)
        print("\nAvailable Translations:")
        print("  jacob  - Abdullah Hasan Jacob (Classic) [DEFAULT]")
        print("  abduh  - Mahmud Muhammad Abduh (Modern)")
        print("  abdu   - Shaykh Mahmood Muhammad Abdu (Contemporary)")
        print("\nUsage examples:")
        print("  python3 query_quran.py 1                    # Get Surah Al-Fatihah")
        print("  python3 query_quran.py 2:255                # Get Ayat Al-Kursi")
        print("  python3 query_quran.py 18:1-10              # Get verses 1-10 of Surah 18")
        print('  python3 query_quran.py "1:1,2:255,112:1-4"  # Multiple verses (use quotes)')
        print("  python3 query_quran.py 36 -o yaseen.json    # Save to file")
        print("  python3 query_quran.py 1 -t abduh           # Use different translation")
        print("\nFor more options, use: python3 query_quran.py --help")
        print()
        sys.exit(0)

    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
