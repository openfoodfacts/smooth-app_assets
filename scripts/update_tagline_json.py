#!/usr/bin/env python3
"""
Update tagline JSON files (android, ios, web) to include the Photos for Impact campaign
and country-specific tagline feeds with deep-links to the campaign hub.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROD_DIR = os.path.join(BASE_DIR, 'prod', 'tagline')

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

TRANSLATIONS_BASE = {
    "default": {
        "title": "Missing products in your country! 📸",
        "message": "We are missing **everyday foods** in Open Food Facts. Snap missing products to help everyone eat better!",
        "button_label": "See missing foods"
    },
    "en": {
        "title": "Missing products in your country! 📸",
        "message": "We are missing **everyday foods** in Open Food Facts. Snap missing products to help everyone eat better!",
        "button_label": "See missing foods"
    },
    "de": {
        "title": "Fehlende Produkte in deinem Land! 📸",
        "message": "In Open Food Facts fehlen **wichtige Grundnahrungsmittel**. Fotografiere fehlende Produkte und hilf allen, sich besser zu ernähren!",
        "button_label": "Produkte ansehen"
    },
    "fr": {
        "title": "Produits manquants dans votre pays ! 📸",
        "message": "Il manque des **produits du quotidien** dans Open Food Facts. Photographiez-les pour aider tout le monde à mieux manger !",
        "button_label": "Voir les produits"
    },
    "it": {
        "title": "Prodotti mancanti nel tuo paese! 📸",
        "message": "Mancano **alimenti essenziali** in Open Food Facts. Fotografa i prodotti mancanti per aiutare tutti a mangiare meglio!",
        "button_label": "Vedi i prodotti"
    },
    "es": {
        "title": "¡Faltan productos en tu país! 📸",
        "message": "Faltan **alimentos cotidianos** en Open Food Facts. ¡Fotografía los productos que faltan para ayudar a todos a comer mejor!",
        "button_label": "Ver productos"
    },
    "nl": {
        "title": "Ontbrekende producten in jouw land! 📸",
        "message": "We missen **alledaagse basisvoedingsmiddelen** in Open Food Facts. Fotografeer ontbrekende producten en help iedereen gezonder te kiezen!",
        "button_label": "Bekijk producten"
    },
    "da": {
        "title": "Mangler produkter i dit land! 📸",
        "message": "Vi mangler **hverdagsfødevarer** i Open Food Facts. Tag billeder af manglende varer og hjælp alle med at spise bedre!",
        "button_label": "Se produkter"
    },
    "sv": {
        "title": "Saknade produkter i ditt land! 📸",
        "message": "Det saknas **vardagsmat** i Open Food Facts. Fota saknade produkter och hjälp alla att äta bättre!",
        "button_label": "Se produkter"
    },
    "nb": {
        "title": "Mangler produkter i ditt land! 📸",
        "message": "Vi mangler **hverdagsmat** i Open Food Facts. Ta bilde av manglende produkter for å hjelpe alle til å spise bedre!",
        "button_label": "Se produkter"
    },
    "no": {
        "title": "Mangler produkter i ditt land! 📸",
        "message": "Vi mangler **hverdagsmat** i Open Food Facts. Ta bilde av manglende produkter for å hjelpe alle til å spise bedre!",
        "button_label": "Se produkter"
    },
    "pl": {
        "title": "Brakujące produkty w Twoim kraju! 📸",
        "message": "W Open Food Facts brakuje **podstawowych produktów spożywczych**. Zrób zdjęcia brakujących artykułów i pomóż innym!",
        "button_label": "Zobacz produkty"
    },
    "pt": {
        "title": "Produtos em falta no seu país! 📸",
        "message": "Faltam **alimentos do dia a dia** na Open Food Facts. Fotografe os produtos em falta e ajude todos a comer melhor!",
        "button_label": "Ver produtos"
    },
    "el": {
        "title": "Λείπουν προϊόντα στη χώρα σας! 📸",
        "message": "Λείπουν **βασικά τρόφιμα** από το Open Food Facts. Φωτογραφίστε τα προϊόντα που λείπουν για να βοηθήσετε όλους!",
        "button_label": "Δείτε τα προϊόντα"
    },
    "hu": {
        "title": "Hiányzó termékek az országodban! 📸",
        "message": "Alapvető **mindennapi élelmiszerek** hiányoznak az Open Food Facts-ból. Fotózd le a hiányzó termékeket és segíts másoknak!",
        "button_label": "Termékek megtekintése"
    },
    "cs": {
        "title": "Chybějící potraviny ve vaší zemi! 📸",
        "message": "V Open Food Facts chybí **každodenní základní potraviny**. Vyfoťte chybějící produkty a pomozte ostatním lépe jíst!",
        "button_label": "Zobrazit potraviny"
    },
    "sk": {
        "title": "Chýbajúce potraviny vo vašej krajine! 📸",
        "message": "V Open Food Facts chýbajú **každodenné základné potraviny**. Odfoťte chýbajúce výrobky a pomôžte všetkým lepšie jesť!",
        "button_label": "Zobraziť potraviny"
    },
    "fi": {
        "title": "Puuttuvia tuotteita maassasi! 📸",
        "message": "Open Food Factsista puuttuu **jokapäiväisiä peruselintarvikkeita**. Kuvaa puuttuvat tuotteet ja auta muita syömään paremmin!",
        "button_label": "Katso tuotteet"
    },
    "et": {
        "title": "Puuduvad tooted sinu riigis! 📸",
        "message": "Open Food Factsist on puudu **igapäevased toidukaubad**. Pildista puuduvaid tooteid ja aita teistel paremini süüa!",
        "button_label": "Vaata tooteid"
    },
    "lv": {
        "title": "Trūkstošie produkti tavā valstī! 📸",
        "message": "Open Food Facts trūkst **ikdienas pārtikas preču**. Nofotografē trūkstošos produktus un palīdzi visiem izvēlēties labāk!",
        "button_label": "Skatīt produktus"
    },
    "lt": {
        "title": "Trūkstami produktai tavo šalyje! 📸",
        "message": "Open Food Facts trūkst **kasdienių maisto produktų**. Nufotografuok trūkstamus produktus ir padėk kitiems valgyti geriau!",
        "button_label": "Žiūrėti produktus"
    },
    "hr": {
        "title": "Nedostajući proizvodi u vašoj zemlji! 📸",
        "message": "U Open Food Factsu nedostaju **svakodnevne namirnice**. Fotografirajte proizvode koji nedostaju i pomozite drugima!",
        "button_label": "Pogledaj namirnice"
    },
    "sr": {
        "title": "Proizvodi koji nedostaju u tvojoj zemlji! 📸",
        "message": "U Open Food Factsu nedostaju **osnovne namirnice**. Fotografišite proizvode koji nedostaju i pomozite svima!",
        "button_label": "Pogledaj namirnice"
    },
    "ro": {
        "title": "Produse lipsă din țara ta! 📸",
        "message": "Lipsesc **alimente de bază** din Open Food Facts. Fotografiază produsele lipsă pentru a ajuta comunitatea să mănânce mai bine!",
        "button_label": "Vezi produsele"
    },
    "bg": {
        "title": "Липсващи продукти във вашата страна! 📸",
        "message": "В Open Food Facts липсват **ежедневни храни**. Снимайте липсващите продукти и помогнете на всички да се хранят по-добре!",
        "button_label": "Виж продуктите"
    },
    "sl": {
        "title": "Manjkajoči izdelki v vaši državi! 📸",
        "message": "V Open Food Facts manjkajo **vsakdanja osnovna živila**. Fotografirajte manjkajoče izdelke in pomagajte vsem bolje jesti!",
        "button_label": "Ogled izdelkov"
    }
}

COUNTRY_CODES_TO_TARGET = [
    ('at', '_AT'),
    ('be', '_BE'),
    ('bg', '_BG'),
    ('hr', '_HR'),
    ('cy', '_CY'),
    ('cs', '_CZ'),
    ('cs', '_CS'),
    ('dk', '_DK'),
    ('ee', '_EE'),
    ('fi', '_FI'),
    ('fr', '_FR'),
    ('de', '_DE'),
    ('el', '_GR'),
    ('el', '_EL'),
    ('hu', '_HU'),
    ('ie', '_IE'),
    ('it', '_IT'),
    ('lv', '_LV'),
    ('lt', '_LT'),
    ('lu', '_LU'),
    ('mt', '_MT'),
    ('me', '_ME'),
    ('nl', '_NL'),
    ('no', '_NO'),
    ('pl', '_PL'),
    ('pt', '_PT'),
    ('ro', '_RO'),
    ('rs', '_RS'),
    ('sk', '_SK'),
    ('si', '_SI'),
    ('si', '_SV'),
    ('es', '_ES'),
    ('se', '_SE'),
    ('ch', '_CH'),
    ('uk', '_UK'),
    ('uk', '_GB'),
]


def update_platform(platform):
    file_path = os.path.join(PROD_DIR, platform, 'main.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    img_url = f"https://raw.githubusercontent.com/openfoodfacts/smooth-app_assets/main/prod/tagline/{platform}/assets/photos_for_impact/photos_for_impact.svg"
    img_obj = {
        "alt": "Photos for Impact",
        "url": img_url,
        "width": 0.2
    }

    # Clone translations and inject image in default
    translations = {}
    for lang, t in TRANSLATIONS_BASE.items():
        t_copy = dict(t)
        if lang == 'default':
            t_copy['image'] = img_obj
        translations[lang] = t_copy

    news_item = {
        "end_date": END_DATE,
        "min_launches": 1,
        "start_date": START_DATE,
        "style": STYLE,
        "translations": translations,
        "url": "https://openfoodfacts.github.io/smooth-app_assets/photos-for-impact/"
    }

    data['news'][CAMPAIGN_ID] = news_item

    # Update default feed
    tagline_feed = data.setdefault('tagline_feed', {})
    default_feed = tagline_feed.setdefault('default', {'news': []})
    existing_ids = [n['id'] for n in default_feed['news']]
    if CAMPAIGN_ID not in existing_ids:
        default_feed['news'].insert(0, {"id": CAMPAIGN_ID})

    # Add country-specific feeds
    for country_slug, feed_key in COUNTRY_CODES_TO_TARGET:
        country_url = f"https://openfoodfacts.github.io/smooth-app_assets/photos-for-impact/?country={country_slug}"
        
        # Build country feed with campaign as top priority
        country_feed = [
            {
                "id": CAMPAIGN_ID,
                "override": {
                    "url": country_url
                }
            }
        ]
        # Append existing default campaigns for fallback rotation
        for existing in default_feed['news']:
            if existing['id'] != CAMPAIGN_ID:
                country_feed.append(existing)

        tagline_feed[feed_key] = {"news": country_feed}

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated {file_path} successfully!")


def main():
    for platform in ['android', 'ios', 'web']:
        update_platform(platform)


if __name__ == '__main__':
    main()
