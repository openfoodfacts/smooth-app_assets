#!/usr/bin/env python3
"""
Update tagline JSON files (android, ios, web) with concise, punchy titles and text
designed specifically for mobile card constraints (no text overflow or truncation).
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROD_DIR = os.path.join(BASE_DIR, 'prod', 'tagline')
STATS_FILE = os.path.join(BASE_DIR, 'data', 'campaign_stats.json')

CAMPAIGN_ID = "photos_for_impact_2026"
START_DATE = "2026-09-18 00:00:00"
END_DATE = "2026-12-31 23:59:59"

STYLE = {
    "title_background": "#2D72D2",
    "title_text_color": "#FFFFFF",
    "title_indicator_color": "#FFB800",
    "button_background": "#347644",
    "button_text_color": "#FFFFFF"
}

# Ultra-concise country templates: (Title <= 22 chars, Message <= 50 chars, Button <= 13 chars)
TEMPLATES = {
    "at": {
        "de": ("🇦🇹 {missing} Produkte fehlen!", "Fotografiere **{missing} Produkte**!", "Liste ansehen"),
        "en": ("🇦🇹 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "be": {
        "fr": ("🇧🇪 {missing} produits manquants", "Photographiez **{missing} produits** !", "Voir la liste"),
        "nl": ("🇧🇪 {missing} producten gezocht!", "Fotografeer **{missing} producten**!", "Bekijk lijst"),
        "de": ("🇧🇪 {missing} Produkte fehlen!", "Fotografiere **{missing} Produkte**!", "Liste ansehen"),
        "en": ("🇧🇪 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "bg": {
        "bg": ("🇧🇬 {missing} липсващи продукта", "Снимайте **{missing} продукта**!", "Виж списъка"),
        "en": ("🇧🇬 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "hr": {
        "hr": ("🇭🇷 Fali hrane!", "Slikajte **hranu**!", "Vidi popis"),
        "en": ("🇭🇷 Missing foods!", "Snap **missing foods**!", "See list"),
    },
    "cy": {
        "el": ("🇨🇾 Λείπουν {missing} τρόφιμα!", "Φωτογραφίστε **{missing} τρόφιμα**!", "Δείτε λίστα"),
        "en": ("🇨🇾 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "cs": {
        "cs": ("🇨🇿 Chybí {missing} potravin!", "Vyfoťte **{missing} potravin**!", "Zobrazit"),
        "en": ("🇨🇿 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "dk": {
        "da": ("🇩🇰 {missing} varer mangler!", "Tag foto af **{missing} varer**!", "Se liste"),
        "en": ("🇩🇰 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "ee": {
        "et": ("🇪🇪 {missing} toodet puudu!", "Pildista **{missing} toodet**!", "Vaata tooteid"),
        "en": ("🇪🇪 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "fi": {
        "fi": ("🇫🇮 {missing} tuotetta puuttuu!", "Kuvaa **{missing} tuotetta**!", "Katso lista"),
        "sv": ("🇫🇮 {missing} varor saknas!", "Fota **{missing} varor**!", "Se lista"),
        "en": ("🇫🇮 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "fr": {
        "fr": ("🇫🇷 {missing} produits manquants", "Photographiez **{missing} produits** !", "Voir la liste"),
        "en": ("🇫🇷 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "de": {
        "de": ("🇩🇪 {missing} Produkte fehlen!", "Fotografiere **{missing} Produkte**!", "Liste ansehen"),
        "en": ("🇩🇪 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "el": {
        "el": ("🇬🇷 Λείπουν {missing} τρόφιμα!", "Φωτογραφίστε **{missing} τρόφιμα**!", "Δείτε λίστα"),
        "en": ("🇬🇷 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "hu": {
        "hu": ("🇭🇺 {missing} termék hiányzik!", "Fotózz le **{missing} terméket**!", "Lista"),
        "en": ("🇭🇺 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "ie": {
        "en": ("🇮🇪 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "it": {
        "it": ("🇮🇹 Mancano {missing} prodotti!", "Fotografa **{missing} alimenti**!", "Vedi lista"),
        "en": ("🇮🇹 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "lv": {
        "lv": ("🇱🇻 Trūkst {missing} produktu!", "Nofotografē **{missing} preces**!", "Skatīt"),
        "en": ("🇱🇻 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "lt": {
        "lt": ("🇱🇹 Trūksta {missing} prekių!", "Nufotografuok **{missing} prekes**!", "Žiūrėti"),
        "en": ("🇱🇹 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "lu": {
        "fr": ("🇱🇺 {missing} produits manquants", "Photographiez **{missing} produits** !", "Voir la liste"),
        "de": ("🇱🇺 {missing} Produkte fehlen!", "Fotografiere **{missing} Produkte**!", "Liste ansehen"),
        "en": ("🇱🇺 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "mt": {
        "mt": ("🇲🇹 Jonqos {missing} prodott!", "Ħu ritratt ta' **{missing} prodott**!", "Ara l-lista"),
        "en": ("🇲🇹 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "me": {
        "sr": ("🇲🇪 Fali hrane!", "Slikajte **hranu**!", "Vidi spisak"),
        "en": ("🇲🇪 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "nl": {
        "nl": ("🇳🇱 {missing} producten gezocht!", "Fotografeer **{missing} producten**!", "Bekijk lijst"),
        "en": ("🇳🇱 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "no": {
        "nb": ("🇳🇴 {missing} varer mangler!", "Ta bilde av **{missing} varer**!", "Se liste"),
        "no": ("🇳🇴 {missing} varer mangler!", "Ta bilde av **{missing} varer**!", "Se liste"),
        "en": ("🇳🇴 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "pl": {
        "pl": ("🇵🇱 Brakuje {missing} produktów!", "Sfotografuj **{missing} produktów**!", "Zobacz listę"),
        "en": ("🇵🇱 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "pt": {
        "pt": ("🇵🇹 Faltam {missing} produtos!", "Fotografe **{missing} produtos**!", "Ver lista"),
        "en": ("🇵🇹 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "ro": {
        "ro": ("🇷🇴 Lipsesc {missing} produse!", "Fotografiază **{missing} alimente**!", "Vezi lista"),
        "en": ("🇷🇴 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "rs": {
        "sr": ("🇷🇸 Fali hrane!", "Slikajte **hranu**!", "Vidi spisak"),
        "en": ("🇷🇸 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "sk": {
        "sk": ("🇸🇰 Chýba {missing} potravín!", "Odfoťte **{missing} potravín**!", "Zobraziť"),
        "en": ("🇸🇰 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "si": {
        "sl": ("🇸🇮 Manjka {missing} živil!", "Slikajte **{missing} izdelkov**!", "Ogled"),
        "en": ("🇸🇮 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "es": {
        "es": ("🇪🇸 ¡Faltan {missing} productos!", "¡Fotografía **{missing} alimentos**!", "Ver lista"),
        "ca": ("🇪🇸 Falten {missing} productes!", "Fotografia **{missing} aliments**!", "Veure llista"),
        "en": ("🇪🇸 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "se": {
        "sv": ("🇸🇪 {missing} varor saknas!", "Fota **{missing} varor**!", "Se lista"),
        "en": ("🇸🇪 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "ch": {
        "de": ("🇨🇭 {missing} Produkte fehlen!", "Fotografiere **{missing} Produkte**!", "Liste ansehen"),
        "fr": ("🇨🇭 {missing} produits manquants", "Photographiez **{missing} produits** !", "Voir la liste"),
        "it": ("🇨🇭 Mancano {missing} prodotti!", "Fotografa **{missing} alimenti**!", "Vedi lista"),
        "en": ("🇨🇭 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    },
    "uk": {
        "en": ("🇬🇧 {missing} foods missing!", "Snap **{missing} foods**!", "See list"),
    }
}

COUNTRY_CODES_TO_TARGET = [
    ('at', '_AT', 'AT'),
    ('be', '_BE', 'BE'),
    ('bg', '_BG', 'BG'),
    ('hr', '_HR', 'HR'),
    ('cy', '_CY', 'CY'),
    ('cs', '_CZ', 'CZ'),
    ('cs', '_CS', 'CS'),
    ('dk', '_DK', 'DK'),
    ('ee', '_EE', 'EE'),
    ('fi', '_FI', 'FI'),
    ('fr', '_FR', 'FR'),
    ('de', '_DE', 'DE'),
    ('el', '_GR', 'GR'),
    ('el', '_EL', 'EL'),
    ('hu', '_HU', 'HU'),
    ('ie', '_IE', 'IE'),
    ('it', '_IT', 'IT'),
    ('lv', '_LV', 'LV'),
    ('lt', '_LT', 'LT'),
    ('lu', '_LU', 'LU'),
    ('mt', '_MT', 'MT'),
    ('me', '_ME', 'ME'),
    ('nl', '_NL', 'NL'),
    ('no', '_NO', 'NO'),
    ('pl', '_PL', 'PL'),
    ('pt', '_PT', 'PT'),
    ('ro', '_RO', 'RO'),
    ('rs', '_RS', 'RS'),
    ('sk', '_SK', 'SK'),
    ('si', '_SI', 'SI'),
    ('si', '_SV', 'SV'),
    ('es', '_ES', 'ES'),
    ('se', '_SE', 'SE'),
    ('ch', '_CH', 'CH'),
    ('uk', '_UK', 'UK'),
    ('uk', '_GB', 'GB'),
]


def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def generate_translations(stats):
    overall_missing = stats.get('total_missing', 1033) if stats else 1033

    # Short default translations
    translations = {
        "default": {
            "title": "Missing foods!",
            "message": "Snap **missing foods**!",
            "button_label": "See list"
        },
        "en": {
            "title": "Missing foods!",
            "message": "Snap **missing foods**!",
            "button_label": "See list"
        },
        "de": {
            "title": "Produkte gesucht!",
            "message": "Fotografiere **fehlende Produkte**!",
            "button_label": "Liste ansehen"
        },
        "fr": {
            "title": "Produits recherchés",
            "message": "Photographiez les **produits manquants** !",
            "button_label": "Voir la liste"
        },
        "it": {
            "title": "Prodotti cercati!",
            "message": "Fotografa gli **alimenti mancanti**!",
            "button_label": "Vedi lista"
        },
        "es": {
            "title": "¡Faltan productos!",
            "message": "¡Fotografía **alimentos que faltan**!",
            "button_label": "Ver lista"
        },
        "nl": {
            "title": "Producten gezocht!",
            "message": "Fotografeer **ontbrekende producten**!",
            "button_label": "Bekijk lijst"
        },
        "hr": {
            "title": "Fali hrane!",
            "message": "Slikajte **hranu**!",
            "button_label": "Vidi popis"
        }
    }

    countries = stats.get('countries', {}) if stats else {}

    for slug, lang_dict in TEMPLATES.items():
        c_stat = countries.get(slug, {})
        missing = c_stat.get('missing', overall_missing)
        
        for lang, (title_tpl, msg_tpl, btn_tpl) in lang_dict.items():
            formatted_title = title_tpl.format(missing=missing)
            formatted_msg = msg_tpl.format(missing=missing)
            formatted_btn = btn_tpl.format(missing=missing)

            for s, feed_key, iso in COUNTRY_CODES_TO_TARGET:
                if s == slug:
                    locale_key = f"{lang}_{iso}"
                    translations[locale_key] = {
                        "title": formatted_title,
                        "message": formatted_msg,
                        "button_label": formatted_btn
                    }
            
            if lang not in translations:
                translations[lang] = {
                    "title": formatted_title,
                    "message": formatted_msg,
                    "button_label": formatted_btn
                }

    return translations


EXPIRED_CAMPAIGNS = {
    'divinfood_survey_2026',
    'openprices_challenge_01_06',
    'nutriscore_petition_2025',
    'prices_summer_campaign'
}


def update_platform(platform, stats):
    file_path = os.path.join(PROD_DIR, platform, 'main.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Prune expired campaigns for cross-platform consistency
    for expired in EXPIRED_CAMPAIGNS:
        data['news'].pop(expired, None)

    img_url = f"https://raw.githubusercontent.com/openfoodfacts/smooth-app_assets/main/prod/tagline/{platform}/assets/photos_for_impact/photos_for_impact.svg"
    img_obj = {
        "alt": "Photos for Impact",
        "url": img_url,
        "width": 0.2
    }

    translations = generate_translations(stats)
    translations['default']['image'] = img_obj

    news_item = {
        "end_date": END_DATE,
        "min_launches": 1,
        "start_date": START_DATE,
        "style": STYLE,
        "translations": translations,
        "url": "https://openfoodfacts.github.io/smooth-app_assets/photos-for-impact/"
    }

    data['news'][CAMPAIGN_ID] = news_item

    tagline_feed = data.setdefault('tagline_feed', {})
    default_feed = tagline_feed.setdefault('default', {'news': []})
    
    # Filter expired items from all feeds in tagline_feed
    for feed_key, feed_val in tagline_feed.items():
        if isinstance(feed_val, dict) and 'news' in feed_val:
            feed_val['news'] = [n for n in feed_val['news'] if n.get('id') not in EXPIRED_CAMPAIGNS and n.get('id') in data['news']]

    existing_ids = [n['id'] for n in default_feed['news']]
    if CAMPAIGN_ID not in existing_ids:
        default_feed['news'].insert(0, {"id": CAMPAIGN_ID})

    for country_slug, feed_key, _ in COUNTRY_CODES_TO_TARGET:
        country_url = f"https://openfoodfacts.github.io/smooth-app_assets/photos-for-impact/?country={country_slug}"
        country_feed = [
            {
                "id": CAMPAIGN_ID,
                "override": {
                    "url": country_url
                }
            }
        ]
        for existing in default_feed['news']:
            if existing['id'] != CAMPAIGN_ID:
                country_feed.append(existing)

        tagline_feed[feed_key] = {"news": country_feed}

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated {file_path} with {len(translations)} concise localized tagline entries.")


def main():
    stats = load_stats()
    for platform in ['android', 'ios', 'web']:
        update_platform(platform, stats)


if __name__ == '__main__':
    main()
