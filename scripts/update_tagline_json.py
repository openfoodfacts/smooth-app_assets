#!/usr/bin/env python3
"""
Update tagline JSON files (android, ios, web) with dynamic, motivating stats
(coverage %, missing product count, localized country names) for all 32 countries.
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
    "message_background": "#F0F4F8",
    "message_text_color": "#1C2024",
    "button_background": "#347644",
    "button_text_color": "#FFFFFF",
    "content_background_color": "#FFFFFF"
}

# Country-specific template configurations
# Maps country slug (lowercase) to localized translations
TEMPLATES = {
    "at": {
        "de": ("🇦🇹 {pct}% in Österreich erfasst! 📸", "In Open Food Facts fehlen noch **{missing} wichtige Produkte** in Österreich. Fotografiere sie beim Einkaufen!", "{missing} Produkte ansehen"),
        "en": ("🇦🇹 {pct}% complete in Austria! 📸", "Open Food Facts is missing **{missing} everyday products** in Austria. Snap them while shopping!", "See {missing} foods"),
    },
    "be": {
        "fr": ("🇧🇪 {pct}% enregistrés en Belgique ! 📸", "Il manque encore **{missing} produits du quotidien** en Belgique. Photographiez-les en magasin !", "Voir les {missing} produits"),
        "nl": ("🇧🇪 {pct}% vastgelegd in België! 📸", "We missen nog **{missing} alledaagse producten** in België. Fotografeer ze tijdens het winkelen!", "Bekijk {missing} producten"),
        "de": ("🇧🇪 {pct}% in Belgien erfasst! 📸", "In Open Food Facts fehlen noch **{missing} Produkte** in Belgien. Fotografiere sie beim Einkaufen!", "{missing} Produkte ansehen"),
        "en": ("🇧🇪 {pct}% complete in Belgium! 📸", "Open Food Facts is missing **{missing} everyday products** in Belgium. Snap them while shopping!", "See {missing} foods"),
    },
    "bg": {
        "bg": ("🇧🇬 {pct}% събрани в България! 📸", "В Open Food Facts липсват само **{missing} продукта** в България. Снимайте ги в магазина!", "Вижте {missing}-те продукта"),
        "en": ("🇧🇬 {pct}% complete in Bulgaria! 📸", "Only **{missing} products** missing in Bulgaria. Snap them in store to reach 100%!", "See {missing} foods"),
    },
    "hr": {
        "hr": ("🇭🇷 {pct}% zabilježeno u Hrvatskoj! 📸", "U Open Food Factsu nedostaju još **{missing} namirnice** u Hrvatskoj. Fotografirajte ih u trgovini!", "Pogledaj {missing} namirnica"),
        "en": ("🇭🇷 {pct}% complete in Croatia! 📸", "Open Food Facts is missing **{missing} everyday products** in Croatia. Snap them while shopping!", "See {missing} foods"),
    },
    "cy": {
        "el": ("🇨🇾 {pct}% καταγεγραμμένα στην Κύπρο! 📸", "Λείπουν ακόμα **{missing} βασικά προϊόντα** στην Κύπρο. Φωτογραφίστε τα στα ψώνια σας!", "Δείτε τα {missing} προϊόντα"),
        "en": ("🇨🇾 {pct}% complete in Cyprus! 📸", "Open Food Facts is missing **{missing} everyday products** in Cyprus. Snap them while shopping!", "See {missing} foods"),
    },
    "cs": {
        "cs": ("🇨🇿 {pct}% hotovo v Česku! 📸", "V Open Food Facts chybí ještě **{missing} potravin** v ČR. Vyfoťte je při nákupu!", "Zobrazit {missing} potravin"),
        "en": ("🇨🇿 {pct}% complete in Czechia! 📸", "Open Food Facts is missing **{missing} everyday products** in Czechia. Snap them while shopping!", "See {missing} foods"),
    },
    "dk": {
        "da": ("🇩🇰 {pct}% registreret i Danmark! 📸", "Vi mangler stadig **{missing} hverdagsprodukter** i Danmark. Tag billeder af dem, når du handler!", "Se {missing} produkter"),
        "en": ("🇩🇰 {pct}% complete in Denmark! 📸", "Open Food Facts is missing **{missing} everyday products** in Denmark. Snap them while shopping!", "See {missing} foods"),
    },
    "ee": {
        "et": ("🇪🇪 {pct}% registreeritud Eestis! 📸", "Open Food Factsist on puudu veel **{missing} toodet** Eestis. Pildista neid poes!", "Vaata {missing} toodet"),
        "en": ("🇪🇪 {pct}% complete in Estonia! 📸", "Open Food Facts is missing **{missing} everyday products** in Estonia. Snap them while shopping!", "See {missing} foods"),
    },
    "fi": {
        "fi": ("🇫🇮 {pct}% katettu Suomessa! 📸", "Open Food Factsista puuttuu vielä **{missing} tuotetta** Suomessa. Ota niistä kuva kaupassa!", "Katso {missing} tuotetta"),
        "sv": ("🇫🇮 {pct}% registrerat i Finland! 📸", "Det saknas fortfarande **{missing} vardagsvaror** i Finland. Fota dem när du handlar!", "Se {missing} produkter"),
        "en": ("🇫🇮 {pct}% complete in Finland! 📸", "Open Food Facts is missing **{missing} everyday products** in Finland. Snap them while shopping!", "See {missing} foods"),
    },
    "fr": {
        "fr": ("🇫🇷 {pct}% enregistrés en France ! 📸", "Il manque seulement **{missing} produits essentiels** en France. Photographiez-les pour compléter la base !", "Voir les {missing} produits"),
        "en": ("🇫🇷 {pct}% complete in France! 📸", "Only **{missing} staple products** missing in France. Snap them in store to complete the basket!", "See {missing} foods"),
    },
    "de": {
        "de": ("🇩🇪 {pct}% in Deutschland erfasst! 📸", "In Open Food Facts fehlen noch **{missing} Grundnahrungsmittel** in Deutschland. Fotografiere sie beim Einkaufen!", "{missing} Produkte ansehen"),
        "en": ("🇩🇪 {pct}% complete in Germany! 📸", "Open Food Facts is missing **{missing} everyday products** in Germany. Snap them while shopping!", "See {missing} foods"),
    },
    "el": {
        "el": ("🇬🇷 {pct}% καταγεγραμμένα στην Ελλάδα! 📸", "Λείπουν ακόμα **{missing} βασικά προϊόντα** στην Ελλάδα. Φωτογραφίστε τα στα ψώνια σας!", "Δείτε τα {missing} προϊόντα"),
        "en": ("🇬🇷 {pct}% complete in Greece! 📸", "Open Food Facts is missing **{missing} everyday products** in Greece. Snap them while shopping!", "See {missing} foods"),
    },
    "hu": {
        "hu": ("🇭🇺 {pct}% rögzítve Magyarországon! 📸", "Az Open Food Facts-ból még **{missing} termék** hiányzik Magyarországon. Fotózd le őket vásárláskor!", "{missing} termék megtekintése"),
        "en": ("🇭🇺 {pct}% complete in Hungary! 📸", "Open Food Facts is missing **{missing} everyday products** in Hungary. Snap them while shopping!", "See {missing} foods"),
    },
    "ie": {
        "en": ("🇮🇪 {pct}% complete in Ireland! 📸", "Open Food Facts is missing **{missing} everyday products** in Ireland. Snap them while shopping!", "See {missing} foods"),
    },
    "it": {
        "it": ("🇮🇹 {pct}% registrati in Italia! 📸", "Mancano solo **{missing} alimenti essenziali** in Italia. Fotografali per completare il paniere!", "Vedi gli {missing} prodotti"),
        "en": ("🇮🇹 {pct}% complete in Italy! 📸", "Only **{missing} staple products** missing in Italy. Snap them in store to complete the basket!", "See {missing} foods"),
    },
    "lv": {
        "lv": ("🇱🇻 {pct}% reģistrēti Latvijā! 📸", "Open Food Facts trūkst vēl **{missing} svarīgu produktu** Latvijā. Nofotografē tos veikalā!", "Skatīt {missing} produktus"),
        "en": ("🇱🇻 {pct}% complete in Latvia! 📸", "Open Food Facts is missing **{missing} everyday products** in Latvia. Snap them while shopping!", "See {missing} foods"),
    },
    "lt": {
        "lt": ("🇱🇹 {pct}% užregistruota Lietuvoje! 📸", "Open Food Facts trūksta dar **{missing} produktų** Lietuvoje. Nufotografuok juos parduotuvėje!", "Žiūrėti {missing} produktus"),
        "en": ("🇱🇹 {pct}% complete in Lithuania! 📸", "Open Food Facts is missing **{missing} everyday products** in Lithuania. Snap them while shopping!", "See {missing} foods"),
    },
    "lu": {
        "fr": ("🇱🇺 {pct}% enregistrés au Luxembourg ! 📸", "Il manque encore **{missing} produits du quotidien** au Luxembourg. Photographiez-les en magasin !", "Voir les {missing} produits"),
        "de": ("🇱🇺 {pct}% in Luxemburg erfasst! 📸", "In Open Food Facts fehlen noch **{missing} Produkte** in Luxemburg. Fotografiere sie beim Einkaufen!", "{missing} Produkte ansehen"),
        "en": ("🇱🇺 {pct}% complete in Luxembourg! 📸", "Open Food Facts is missing **{missing} everyday products** in Luxembourg. Snap them while shopping!", "See {missing} foods"),
    },
    "mt": {
        "mt": ("🇲🇹 {pct}% reġistrati f'Malta! 📸", "F'Open Food Facts jonqos **{missing} prodott essenzjali** f'Malta. Ħu ritratt tagħhom waqt li tixtri!", "Ara d-{missing} prodott"),
        "en": ("🇲🇹 {pct}% complete in Malta! 📸", "Open Food Facts is missing **{missing} everyday products** in Malta. Snap them while shopping!", "See {missing} foods"),
    },
    "me": {
        "sr": ("🇲🇪 Samo {pct}% u Crnoj Gori! 📸", "U Open Food Factsu nedostaje još **{missing} osnovnih proizvoda** u Crnoj Gori. Fotografišite ih u prodavnici!", "Pogledaj {missing} namirnica"),
        "en": ("🇲🇪 Only {pct}% complete in Montenegro! 📸", "Open Food Facts is missing **{missing} everyday products** in Montenegro. Snap them while shopping!", "See {missing} foods"),
    },
    "nl": {
        "nl": ("🇳🇱 {pct}% vastgelegd in Nederland! 📸", "We missen nog **{missing} basisproducten** in Nederland. Fotografeer ze tijdens je boodschappen!", "Bekijk {missing} producten"),
        "en": ("🇳🇱 {pct}% complete in the Netherlands! 📸", "Open Food Facts is missing **{missing} everyday products** in the Netherlands. Snap them while shopping!", "See {missing} foods"),
    },
    "no": {
        "nb": ("🇳🇴 {pct}% registrert i Norge! 📸", "Det mangler fortsatt **{missing} hverdagsvaror** i Norge. Ta bilde av dem når du handler!", "Se {missing} produkter"),
        "no": ("🇳🇴 {pct}% registrert i Norge! 📸", "Det mangler fortsatt **{missing} hverdagsvaror** i Norge. Ta bilde av dem når du handler!", "Se {missing} produkter"),
        "en": ("🇳🇴 {pct}% complete in Norway! 📸", "Open Food Facts is missing **{missing} everyday products** in Norway. Snap them while shopping!", "See {missing} foods"),
    },
    "pl": {
        "pl": ("🇵🇱 {pct}% zarejestrowane w Polsce! 📸", "W Open Food Facts brakuje jeszcze **{missing} produktów** w Polsce. Zrób im zdjęcia w sklepie!", "Zobacz {missing} produktów"),
        "en": ("🇵🇱 {pct}% complete in Poland! 📸", "Open Food Facts is missing **{missing} everyday products** in Poland. Snap them while shopping!", "See {missing} foods"),
    },
    "pt": {
        "pt": ("🇵🇹 {pct}% registados em Portugal! 📸", "Faltam ainda **{missing} alimentos essenciais** em Portugal. Fotografe-os durante as compras!", "Ver {missing} produtos"),
        "en": ("🇵🇹 {pct}% complete in Portugal! 📸", "Open Food Facts is missing **{missing} everyday products** in Portugal. Snap them while shopping!", "See {missing} foods"),
    },
    "ro": {
        "ro": ("🇷🇴 {pct}% înregistrate în România! 📸", "Lipsesc încă **{missing} produse de bază** în România. Fotografiază-le la cumpărături!", "Vezi cele {missing} produse"),
        "en": ("🇷🇴 {pct}% complete in Romania! 📸", "Open Food Facts is missing **{missing} everyday products** in Romania. Snap them while shopping!", "See {missing} foods"),
    },
    "rs": {
        "sr": ("🇷🇸 {pct}% zabeleženo u Srbiji! 📸", "U Open Food Factsu nedostaju još **{missing} namirnice** u Srbiji. Fotografišite ih u prodavnici!", "Pogledaj {missing} namirnica"),
        "en": ("🇷🇸 {pct}% complete in Serbia! 📸", "Open Food Facts is missing **{missing} everyday products** in Serbia. Snap them while shopping!", "See {missing} foods"),
    },
    "sk": {
        "sk": ("🇸🇰 {pct}% hotovo na Slovensku! 📸", "V Open Food Facts chýba ešte **{missing} základných potravín** na Slovensku. Odfoťte ich pri nákupe!", "Zobraziť {missing} potravín"),
        "en": ("🇸🇰 {pct}% complete in Slovakia! 📸", "Open Food Facts is missing **{missing} everyday products** in Slovakia. Snap them while shopping!", "See {missing} foods"),
    },
    "si": {
        "sl": ("🇸🇮 {pct}% zabeleženih v Sloveniji! 📸", "V Open Food Facts manjka še **{missing} izdelkov** v Sloveniji. Fotografirajte jih v trgovini!", "Ogled {missing} izdelkov"),
        "en": ("🇸🇮 {pct}% complete in Slovenia! 📸", "Open Food Facts is missing **{missing} everyday products** in Slovenia. Snap them while shopping!", "See {missing} foods"),
    },
    "es": {
        "es": ("🇪🇸 {pct}% registrados en España! 📸", "Solo faltan **{missing} alimentos cotidianos** en España. ¡Fotografíalos para completar la lista!", "Ver los {missing} productos"),
        "ca": ("🇪🇸 {pct}% registrats a Espanya! 📸", "Només falten **{missing} aliments quotidians** a Espanya. Fotografia'ls per completar la llista!", "Veure els {missing} productes"),
        "en": ("🇪🇸 {pct}% complete in Spain! 📸", "Only **{missing} staple products** missing in Spain. Snap them in store to complete the basket!", "See {missing} foods"),
    },
    "se": {
        "sv": ("🇸🇪 {pct}% registrerat i Sverige! 📸", "Det saknas fortfarande **{missing} vardagsvaror** i Sverige. Fota dem när du handlar!", "Se {missing} produkter"),
        "en": ("🇸🇪 {pct}% complete in Sweden! 📸", "Open Food Facts is missing **{missing} everyday products** in Sweden. Snap them while shopping!", "See {missing} foods"),
    },
    "ch": {
        "de": ("🇨🇭 {pct}% in der Schweiz erfasst! 📸", "In Open Food Facts fehlen noch **{missing} wichtige Produkte** in der Schweiz. Hilf mit beim Einkaufen!", "{missing} Produkte ansehen"),
        "fr": ("🇨🇭 {pct}% enregistrés en Suisse ! 📸", "Il manque encore **{missing} produits du quotidien** en Suisse. Photographiez-les lors de vos courses !", "Voir les {missing} produits"),
        "it": ("🇨🇭 {pct}% registrati in Svizzera! 📸", "Mancano ancora **{missing} alimenti essenziali** in Svizzera. Fotografali mentre fai la spesa!", "Vedi {missing} prodotti"),
        "en": ("🇨🇭 {pct}% complete in Switzerland! 📸", "Open Food Facts is missing **{missing} everyday products** in Switzerland. Snap them while shopping!", "See {missing} foods"),
    },
    "uk": {
        "en": ("🇬🇧 {pct}% complete in the UK! 📸", "Open Food Facts is missing **{missing} everyday products** in the UK. Snap missing items when you shop!", "See {missing} foods"),
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
    overall_pct = stats.get('overall_coverage_pct', 66.9) if stats else 66.9
    overall_missing = stats.get('total_missing', 1033) if stats else 1033

    # Base generic translations
    translations = {
        "default": {
            "title": f"Missing products in your country! 📸",
            "message": f"We are missing **everyday foods** in Open Food Facts. Snap missing products to help everyone eat better!",
            "button_label": "See missing foods"
        },
        "en": {
            "title": f"Missing products in your country! 📸",
            "message": f"We are missing **everyday foods** in Open Food Facts. Snap missing products to help everyone eat better!",
            "button_label": "See missing foods"
        },
        "de": {
            "title": "Fehlende Produkte in deinem Land! 📸",
            "message": "In Open Food Facts fehlen **wichtige Grundnahrungsmittel**. Fotografiere fehlende Produkte und hilf allen!",
            "button_label": "Produkte ansehen"
        },
        "fr": {
            "title": "Produits manquants dans votre pays ! 📸",
            "message": "Il manque des **produits du quotidien** dans Open Food Facts. Photographiez-les pour aider tout le monde !",
            "button_label": "Voir les produits"
        },
        "it": {
            "title": "Prodotti mancanti nel tuo paese! 📸",
            "message": "Mancano **alimenti essenziali** in Open Food Facts. Fotografa i prodotti mancanti per aiutare tutti a mangiare meglio!",
            "button_label": "Vedi i prodotti"
        },
        "es": {
            "title": "¡Faltan productos en tu país! 📸",
            "message": "Faltan **alimentos cotidianos** en Open Food Facts. ¡Fotografía los productos que faltan para ayudar a todos!",
            "button_label": "Ver productos"
        },
        "nl": {
            "title": "Ontbrekende producten in jouw land! 📸",
            "message": "We missen **alledaagse basisvoedingsmiddelen** in Open Food Facts. Fotografeer ontbrekende producten!",
            "button_label": "Bekijk producten"
        }
    }

    # Generate country-locale specific translations (e.g. de_AT, fr_BE, de_CH, etc.)
    countries = stats.get('countries', {}) if stats else {}

    for slug, lang_dict in TEMPLATES.items():
        c_stat = countries.get(slug, {})
        pct = c_stat.get('coverage_pct', overall_pct)
        missing = c_stat.get('missing', overall_missing)
        
        for lang, (title_tpl, msg_tpl, btn_tpl) in lang_dict.items():
            formatted_title = title_tpl.format(pct=pct, missing=missing)
            formatted_msg = msg_tpl.format(pct=pct, missing=missing)
            formatted_btn = btn_tpl.format(pct=pct, missing=missing)

            # Map to upper country code (e.g. de_AT, fr_CH, lv_LV)
            for s, feed_key, iso in COUNTRY_CODES_TO_TARGET:
                if s == slug:
                    locale_key = f"{lang}_{iso}"
                    translations[locale_key] = {
                        "title": formatted_title,
                        "message": formatted_msg,
                        "button_label": formatted_btn
                    }
            
            # Also register language fallback if not already present
            if lang not in translations:
                translations[lang] = {
                    "title": formatted_title,
                    "message": formatted_msg,
                    "button_label": formatted_btn
                }

    return translations


def update_platform(platform, stats):
    file_path = os.path.join(PROD_DIR, platform, 'main.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

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
    existing_ids = [n['id'] for n in default_feed['news']]
    if CAMPAIGN_ID not in existing_ids:
        default_feed['news'].insert(0, {"id": CAMPAIGN_ID})

    # Add country-specific feeds
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
    print(f"Updated {file_path} with {len(translations)} localized tagline entries.")


def main():
    stats = load_stats()
    for platform in ['android', 'ios', 'web']:
        update_platform(platform, stats)


if __name__ == '__main__':
    main()
