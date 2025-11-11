# Qur'an Somali Translation / Tarjumaadda Soomaaliga ee Quraanka

**Three complete Somali translations of the Holy Quran with Arabic text in JSON format**

Somali translations of the Quran | Quraan Soomaali | القرآن الصومالية | Al-Quran Somali | Mushaf Somali

[![Surahs](https://img.shields.io/badge/Surahs-114-green.svg)](.) [![Verses](https://img.shields.io/badge/Verses-6236-blue.svg)](.) [![Translations](https://img.shields.io/badge/Translations-3-orange.svg)](.) [![Language](https://img.shields.io/badge/Language-Somali-blue.svg)](.)

---

## 🔍 Keywords / Search Terms

**Quran Somali**, Quraan Soomaali, Quran translation Somali, Al-Quran Somali, Koran Somali, القرآن الصومالية, Mushaf Somali, Somali Tafseer, Tafsiir Soomaali, Somali Quran, Soomaali Quraan, Islamic texts Somali, Somalia Quran, Quraanka Soomaaliga, Somali Islamic resources, Holy Quran Somali language, Quran in Somali script

---

## 📊 Translation Metadata

-   **Language:** Somali (ISO 639-1: so, ISO 639-3: som)
-   **Script:** Latin (Somali orthography)
-   **Format:** JSON (UTF-8 encoded)
-   **Region:** Somalia, Somaliland, Djibouti, Ethiopian Somali region, Kenyan Somali region
-   **Speakers:** ~20+ million native speakers
-   **Translators:** Abdullah Hassan Jacob, Mahmud Muhammad Abduh, Shaykh Mahmood Muhammad Abdu
-   **Content:** Complete Quran - 114 Surahs, 6,236 Verses
-   **Includes:** Arabic text + Somali translation

---

## 📖 What's Included

This repository contains **THREE complete Somali translations** of the Qur'an:

1. **Abdullah Hasan Jacob** (Classic) - Most widely used traditional translation
2. **Mahmud Muhammad Abduh** (Modern) - Contemporary language for modern readers
3. **Shaykh Mahmood Muhammad Abdu** (Contemporary) - Alternative modern approach

Each translation includes:

-   ✅ All 114 surahs
-   ✅ All 6,236 verses
-   ✅ Arabic text (simplified Unicode)
-   ✅ Somali translation
-   ✅ Proper JSON formatting
-   ✅ UTF-8 encoding

**Total Size:** ~8 MB

---

## 🚀 Quick Start

```bash
# Navigate to folder
cd ~/Desktop/quran_somali

# Get Al-Fatihah (classic translation)
python3 query_quran.py 1

# Get Ayat Al-Kursi
python3 query_quran.py 2:255

# Use modern translation
python3 query_quran.py 1 -t abduh

# Compare translations
python3 query_quran.py 112:1
python3 query_quran.py 112:1 -t abduh
python3 query_quran.py 112:1 -t abdu
```

---

## 📁 Files

### Data Files (JSON)

| File                                          | Translator                   | Style        | Size   |
| --------------------------------------------- | ---------------------------- | ------------ | ------ |
| `quran_somali_AbdullahHasanJacob.json`        | Abdullah Hasan Jacob         | Classic      | 2.7 MB |
| `quran_somali_MahmudMuhammadAbduh.json`       | Mahmud Muhammad Abduh        | Modern       | 2.6 MB |
| `quran_somali_ShaykhMahmoodMuhammadAbdu.json` | Shaykh Mahmood Muhammad Abdu | Contemporary | 2.6 MB |

### Scripts

-   **`query_quran.py`** - Main query tool (supports all 3 translations)
-   **`fetch_all_translations.py`** - Download all translations from API
-   **`fetch_quran.py`** - Download single translation
-   **`check_editions.py`** - Check available translations

### Documentation

-   **`README.md`** - This file (project overview)
-   **`QUICK_START.txt`** - Quick reference guide
-   **`QUERY_GUIDE.txt`** - Complete query tool documentation
-   **`INDEX.txt`** - Project index

---

## 💻 Usage

### Query Tool

The `query_quran.py` script provides easy access to the Qur'an data:

```bash
# Get entire surah
python3 query_quran.py 1

# Get specific verse
python3 query_quran.py 2:255

# Get verse range
python3 query_quran.py 18:1-10

# Get multiple verses (use quotes!)
python3 query_quran.py "1:1,2:255,112:1-4"

# Use different translation
python3 query_quran.py 1 -t abduh     # Modern
python3 query_quran.py 1 -t abdu      # Contemporary

# Save to file
python3 query_quran.py 36 -o yaseen.json

# Save with specific translation
python3 query_quran.py 36 -o yaseen_modern.json -t abduh
```

### Translation Options

| Flag    | Translator                   | Style        | Default |
| ------- | ---------------------------- | ------------ | ------- |
| `jacob` | Abdullah Hasan Jacob         | Classic      | ✓       |
| `abduh` | Mahmud Muhammad Abduh        | Modern       |         |
| `abdu`  | Shaykh Mahmood Muhammad Abdu | Contemporary |         |

---

## 📋 JSON Structure

All three JSON files use identical structure:

```json
[
    {
        "surah_number": 1,
        "surah_name": "Al-Faatiha",
        "verses": [
            {
                "verse_number": 1,
                "arabic_text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                "somali_translation": "Ku Billaabasho Magaca Allaah..."
            }
        ]
    }
]
```

---

## 👨‍💻 Programming Examples

### Python

```python
import json

# Load classic translation
with open('quran_somali_AbdullahHasanJacob.json', 'r', encoding='utf-8') as f:
    quran_classic = json.load(f)

# Load modern translation
with open('quran_somali_MahmudMuhammadAbduh.json', 'r', encoding='utf-8') as f:
    quran_modern = json.load(f)

# Get Al-Fatihah
al_fatihah_classic = quran_classic[0]
al_fatihah_modern = quran_modern[0]

# Compare first verse
verse_classic = al_fatihah_classic['verses'][0]
verse_modern = al_fatihah_modern['verses'][0]

print("Classic:", verse_classic['somali_translation'])
print("Modern:", verse_modern['somali_translation'])
```

### JavaScript

```javascript
const quranClassic = require("./quran_somali_AbdullahHasanJacob.json");
const quranModern = require("./quran_somali_MahmudMuhammadAbduh.json");
const quranContemporary = require("./quran_somali_ShaykhMahmoodMuhammadAbdu.json");

// Get Al-Fatihah from all three
const fatihahClassic = quranClassic[0];
const fatihahModern = quranModern[0];
const fatihahContemporary = quranContemporary[0];

// Compare translations
console.log("Classic:", fatihahClassic.verses[0].somali_translation);
console.log("Modern:", fatihahModern.verses[0].somali_translation);
console.log("Contemporary:", fatihahContemporary.verses[0].somali_translation);
```

---

## 🎯 Common Queries

```bash
# Al-Fatihah
python3 query_quran.py 1

# Ayat Al-Kursi
python3 query_quran.py 2:255

# First 10 of Al-Kahf (Friday recitation)
python3 query_quran.py 18:1-10

# Yaseen (Friday)
python3 query_quran.py 36

# Al-Mulk (before sleep)
python3 query_quran.py 67

# Last 3 Surahs
python3 query_quran.py 112  # Al-Ikhlas
python3 query_quran.py 113  # Al-Falaq
python3 query_quran.py 114  # An-Nas
```

---

## 🔄 Choosing a Translation

### Use Case Recommendations

| Use Case                        | Recommended Translation        |
| ------------------------------- | ------------------------------ |
| Traditional study & scholarship | `jacob` (Classic)              |
| Modern readers & young learners | `abduh` (Modern)               |
| Comparison & research           | All three                      |
| General purpose                 | `jacob` (Most widely accepted) |

### Translation Differences

All translations include the same content but differ in:

-   Language style (classical vs modern vs contemporary)
-   Word choice in Somali
-   Interpretation approach

**Recommendation:** Try all three and choose what resonates with you!

---

## 📚 Data Source

-   **API:** [github.com/fawazahmed0/quran-api](https://github.com/fawazahmed0/quran-api)
-   **License:** Public domain / Free to use
-   **Arabic Text:** `ara-quransimple`
-   **Somali Translations:**
    -   `som-abdullahhasanja` (Jacob)
    -   `som-mahmudmuhammada` (Abduh)
    -   `som-shaykhmahmoodmu` (Abdu)

---

## 📖 Documentation

-   **README.md** (this file) - Project overview
-   **QUICK_START.txt** - Quick reference with copy-paste commands
-   **QUERY_GUIDE.txt** - Complete query tool documentation
-   **INDEX.txt** - Complete project index

---

## 🛠️ Requirements

-   Python 3.6+ (for query tool)
-   `requests` library (for fetching new data): `pip3 install requests`

---

## ⚡ Features

-   ✅ Three complete Somali translations
-   ✅ All translations verified (114 surahs, 6,236 verses each)
-   ✅ Easy-to-use query tool with translation switching
-   ✅ JSON format for easy integration
-   ✅ Comprehensive documentation
-   ✅ Ready to use in web apps, mobile apps, and research tools
-   ✅ Offline-capable (no internet needed once downloaded)
-   ✅ Free and open source

---

## 📝 License

The Qur'an text and translations are in the public domain.
Scripts and documentation created for this project are free to use.

---

## 🙏 Credits

**Translators:**

-   Abdullah Hasan Jacob
-   Mahmud Muhammad Abduh
-   Shaykh Mahmood Muhammad Abdu

**Data Source:** [Quran API](https://github.com/fawazahmed0/quran-api)

**Created:** November 8, 2025

---

## 📞 Support

For detailed usage:

-   Read `QUICK_START.txt` for quick reference
-   Read `QUERY_GUIDE.txt` for complete documentation
-   Run `python3 query_quran.py --help`

---

**May this be beneficial for you and your projects!**
