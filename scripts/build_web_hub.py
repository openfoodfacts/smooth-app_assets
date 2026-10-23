#!/usr/bin/env python3
"""
Build script to generate both web games:
1. Scan Champion (photos-for-impact/index.html):
   Mobile-first, high density shopping list for in-store/pantry scanning with Open Food Facts.
2. Data Detective (data-detective/index.html):
   Desktop-friendly checklist for completing products:
   - Select & crop photos (ingredients & nutrition)
   - OCR ingredients & verify text
   - Enter nutrition table
   - Enter packaging details
   Linking directly to Open Food Facts category pages (e.g. /facets/categories/Liqueurs).
3. Taxonomy Wiz legacy redirect (taxonomy-wiz/index.html -> data-detective/)
"""

import os
import shutil
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Shared Language Names
LANGUAGE_NAMES = {
    "en": "English",
    "fr": "Français",
    "de": "Deutsch",
    "es": "Español",
    "it": "Italiano",
    "nl": "Nederlands",
    "pl": "Polski",
    "pt": "Português",
    "ro": "Română",
    "cs": "Čeština",
    "sk": "Slovenčina",
    "hu": "Magyar",
    "el": "Ελληνικά",
    "bg": "Български",
    "hr": "Hrvatski",
    "sr": "Srpski",
    "sl": "Slovenščina",
    "da": "Dansk",
    "sv": "Svenska",
    "fi": "Suomi",
    "no": "Norsk",
    "nb": "Norsk (bokmål)",
    "et": "Eesti",
    "lv": "Latviešu",
    "lt": "Lietuvių",
    "ga": "Gaeilge",
    "mt": "Malti",
    "lb": "Lëtzebuergesch",
    "ca": "Català",
    "eu": "Euskara",
    "gl": "Galego",
    "tr": "Türkçe"
}

TRANSLATIONS = {
    "en": {
        # Scan Champion
        "app_title": "Scan Champion",
        "app_badge": "Open Food Facts",
        "guide_title": "Scan Champion Instructions",
        "guide_hide": "Hide tips",
        "guide_show": "Show tips",
        "guide_headline": "Scan and photograph popular products sold in your country",
        "step_store_title": "In Store or In Pantry",
        "step_store_desc": "Scan products with the Open Food Facts app using this Scan List.",
        "step_photos_title": "Add 3 Clean Photos",
        "step_photos_desc": "Product front packaging, ingredient lists, and nutrition facts.",
        "step_category_title": "Add Category in App",
        "step_category_desc": "When adding or editing a product, be sure to select or enter its category in the app!",
        "tip_text": "Pro-tip: If a category sounds strange, just go to the closest category in the aisle!",
        "tab_missing": "High Priority (Missing)",
        "tab_all": "All Categories",
        "search_placeholder": "Filter categories (e.g. beer, bread, cheese)...",
        "reset_btn": "Reset",
        "reset_confirm": "Reset all checked categories for {country}?",
        "progress_summary": "{checked} of {total} scanned ({pct}%)",
        "completed_label": "Completed ({count})",
        "empty_search_title": "No categories found",
        "empty_search_desc": "No categories match \"{query}\".",
        "empty_missing_done_title": "All high-priority categories covered!",
        "empty_missing_done_desc": "Switch to \"All Categories\" to discover more products to photograph.",
        "empty_all_done_title": "Scan Champion! All {count} items checked!",
        "empty_all_done_desc": "Great job! You scanned all categories in this list. Tap completed items to uncheck or hit Reset to scan again.",
        "modal_title": "Select your country",
        "modal_subtitle": "Choose your country to see the categories needed for your local food basket:",
        "modal_search_placeholder": "Search country...",
        "modal_confirm": "Select",
        "footer_supported": "Project supported by:",
        "footer_citizen": "Discover our citizen science research:",
        "footer_citizen_link_en": "Citizen Science (EN)",
        "footer_citizen_link_fr": "Science Citoyenne (FR)",
        "footer_storage": "Ticks saved locally on your device",
        "switch_to_detective": "🕵️‍♂️ At home? Data Detective",
        "switch_to_scan": "🤳 In store? Scan Champion",

        # Data Detective
        "detective_title": "Data Detective",
        "detective_badge": "Open Food Facts",
        "detective_guide_title": "Data Detective Mission",
        "detective_guide_headline": "Complete product data: photos, ingredients, nutrition, and packaging",
        "detective_step1_title": "1. Select & Crop Photos",
        "detective_step1_desc": "Select and crop clear photos for the ingredients list and nutrition facts table.",
        "detective_step2_title": "2. OCR Ingredients & Verify",
        "detective_step2_desc": "Run the OCR to extract ingredients from the photo, then verify and correct the text.",
        "detective_step3_title": "3. Enter Nutrition Facts",
        "detective_step3_desc": "Transcribe the nutrition table values (energy, fats, sugars, salt, proteins...).",
        "detective_step4_title": "4. Enter Packaging",
        "detective_step4_desc": "Add packaging shapes, materials, and recycling instructions.",
        "detective_warning_title": "At home with your computer:",
        "detective_warning_desc": "Completing products is much easier on a desktop computer. Need help? Join #ingredients and #packaging on Slack!",
        "detective_slack_btn": "Join Slack",
        "detective_wiki_btn": "How to edit products",
        "detective_tip_text": "Pro-tip: Click any category to open its Open Food Facts page, find products to complete, and tick them off!",
        "detective_tab_all": "All Categories",
        "detective_tab_priority": "High Priority",
        "detective_progress_summary": "{checked} of {total} completed ({pct}%)",
        "detective_completed_label": "Completed ({count})",
        "detective_empty_priority_title": "No high priority items right now",
        "detective_empty_priority_desc": "Switch to 'All Categories' to browse and complete products in this country.",
        "detective_empty_all_done_title": "Data Detective Champion! All {count} categories completed!",
        "detective_empty_all_done_desc": "Incredible detective work! You reviewed and completed all categories in this list.",
        "detective_open_category": "Open category in Open Food Facts"
    },
    "fr": {
        # Scan Champion
        "app_title": "Scan Champion",
        "app_badge": "Open Food Facts",
        "guide_title": "Instructions Scan Champion",
        "guide_hide": "Masquer astuces",
        "guide_show": "Afficher astuces",
        "guide_headline": "Scannez et photographiez les produits populaires vendus dans votre pays",
        "step_store_title": "En magasin ou dans vos placards",
        "step_store_desc": "Scannez les produits avec l'application Open Food Facts grâce à cette liste.",
        "step_photos_title": "Ajoutez 3 photos nettes",
        "step_photos_desc": "Face avant du produit, liste des ingrédients et tableau nutritionnel.",
        "step_category_title": "Ajoutez la catégorie",
        "step_category_desc": "Lors de l'ajout ou de l'édition du produit, pensez bien à renseigner sa catégorie dans l'application !",
        "tip_text": "Astuce : Si le nom d'une catégorie vous paraît étrange, prenez le produit le plus proche dans le rayon !",
        "tab_missing": "Priorité haute (manquants)",
        "tab_all": "Toutes les catégories",
        "search_placeholder": "Filtrer les catégories (ex : bière, pain, fromage)...",
        "reset_btn": "Réinitialiser",
        "reset_confirm": "Réinitialiser toutes les catégories cochées pour {country} ?",
        "progress_summary": "{checked} sur {total} scannés ({pct}%)",
        "completed_label": "Complétés ({count})",
        "empty_search_title": "Aucune catégorie trouvée",
        "empty_search_desc": "Aucune catégorie ne correspond à « {query} ».",
        "empty_missing_done_title": "Toutes les catégories prioritaires sont couvertes !",
        "empty_missing_done_desc": "Basculez sur « Toutes les catégories » pour découvrir d'autres produits à photographier.",
        "empty_all_done_title": "Scan Champion ! Les {count} catégories sont cochées !",
        "empty_all_done_desc": "Bravo ! Vous avez scanné toutes les catégories. Touchez un élément complété pour le décocher ou réinitialisez.",
        "modal_title": "Choisissez votre pays",
        "modal_subtitle": "Sélectionnez votre pays pour afficher les catégories prioritaires :",
        "modal_search_placeholder": "Rechercher un pays...",
        "modal_confirm": "Choisir",
        "footer_supported": "Projet soutenu par :",
        "footer_citizen": "Découvrez nos recherches en science citoyenne :",
        "footer_citizen_link_en": "Citizen Science (EN)",
        "footer_citizen_link_fr": "Science Citoyenne (FR)",
        "footer_storage": "Coches enregistrées localement sur votre appareil",
        "switch_to_detective": "🕵️‍♂️ Sur ordi ? Data Detective",
        "switch_to_scan": "🤳 En magasin ? Scan Champion",

        # Data Detective
        "detective_title": "Data Detective",
        "detective_badge": "Open Food Facts",
        "detective_guide_title": "Mission Data Detective",
        "detective_guide_headline": "Complétez les données des produits : photos, ingrédients, nutrition et emballages",
        "detective_step1_title": "1. Sélectionner les photos",
        "detective_step1_desc": "Sélectionnez et cadrez les photos des ingrédients et du tableau nutritionnel.",
        "detective_step2_title": "2. OCR & Ingrédients",
        "detective_step2_desc": "Utilisez l'OCR pour extraire les ingrédients depuis la photo, puis vérifiez et corrigez le texte.",
        "detective_step3_title": "3. Entrer la nutrition",
        "detective_step3_desc": "Renseignez le tableau nutritionnel (énergie, matières grasses, sucres, sel, protéines...).",
        "detective_step4_title": "4. Entrer le packaging",
        "detective_step4_desc": "Indiquez les emballages, matériaux, formats et consignes de tri.",
        "detective_warning_title": "À la maison sur votre ordinateur :",
        "detective_warning_desc": "Éditer les produits est bien plus simple sur un ordinateur avec un grand écran et un clavier. Rejoignez #ingredients et #packaging sur Slack !",
        "detective_slack_btn": "Rejoindre Slack",
        "detective_wiki_btn": "Guide d'édition",
        "detective_tip_text": "Astuce : Cliquez sur une catégorie pour ouvrir sa page sur Open Food Facts, complétez les produits et cochez la catégorie !",
        "detective_tab_all": "Toutes les catégories",
        "detective_tab_priority": "Haute priorité",
        "detective_progress_summary": "{checked} sur {total} complétés ({pct}%)",
        "detective_completed_label": "Complétés ({count})",
        "detective_empty_priority_title": "Aucun élément hautement prioritaire pour l'instant",
        "detective_empty_priority_desc": "Basculez sur « Toutes les catégories » pour explorer et compléter les produits.",
        "detective_empty_all_done_title": "Data Detective Champion ! Les {count} catégories ont été complétées !",
        "detective_empty_all_done_desc": "Formidable travail d'enquête ! Vous avez vérifié et complété toutes les catégories de la liste.",
        "detective_open_category": "Ouvrir la catégorie sur Open Food Facts"
    },
    "de": {
        "app_title": "Scan Champion",
        "app_badge": "Open Food Facts",
        "guide_title": "Scan Champion Anleitung",
        "guide_hide": "Tipps ausblenden",
        "guide_show": "Tipps anzeigen",
        "guide_headline": "Scanne und fotografiere beliebte Produkte deines Landes",
        "step_store_title": "Im Geschäft oder in der Vorratskammer",
        "step_store_desc": "Scanne Produkte mit der Open Food Facts App anhand dieser Scan-Liste.",
        "step_photos_title": "3 klare Fotos aufnehmen",
        "step_photos_desc": "Produktvorderseite, Zutatenliste und Nährwerttabelle.",
        "step_category_title": "Kategorie in der App angeben",
        "step_category_desc": "Beim Hinzufügen oder Bearbeiten bitte unbedingt die passende Kategorie in der App auswählen!",
        "tip_text": "Tipp: Klingt eine Kategorie ungewöhnlich, wähle einfach das ähnlichste Produkt im Regal!",
        "tab_missing": "Hohe Priorität (Fehlend)",
        "tab_all": "Alle Kategorien",
        "search_placeholder": "Kategorien filtern (z.B. Bier, Brot, Käse)...",
        "reset_btn": "Zurücksetzen",
        "reset_confirm": "Alle abgehakten Kategorien für {country} zurücksetzen?",
        "progress_summary": "{checked} von {total} gescannt ({pct}%)",
        "completed_label": "Erledigt ({count})",
        "empty_search_title": "Keine Kategorien gefunden",
        "empty_search_desc": "Keine Kategorien entsprechen „{query}“.",
        "empty_missing_done_title": "Alle vorrangigen Kategorien erfasst!",
        "empty_missing_done_desc": "Wechsle zu „Alle Kategorien“, um weitere Produkte zu entdecken.",
        "empty_all_done_title": "Scan Champion! Alle {count} Kategorien abgehakt!",
        "empty_all_done_desc": "Klasse! Du hast alle Kategorien gescannt.",
        "modal_title": "Wähle dein Land",
        "modal_subtitle": "Wähle dein Land, um die benötigten Lebensmittelkategorien anzuzeigen:",
        "modal_search_placeholder": "Land suchen...",
        "modal_confirm": "Auswählen",
        "footer_supported": "Projekt unterstützt von:",
        "footer_citizen": "Entdecke unsere Citizen-Science-Forschung:",
        "footer_citizen_link_en": "Citizen Science (EN)",
        "footer_citizen_link_fr": "Science Citoyenne (FR)",
        "footer_storage": "Häkchen lokal auf deinem Gerät gespeichert",
        "switch_to_detective": "🕵️‍♂️ Am Computer? Data Detective",
        "switch_to_scan": "🤳 Im Supermarkt? Scan Champion",

        "detective_title": "Data Detective",
        "detective_badge": "Open Food Facts",
        "detective_guide_title": "Data Detective Mission",
        "detective_guide_headline": "Produktdaten vervollständigen: Fotos, Zutaten, Nährwerte und Verpackung",
        "detective_step1_title": "1. Fotos auswählen",
        "detective_step1_desc": "Wähle und schneide die Fotos für Zutatenliste und Nährwerttabelle passgenau zu.",
        "detective_step2_title": "2. Zutaten-OCR & Prüfung",
        "detective_step2_desc": "Nutze OCR, um Zutaten aus dem Foto zu extrahieren, und überprüfe den Text.",
        "detective_step3_title": "3. Nährwerte eintragen",
        "detective_step3_desc": "Trage die Nährwertangaben ein (Energie, Fett, Zucker, Salz, Eiweiß...).",
        "detective_step4_title": "4. Verpackung erfassen",
        "detective_step4_desc": "Erfasse Verpackungsmaterialien, Formen und Recyclinghinweise.",
        "detective_warning_title": "Zuhause am Computer:",
        "detective_warning_desc": "Am PC geht das Bearbeiten viel leichter von der Hand. Fragen? Triff uns auf Slack in #ingredients und #packaging!",
        "detective_slack_btn": "Slack beitreten",
        "detective_wiki_btn": "Bearbeitungs-Leitfaden",
        "detective_tip_text": "Tipp: Klicke auf eine Kategorie, um Produkte auf Open Food Facts zu öffnen und zu vervollständigen!",
        "detective_tab_all": "Alle Kategorien",
        "detective_tab_priority": "Hohe Priorität",
        "detective_progress_summary": "{checked} von {total} vervollständigt ({pct}%)",
        "detective_completed_label": "Vervollständigt ({count})",
        "detective_empty_priority_title": "Derzeit keine hochprioritären Einträge",
        "detective_empty_priority_desc": "Wechsle zu „Alle Kategorien“, um Produkte zu vervollständigen.",
        "detective_empty_all_done_title": "Data Detective Champion! Alle {count} Kategorien vervollständigt!",
        "detective_empty_all_done_desc": "Tolle Detektivarbeit! Du hast alle Kategorien durchgesehen.",
        "detective_open_category": "Kategorie auf Open Food Facts öffnen"
    },
    "es": {
        "app_title": "Scan Champion",
        "app_badge": "Open Food Facts",
        "guide_title": "Instrucciones de Scan Champion",
        "guide_hide": "Ocultar consejos",
        "guide_show": "Mostrar consejos",
        "guide_headline": "Escanea y fotografía productos populares vendidos en tu país",
        "step_store_title": "En tienda o en tu despensa",
        "step_store_desc": "Escanea productos con la app Open Food Facts usando esta lista.",
        "step_photos_title": "Añade 3 fotos nítidas",
        "step_photos_desc": "Frontal del producto, lista de ingredientes y tabla nutricional.",
        "step_category_title": "Añade la categoría en la app",
        "step_category_desc": "¡Al añadir o editar el producto, asegúrate de seleccionar su categoría en la app!",
        "tip_text": "Consejo: Si una categoría te suena extraña, ¡elige la más parecida del pasillo!",
        "tab_missing": "Prioridad alta (Faltan)",
        "tab_all": "Todas las categorías",
        "search_placeholder": "Filtrar categorías (ej. cerveza, pan, queso)...",
        "reset_btn": "Restablecer",
        "reset_confirm": "¿Restablecer todas las categorías marcadas para {country}?",
        "progress_summary": "{checked} de {total} escaneados ({pct}%)",
        "completed_label": "Completados ({count})",
        "empty_search_title": "No se encontraron categorías",
        "empty_search_desc": "Ninguna categoría coincide con «{query}».",
        "empty_missing_done_title": "¡Todas las categorías prioritarias completadas!",
        "empty_missing_done_desc": "Cambia a «Todas las categorías» para descubrir más productos.",
        "empty_all_done_title": "¡Scan Champion! ¡Las {count} categorías marcadas!",
        "empty_all_done_desc": "¡Excelente trabajo! Has escaneado todas las categorías.",
        "modal_title": "Selecciona tu país",
        "modal_subtitle": "Elige tu país para ver las categorías necesarias de tu cesta básica:",
        "modal_search_placeholder": "Buscar país...",
        "modal_confirm": "Seleccionar",
        "footer_supported": "Proyecto apoyado por:",
        "footer_citizen": "Descubre nuestra investigación en ciencia ciudadana:",
        "footer_citizen_link_en": "Citizen Science (EN)",
        "footer_citizen_link_fr": "Science Citoyenne (FR)",
        "footer_storage": "Marcas guardadas localmente en tu dispositivo",
        "switch_to_detective": "🕵️‍♂️ ¿En ordenador? Data Detective",
        "switch_to_scan": "🤳 ¿En el súper? Scan Champion",

        "detective_title": "Data Detective",
        "detective_badge": "Open Food Facts",
        "detective_guide_title": "Misión Data Detective",
        "detective_guide_headline": "Completa los datos de productos: fotos, ingredientes, nutrición y envases",
        "detective_step1_title": "1. Seleccionar fotos",
        "detective_step1_desc": "Selecciona y encuadra las fotos de la lista de ingredientes y la tabla nutricional.",
        "detective_step2_title": "2. OCR y verificar",
        "detective_step2_desc": "Extrae los ingredientes con el OCR y revisa y corrige el texto.",
        "detective_step3_title": "3. Introducir nutrición",
        "detective_step3_desc": "Introduce la tabla nutricional (energía, grasas, azúcares, sal, proteínas...).",
        "detective_step4_title": "4. Introducir envases",
        "detective_step4_desc": "Añade formatos, materiales e instrucciones de reciclaje de los envases.",
        "detective_warning_title": "En casa con tu ordenador:",
        "detective_warning_desc": "Editar productos es mucho más cómodo en ordenador. ¿Dudas? ¡Únete a #ingredients y #packaging en Slack!",
        "detective_slack_btn": "Unirse a Slack",
        "detective_wiki_btn": "Guía de edición",
        "detective_tip_text": "Consejo: ¡Haz clic en una categoría para abrirla en Open Food Facts, completar productos y marcarla!",
        "detective_tab_all": "Todas las categorías",
        "detective_tab_priority": "Prioridad alta",
        "detective_progress_summary": "{checked} de {total} completados ({pct}%)",
        "detective_completed_label": "Completados ({count})",
        "detective_empty_priority_title": "No hay elementos de alta prioridad en este momento",
        "detective_empty_priority_desc": "Cambia a «Todas las categorías» para explorar y completar productos.",
        "detective_empty_all_done_title": "¡Data Detective Champion! ¡Las {count} categorías completadas!",
        "detective_empty_all_done_desc": "¡Increíble labor detectivesca! Has completado todas las categorías de la lista.",
        "detective_open_category": "Abrir categoría en Open Food Facts"
    }
}

OTHER_LANG_CODES = [
    "it", "nl", "pl", "pt", "ro", "cs", "sk", "hu", "el", "bg", "hr",
    "sr", "sl", "da", "sv", "fi", "no", "nb", "et", "lv", "lt", "ga",
    "mt", "lb", "ca", "eu", "gl", "tr"
]

for code in OTHER_LANG_CODES:
    if code not in TRANSLATIONS:
        TRANSLATIONS[code] = dict(TRANSLATIONS["en"])

TRANSLATIONS["nb"] = TRANSLATIONS.get("no", TRANSLATIONS["en"])


def build_data_detective_html():
    """Build Data Detective HTML file."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Data Detective 🕵️‍♂️💻 — Open Food Facts</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Matomo -->
    <script>
      var _paq = window._paq = window._paq || [];
      _paq.push(['setDoNotTrack', true]);
      _paq.push(['disableCookies']);
      _paq.push(['trackPageView']);
      _paq.push(['enableLinkTracking']);
      (function() {
        var u="https://analytics.openfoodfacts.org/";
        _paq.push(['setTrackerUrl', u+'matomo.php']);
        _paq.push(['setSiteId', '19']);
        var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
        g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
      })();
    </script>
    <noscript><p><img src="https://analytics.openfoodfacts.org/matomo.php?idsite=19&amp;rec=1" style="border:0;" alt="" /></p></noscript>
    <style>
        :root {
            --primary: #1b7340;
            --primary-dark: #12522c;
            --primary-light: #e8f5e9;
            --accent-detective: #0284c7;
            --accent-detective-dark: #0369a1;
            --accent-detective-light: #e0f2fe;
            --accent-gold: #f59e0b;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --text-light: #94a3b8;
            --border: #e2e8f0;
            --border-hover: #cbd5e1;
            --radius-lg: 14px;
            --radius-md: 10px;
            --radius-sm: 6px;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.08);
            --shadow-lg: 0 10px 25px -3px rgba(0,0,0,0.1);
            --item-height: 42px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.45;
            padding-bottom: 70px;
            -webkit-font-smoothing: antialiased;
        }

        /* Top Sticky Header */
        header {
            background: #ffffff;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: var(--shadow-sm);
        }

        .header-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 10px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }

        .brand-area {
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            color: var(--text-main);
            min-width: 0;
        }

        .brand-emoji {
            font-size: 24px;
            line-height: 1;
            flex-shrink: 0;
        }

        .brand-text {
            display: flex;
            flex-direction: column;
            min-width: 0;
        }

        .brand-title {
            font-size: 16px;
            font-weight: 800;
            letter-spacing: -0.3px;
            white-space: nowrap;
        }

        .brand-badge {
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--accent-detective);
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-shrink: 0;
        }

        .switch-game-link {
            font-size: 11.5px;
            font-weight: 600;
            color: var(--primary);
            text-decoration: none;
            background: var(--primary-light);
            padding: 6px 10px;
            border-radius: 20px;
            display: none;
            transition: all 0.15s ease;
            white-space: nowrap;
        }

        .switch-game-link:hover {
            background: #dcfce7;
        }

        @media (min-width: 680px) {
            .switch-game-link {
                display: inline-flex;
                align-items: center;
                gap: 4px;
            }
        }

        .select-wrapper {
            position: relative;
        }

        select.header-select {
            appearance: none;
            -webkit-appearance: none;
            background: #ffffff;
            border: 1.5px solid var(--border);
            padding: 6px 24px 6px 8px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-main);
            cursor: pointer;
            box-shadow: var(--shadow-sm);
            max-width: 155px;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        select.header-select:focus {
            outline: none;
            border-color: var(--accent-detective);
        }

        .select-wrapper::after {
            content: '▾';
            font-size: 10px;
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }

        select.lang-select {
            max-width: 110px;
        }

        main {
            max-width: 900px;
            margin: 0 auto;
            padding: 12px 16px;
        }

        /* Computer Context Card */
        .context-card {
            background: #f0f9ff;
            border: 1.5px solid #bae6fd;
            border-radius: var(--radius-md);
            padding: 12px 16px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
        }

        .context-left {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            font-size: 13px;
            color: #0369a1;
            flex: 1;
            min-width: 240px;
        }

        .context-icon {
            font-size: 20px;
            flex-shrink: 0;
            line-height: 1;
        }

        .context-text strong {
            display: block;
            margin-bottom: 2px;
            color: #075985;
        }

        .context-buttons {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            align-items: center;
        }

        .btn-tool {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            font-size: 11.5px;
            font-weight: 700;
            padding: 6px 12px;
            border-radius: 20px;
            text-decoration: none;
            transition: all 0.15s ease;
            box-shadow: var(--shadow-sm);
        }

        .btn-slack {
            background: #4a154b;
            color: #ffffff;
        }

        .btn-slack:hover {
            background: #611f69;
        }

        .btn-wiki {
            background: #0284c7;
            color: #ffffff;
        }

        .btn-wiki:hover {
            background: #0369a1;
        }

        /* Mission / Guide Card */
        .guide-card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            margin-bottom: 12px;
            box-shadow: var(--shadow-sm);
            overflow: hidden;
        }

        .guide-header {
            padding: 10px 16px;
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            user-select: none;
        }

        .guide-header-title {
            font-size: 13.5px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .guide-toggle-btn {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: #ffffff;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
        }

        .guide-body {
            padding: 12px 16px;
            font-size: 13px;
        }

        .guide-body.collapsed {
            display: none;
        }

        .guide-headline {
            font-weight: 700;
            font-size: 13.5px;
            margin-bottom: 10px;
            color: #0369a1;
        }

        /* 4 Steps Grid: Photos, OCR, Nutrition, Packaging */
        .guide-steps {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
            gap: 10px;
            margin-bottom: 10px;
        }

        .guide-step {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            background: var(--bg);
            border: 1px solid var(--border);
            padding: 10px 12px;
            border-radius: var(--radius-sm);
        }

        .guide-step-icon {
            font-size: 20px;
            flex-shrink: 0;
            margin-top: 1px;
        }

        .guide-step-text {
            font-size: 12px;
            line-height: 1.35;
        }

        .guide-step-text strong {
            display: block;
            color: var(--text-main);
            font-weight: 600;
            margin-bottom: 2px;
        }

        .guide-tip-banner {
            background: #fffbeb;
            border: 1px solid #fef3c7;
            border-radius: var(--radius-sm);
            padding: 7px 12px;
            font-size: 12px;
            color: #92400e;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Sticky Control Bar */
        .controls-sticky {
            position: sticky;
            top: 53px;
            background: var(--bg);
            padding: 6px 0 8px 0;
            z-index: 90;
            border-bottom: 1px solid rgba(226, 232, 240, 0.8);
            margin-bottom: 10px;
        }

        /* 2 Tabs: All Categories (default active) & High Priority */
        .tab-bar {
            display: flex;
            background: #e2e8f0;
            border-radius: var(--radius-md);
            padding: 3px;
            gap: 3px;
            margin-bottom: 8px;
        }

        .tab-btn {
            flex: 1;
            padding: 8px 6px;
            border: none;
            background: transparent;
            border-radius: var(--radius-sm);
            font-size: 12.5px;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.15s ease;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            white-space: nowrap;
        }

        .tab-btn.active {
            background: #ffffff;
            color: var(--text-main);
            box-shadow: var(--shadow-sm);
            font-weight: 700;
        }

        .tab-btn .badge-pill {
            background: #e2e8f0;
            color: var(--text-main);
            padding: 1px 6px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 700;
        }

        .tab-btn.active .badge-pill {
            background: var(--accent-detective-light);
            color: var(--accent-detective-dark);
        }

        /* Search + Toolbar */
        .toolbar-row {
            display: flex;
            gap: 8px;
            align-items: center;
        }

        .search-box-wrapper {
            position: relative;
            flex: 1;
        }

        .search-box-wrapper input {
            width: 100%;
            padding: 8px 30px 8px 30px;
            border: 1px solid var(--border);
            border-radius: 20px;
            font-size: 13px;
            background: #ffffff;
            color: var(--text-main);
            box-shadow: var(--shadow-sm);
        }

        .search-box-wrapper input:focus {
            outline: none;
            border-color: var(--accent-detective);
        }

        .search-icon {
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 12px;
            color: var(--text-muted);
            pointer-events: none;
        }

        .search-clear-btn {
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            background: #e2e8f0;
            border: none;
            color: var(--text-muted);
            border-radius: 50%;
            width: 18px;
            height: 18px;
            font-size: 10px;
            cursor: pointer;
            display: none;
            align-items: center;
            justify-content: center;
        }

        .search-clear-btn.visible {
            display: flex;
        }

        .btn-reset {
            background: #ffffff;
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 7px 12px;
            border-radius: 20px;
            font-size: 11.5px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 4px;
            flex-shrink: 0;
            box-shadow: var(--shadow-sm);
        }

        .btn-reset:hover {
            background: #fee2e2;
            color: #b91c1c;
            border-color: #fca5a5;
        }

        /* Mini Progress Bar */
        .progress-strip {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 6px;
            font-size: 11.5px;
            color: var(--text-muted);
            padding: 0 4px;
        }

        .progress-bar-track {
            flex: 1;
            height: 6px;
            background: #e2e8f0;
            border-radius: 10px;
            overflow: hidden;
        }

        .progress-bar-fill {
            height: 100%;
            background: var(--accent-detective);
            border-radius: 10px;
            transition: width 0.3s ease;
        }

        .progress-text {
            font-weight: 600;
            white-space: nowrap;
        }

        /* Google Keep Style Checklist with Direct Category Links */
        .checklist-container {
            display: grid;
            grid-template-columns: 1fr;
            gap: 6px;
        }

        @media (min-width: 680px) {
            .checklist-container {
                grid-template-columns: repeat(2, 1fr);
                gap: 8px;
            }
        }

        .check-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 9px 12px;
            min-height: var(--item-height);
            min-width: 0;
            width: 100%;
            transition: background 0.12s ease, border-color 0.12s ease;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        }

        .check-item:hover {
            border-color: var(--border-hover);
            background: #fdfdfd;
        }

        /* Checkbox Box (clickable to tick review/completion status) */
        .check-box {
            width: 19px;
            height: 19px;
            border: 1.8px solid #94a3b8;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            margin-top: 1px;
            transition: all 0.15s ease;
            background: #ffffff;
            cursor: pointer;
        }

        .check-item.done .check-box {
            background: var(--accent-detective);
            border-color: var(--accent-detective);
        }

        .check-box svg {
            display: none;
            width: 12px;
            height: 12px;
            stroke: #ffffff;
            stroke-width: 2.5;
            fill: none;
        }

        .check-item.done .check-box svg {
            display: block;
        }

        /* Item Text Label Wrapper with Link to Category */
        .check-label-wrap {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            flex: 1;
            min-width: 0;
            gap: 8px;
        }

        .check-label-link {
            font-size: 13.5px;
            font-weight: 600;
            color: var(--text-main);
            text-decoration: none;
            white-space: normal;
            word-break: break-word;
            overflow-wrap: break-word;
            line-height: 1.35;
            display: inline-flex;
            align-items: baseline;
            gap: 5px;
        }

        .check-label-link:hover {
            color: var(--accent-detective);
            text-decoration: underline;
        }

        .check-item.done .check-label-link {
            text-decoration: line-through;
            color: var(--text-light);
        }

        .ext-icon {
            font-size: 11px;
            color: var(--text-muted);
            opacity: 0.7;
            text-decoration: none !important;
        }

        .check-label-link:hover .ext-icon {
            color: var(--accent-detective);
            opacity: 1;
        }

        .item-priority-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #f97316;
            flex-shrink: 0;
            margin-top: 5px;
        }

        /* Completed Accordion Divider (Keep Style) */
        .completed-section {
            margin-top: 14px;
            border-top: 1px solid var(--border);
            padding-top: 10px;
        }

        .completed-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 12px;
            font-size: 12px;
            font-weight: 700;
            color: var(--text-muted);
            cursor: pointer;
            border-radius: var(--radius-sm);
            user-select: none;
            background: #f1f5f9;
            margin-bottom: 6px;
        }

        .completed-header:hover {
            background: #e2e8f0;
        }

        .completed-header .chevron {
            font-size: 11px;
            transition: transform 0.2s ease;
        }

        .completed-header.collapsed .chevron {
            transform: rotate(-90deg);
        }

        .completed-items-list.collapsed {
            display: none;
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 30px 16px;
            color: var(--text-muted);
            background: #ffffff;
            border: 1px dashed var(--border);
            border-radius: var(--radius-md);
            margin-top: 10px;
        }

        .empty-state-icon {
            font-size: 32px;
            margin-bottom: 6px;
            display: block;
        }

        .empty-state-title {
            font-weight: 700;
            font-size: 14px;
            color: var(--text-main);
            margin-bottom: 4px;
        }

        .empty-state-desc {
            font-size: 12px;
        }

        /* Country Selection Modal */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(4px);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 16px;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.2s ease;
        }

        .modal-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }

        .modal-card {
            background: #ffffff;
            border-radius: var(--radius-lg);
            width: 100%;
            max-width: 480px;
            max-height: 85vh;
            display: flex;
            flex-direction: column;
            box-shadow: var(--shadow-lg);
            overflow: hidden;
            transform: translateY(10px);
            transition: transform 0.2s ease;
        }

        .modal-overlay.active .modal-card {
            transform: translateY(0);
        }

        .modal-header {
            padding: 16px 20px 12px 20px;
            border-bottom: 1px solid var(--border);
        }

        .modal-title {
            font-size: 18px;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 4px;
        }

        .modal-subtitle {
            font-size: 13px;
            color: var(--text-muted);
            line-height: 1.4;
        }

        .modal-search-box {
            padding: 10px 20px;
            border-bottom: 1px solid var(--border);
            background: var(--bg);
        }

        .modal-search-box input {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            font-size: 13px;
            background: #ffffff;
        }

        .modal-body {
            overflow-y: auto;
            padding: 10px 14px;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
            gap: 8px;
        }

        .country-grid-btn {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 10px 8px;
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            color: var(--text-main);
            transition: all 0.15s ease;
            text-align: left;
        }

        .country-grid-btn:hover {
            border-color: var(--accent-detective);
            background: var(--accent-detective-light);
        }

        .country-grid-btn.selected {
            border-color: var(--accent-detective);
            background: var(--accent-detective-light);
            color: var(--accent-detective-dark);
            font-weight: 700;
        }

        .country-grid-flag {
            font-size: 20px;
            line-height: 1;
        }

        /* Footer with Sponsors and Citizen Science */
        footer.app-footer {
            margin-top: 35px;
            padding: 20px 14px 10px 14px;
            border-top: 1px solid var(--border);
            background: #ffffff;
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-sm);
            text-align: center;
        }

        .footer-sponsors {
            margin-bottom: 16px;
        }

        .footer-sponsor-label {
            font-size: 12px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }

        .footer-logos {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 24px;
            flex-wrap: wrap;
        }

        .footer-logos a {
            display: inline-flex;
            align-items: center;
            transition: opacity 0.2s ease;
        }

        .footer-logos a:hover {
            opacity: 0.85;
        }

        .sponsor-logo {
            max-height: 42px;
            width: auto;
            max-width: 150px;
            object-fit: contain;
        }

        .sponsor-logo-foodture {
            max-height: 38px;
        }

        .footer-citizen {
            margin-top: 14px;
            padding-top: 14px;
            border-top: 1px dashed var(--border);
            font-size: 12.5px;
            color: var(--text-main);
        }

        .footer-citizen-label {
            font-weight: 600;
            margin-bottom: 6px;
            display: block;
        }

        .footer-citizen-links {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        .citizen-link {
            color: var(--accent-detective-dark);
            text-decoration: none;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }

        .citizen-link:hover {
            text-decoration: underline;
        }

        .citizen-sep {
            color: var(--border-hover);
        }

        .footer-bottom-note {
            margin-top: 16px;
            font-size: 11px;
            color: var(--text-muted);
        }
    </style>
</head>
<body>

    <!-- Sticky App Header -->
    <header>
        <div class="header-container">
            <div class="brand-area">
                <span class="brand-emoji">🕵️‍♂️💻</span>
                <div class="brand-text">
                    <span class="brand-title" id="headerBrandTitle">Data Detective</span>
                    <span class="brand-badge" id="headerBrandBadge">Open Food Facts</span>
                </div>
            </div>
            <div class="header-actions">
                <a href="../photos-for-impact/" id="switchGameLink" class="switch-game-link">
                    <span>🤳 In store? Scan Champion</span>
                </a>
                <!-- Country Selector -->
                <div class="select-wrapper">
                    <select id="countrySelect" class="header-select country-select" aria-label="Select country"></select>
                </div>
                <!-- Language Selector -->
                <div class="select-wrapper">
                    <select id="langSelect" class="header-select lang-select" aria-label="Select language"></select>
                </div>
            </div>
        </div>
    </header>

    <main>
        <!-- Desktop Context & Slack Info Card -->
        <section class="context-card">
            <div class="context-left">
                <span class="context-icon">💻</span>
                <div class="context-text">
                    <strong id="detectiveWarningTitle">At home with your computer:</strong>
                    <span id="detectiveWarningDesc">Completing products is much easier on a desktop computer. Need help? Join #ingredients and #packaging on Slack!</span>
                </div>
            </div>
            <div class="context-buttons">
                <a href="https://slack.openfoodfacts.org" target="_blank" rel="noopener" class="btn-tool btn-slack">
                    <span>💬</span>
                    <span id="btnSlackLabel">Join Slack</span>
                </a>
                <a href="https://wiki.openfoodfacts.org/How_to_edit_a_product" target="_blank" rel="noopener" class="btn-tool btn-wiki">
                    <span>📖</span>
                    <span id="btnWikiLabel">How to edit</span>
                </a>
            </div>
        </section>

        <!-- Mission / Guide Card with the 4 Core Steps -->
        <section class="guide-card" id="guideCard">
            <div class="guide-header" id="guideToggle">
                <div class="guide-header-title">
                    <span id="guideTitleText">🕵️‍♂️ Data Detective Mission</span>
                </div>
                <button class="guide-toggle-btn" id="guideToggleBtn">Hide tips</button>
            </div>
            <div class="guide-body" id="guideBody">
                <div class="guide-headline" id="guideHeadline">Complete product data: photos, ingredients, nutrition, and packaging</div>
                <div class="guide-steps">
                    <div class="guide-step">
                        <span class="guide-step-icon">📸</span>
                        <div class="guide-step-text">
                            <strong id="step1Title">1. Select & Crop Photos</strong>
                            <span id="step1Desc">Select and crop clear photos for the ingredients list and nutrition facts table.</span>
                        </div>
                    </div>
                    <div class="guide-step">
                        <span class="guide-step-icon">🔤</span>
                        <div class="guide-step-text">
                            <strong id="step2Title">2. OCR Ingredients & Verify</strong>
                            <span id="step2Desc">Run the OCR to extract ingredients from the photo, then verify and correct the text.</span>
                        </div>
                    </div>
                    <div class="guide-step">
                        <span class="guide-step-icon">📊</span>
                        <div class="guide-step-text">
                            <strong id="step3Title">3. Enter Nutrition Facts</strong>
                            <span id="step3Desc">Transcribe the nutrition table values (energy, fats, sugars, salt, proteins...).</span>
                        </div>
                    </div>
                    <div class="guide-step">
                        <span class="guide-step-icon">📦</span>
                        <div class="guide-step-text">
                            <strong id="step4Title">4. Enter Packaging</strong>
                            <span id="step4Desc">Add packaging shapes, materials, and recycling instructions.</span>
                        </div>
                    </div>
                </div>
                <div class="guide-tip-banner">
                    <span>💡</span>
                    <span id="guideTipText"><strong>Pro-tip:</strong> Click any category to open its Open Food Facts page, find products to complete, and tick them off!</span>
                </div>
            </div>
        </section>

        <!-- Sticky Controls Bar: 2 Tabs (All Categories default active), Search, and Progress -->
        <div class="controls-sticky">
            <!-- 2 Tabs: All Categories (default active) & High Priority -->
            <div class="tab-bar">
                <button class="tab-btn active" data-tab="all" id="tabAll">
                    <span id="tabAllLabel">📋 All Categories</span>
                    <span class="badge-pill" id="badgeAll">0</span>
                </button>
                <button class="tab-btn" data-tab="missing" id="tabMissing">
                    <span id="tabMissingLabel">🔥 High Priority</span>
                    <span class="badge-pill" id="badgeMissing">0</span>
                </button>
            </div>

            <!-- Search + Reset Bar -->
            <div class="toolbar-row">
                <div class="search-box-wrapper">
                    <span class="search-icon">🔍</span>
                    <input type="search" id="searchInput" placeholder="Filter categories (e.g. beer, bread, cheese)..." autocomplete="off" />
                    <button class="search-clear-btn" id="searchClearBtn" aria-label="Clear search">✕</button>
                </div>
                <button class="btn-reset" id="btnReset" title="Clear all completed categories for this country">
                    <span>↺</span>
                    <span id="btnResetLabel">Reset</span>
                </button>
            </div>

            <!-- Mini Progress Indicator -->
            <div class="progress-strip">
                <div class="progress-bar-track">
                    <div class="progress-bar-fill" id="progressBarFill" style="width: 0%;"></div>
                </div>
                <span class="progress-text" id="progressSummary">0 / 0 completed</span>
            </div>
        </div>

        <!-- Active Categories Checklist with Links to Open Food Facts Category Pages -->
        <div class="checklist-container" id="activeChecklist">
            <!-- Items rendered via JS -->
        </div>

        <!-- Completed Categories Section (Google Keep Style) -->
        <section class="completed-section" id="completedSection" style="display: none;">
            <div class="completed-header" id="completedHeader">
                <span id="completedHeaderLabel">✓ Completed (0 items)</span>
                <span class="chevron">▾</span>
            </div>
            <div class="checklist-container completed-items-list" id="completedChecklist">
                <!-- Completed items rendered via JS -->
            </div>
        </section>

        <!-- Empty State Container -->
        <div id="emptyState" style="display: none;"></div>

        <!-- Footer with Sponsors and Citizen Science -->
        <footer class="app-footer">
            <div class="footer-sponsors">
                <div class="footer-sponsor-label" id="footerSupportedLabel">Project supported by:</div>
                <div class="footer-logos">
                    <a href="https://www.fondationdefrance.org" target="_blank" rel="noopener" title="Fondation de France">
                        <img src="https://thumb.wikimedia.org/wikipedia/fr/thumb/d/d2/Fondation_de_France.svg/langfr-330px-Fondation_de_France.svg.png" alt="Fondation de France" class="sponsor-logo" />
                    </a>
                    <a href="https://foodture-project.eu" target="_blank" rel="noopener" title="FOODTURE Project">
                        <img src="https://foodture-project.eu/wp-content/uploads/2025/05/FOODTURE-LOGO_Color-scaled.png" alt="FOODTURE Project" class="sponsor-logo sponsor-logo-foodture" />
                    </a>
                </div>
            </div>

            <div class="footer-citizen">
                <span class="footer-citizen-label" id="footerCitizenLabel">Discover our citizen science research:</span>
                <div class="footer-citizen-links">
                    <a href="https://world.openfoodfacts.net/citizen-science" target="_blank" rel="noopener" class="citizen-link">
                        <span>🔬</span>
                        <span id="linkCitizenEn">Citizen Science (EN)</span>
                    </a>
                    <span class="citizen-sep">·</span>
                    <a href="https://fr.openfoodfacts.net/science-citoyenne" target="_blank" rel="noopener" class="citizen-link">
                        <span>🔬</span>
                        <span id="linkCitizenFr">Science Citoyenne (FR)</span>
                    </a>
                </div>
            </div>

            <div class="footer-bottom-note">
                <span>Open Food Facts · Data Detective · <span id="footerStorageLabel">Completed items saved locally on your device</span></span>
            </div>
        </footer>
    </main>

    <!-- Country Selection Modal -->
    <div class="modal-overlay" id="countryModal" role="dialog" aria-modal="true">
        <div class="modal-card">
            <div class="modal-header">
                <h2 class="modal-title" id="modalTitle">Select your country</h2>
                <p class="modal-subtitle" id="modalSubtitle">Choose your country to see the categories needed for your local food basket:</p>
            </div>
            <div class="modal-search-box">
                <input type="search" id="modalCountrySearch" placeholder="Search country..." autocomplete="off" />
            </div>
            <div class="modal-body" id="modalCountryGrid">
                <!-- Countries rendered via JS -->
            </div>
        </div>
    </div>

    <!-- Live Data Feeds -->
    <script src="data.js"></script>
    <script>
        const TRANSLATIONS = __TRANSLATIONS_JSON__;
        const LANGUAGE_NAMES = __LANG_NAMES_JSON__;

        // State
        let currentCountry = null;
        let currentLang = 'en';
        let currentTab = 'all'; // Default active tab is 'all' for Data Detective!
        let currentSearch = '';
        let completedCollapsed = false;

        function t(key, vars = {}) {
            const langDict = TRANSLATIONS[currentLang] || TRANSLATIONS['en'];
            let text = langDict[key] || (TRANSLATIONS['en'] ? TRANSLATIONS['en'][key] : '') || key;
            for (const [k, v] of Object.entries(vars)) {
                text = text.replace(new RegExp(`\\\\{${k}\\\\}`, 'g'), v);
            }
            return text;
        }

        function getStorageKey(country) {
            return 'data_detective_done_' + country;
        }

        function getCheckedTags(country) {
            try {
                // Check new key first, fallback to previous taxonomy key if available
                let stored = localStorage.getItem(getStorageKey(country));
                if (!stored) {
                    stored = localStorage.getItem('taxonomy_wiz_done_' + country);
                }
                return stored ? new Set(JSON.parse(stored)) : new Set();
            } catch (e) {
                return new Set();
            }
        }

        function saveCheckedTags(country, tagSet) {
            try {
                localStorage.setItem(getStorageKey(country), JSON.stringify(Array.from(tagSet)));
            } catch (e) {}
        }

        function getParam(param) {
            const params = new URLSearchParams(window.location.search);
            return params.get(param);
        }

        function toggleItem(tag) {
            if (!currentCountry) return;
            const checkedSet = getCheckedTags(currentCountry);
            if (checkedSet.has(tag)) {
                checkedSet.delete(tag);
            } else {
                checkedSet.add(tag);
                if (navigator.vibrate) {
                    try { navigator.vibrate(12); } catch (e) {}
                }
            }
            saveCheckedTags(currentCountry, checkedSet);
            render();
        }

        function resetCurrentCountry() {
            if (!currentCountry) return;
            const countryMeta = (window.CAMPAIGN_STATS && window.CAMPAIGN_STATS.countries) ? window.CAMPAIGN_STATS.countries[currentCountry] : null;
            const countryName = countryMeta ? countryMeta.name : currentCountry.toUpperCase();
            if (confirm(t('reset_confirm', { country: countryName }))) {
                localStorage.removeItem(getStorageKey(currentCountry));
                render();
            }
        }

        function detectBrowserCountry(countries) {
            const langList = navigator.languages || [navigator.language || ''];
            for (const l of langList) {
                if (!l) continue;
                const parts = l.split('-');
                if (parts.length > 1) {
                    let region = parts[1].toLowerCase();
                    if (region === 'gb') region = 'uk';
                    if (countries[region]) {
                        return region;
                    }
                }
            }
            try {
                const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
                const tzMap = {
                    'Europe/Vienna': 'at', 'Europe/Brussels': 'be', 'Europe/Sofia': 'bg',
                    'Europe/Zagreb': 'hr', 'Asia/Nicosia': 'cy', 'Europe/Nicosia': 'cy',
                    'Europe/Prague': 'cs', 'Europe/Copenhagen': 'dk', 'Europe/Tallinn': 'ee',
                    'Europe/Helsinki': 'fi', 'Europe/Paris': 'fr', 'Europe/Berlin': 'de',
                    'Europe/Busingen': 'de', 'Europe/Athens': 'el', 'Europe/Budapest': 'hu',
                    'Europe/Dublin': 'ie', 'Europe/Rome': 'it', 'Europe/Riga': 'lv',
                    'Europe/Vilnius': 'lt', 'Europe/Luxembourg': 'lu', 'Europe/Malta': 'mt',
                    'Europe/Podgorica': 'me', 'Europe/Amsterdam': 'nl', 'Europe/Oslo': 'no',
                    'Europe/Warsaw': 'pl', 'Europe/Lisbon': 'pt', 'Atlantic/Madeira': 'pt',
                    'Atlantic/Azores': 'pt', 'Europe/Bucharest': 'ro', 'Europe/Belgrade': 'rs',
                    'Europe/Bratislava': 'sk', 'Europe/Ljubljana': 'si', 'Europe/Madrid': 'es',
                    'Atlantic/Canary': 'es', 'Africa/Ceuta': 'es', 'Europe/Stockholm': 'se',
                    'Europe/Zurich': 'ch', 'Europe/London': 'uk'
                };
                if (tzMap[tz] && countries[tzMap[tz]]) {
                    return tzMap[tz];
                }
            } catch (e) {}

            for (const l of langList) {
                const primary = (l.split('-')[0] || '').toLowerCase();
                const langToCountry = {
                    'pl': 'pl', 'el': 'el', 'hu': 'hu', 'cs': 'cs', 'sk': 'sk',
                    'ro': 'ro', 'bg': 'bg', 'da': 'dk', 'fi': 'fi', 'et': 'ee',
                    'lv': 'lv', 'lt': 'lt', 'hr': 'hr', 'sl': 'sl', 'pt': 'pt',
                    'sv': 'se', 'nl': 'nl'
                };
                if (langToCountry[primary] && countries[langToCountry[primary]]) {
                    return langToCountry[primary];
                }
            }
            return null;
        }

        function openCountryModal() {
            const modal = document.getElementById('countryModal');
            modal.classList.add('active');
            renderModalCountryGrid();
            document.getElementById('modalCountrySearch').focus();
        }

        function closeCountryModal() {
            const modal = document.getElementById('countryModal');
            modal.classList.remove('active');
        }

        function renderModalCountryGrid() {
            const grid = document.getElementById('modalCountryGrid');
            const searchVal = (document.getElementById('modalCountrySearch').value || '').toLowerCase().trim();
            grid.innerHTML = '';

            const countries = window.CAMPAIGN_STATS ? window.CAMPAIGN_STATS.countries : {};
            const sortedCodes = Object.keys(countries).sort((a, b) => countries[a].name.localeCompare(countries[b].name));

            sortedCodes.forEach(code => {
                const c = countries[code];
                if (searchVal && !c.name.toLowerCase().includes(searchVal) && !code.includes(searchVal)) {
                    return;
                }
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'country-grid-btn' + (currentCountry === code ? ' selected' : '');
                btn.innerHTML = `<span class="country-grid-flag">${c.flag}</span><span>${c.name}</span>`;
                btn.addEventListener('click', () => {
                    selectCountry(code);
                    closeCountryModal();
                });
                grid.appendChild(btn);
            });
        }

        function selectCountry(code) {
            currentCountry = code;
            try {
                localStorage.setItem('scan_champion_country', code);
            } catch (e) {}

            const url = new URL(window.location);
            url.searchParams.set('country', code);
            window.history.replaceState({}, '', url);

            const select = document.getElementById('countrySelect');
            if (select) select.value = code;

            const storedLang = localStorage.getItem('scan_champion_lang');
            const urlLang = getParam('lang');
            if (!urlLang && !storedLang) {
                const cMeta = window.CAMPAIGN_STATS.countries[code];
                if (cMeta && cMeta.languages && cMeta.languages[0]) {
                    selectLanguage(cMeta.languages[0], false);
                }
            }

            updateSwitchLink();

            if (window._paq) {
                const countries = window.CAMPAIGN_STATS.countries;
                _paq.push(['setCustomUrl', window.location.href]);
                _paq.push(['setDocumentTitle', 'Data Detective - ' + (countries[code] ? countries[code].name : code.toUpperCase())]);
                _paq.push(['trackPageView']);
            }

            render();
        }

        function selectLanguage(langCode, updateStorage = true) {
            if (!TRANSLATIONS[langCode]) {
                langCode = 'en';
            }
            currentLang = langCode;

            if (updateStorage) {
                try {
                    localStorage.setItem('scan_champion_lang', langCode);
                } catch (e) {}
            }

            const url = new URL(window.location);
            url.searchParams.set('lang', langCode);
            window.history.replaceState({}, '', url);

            const langSelect = document.getElementById('langSelect');
            if (langSelect) langSelect.value = langCode;

            updateSwitchLink();
            applyTranslations();
            render();
        }

        function updateSwitchLink() {
            const link = document.getElementById('switchGameLink');
            if (link) {
                link.href = `../photos-for-impact/?country=${encodeURIComponent(currentCountry || 'at')}&lang=${encodeURIComponent(currentLang || 'en')}`;
            }
        }

        function getCategoryUrl(categoryName) {
            const langDomain = (currentLang === 'en') ? 'world' : currentLang;
            return `https://${langDomain}.openfoodfacts.org/facets/categories/${encodeURIComponent(categoryName)}`;
        }

        function applyTranslations() {
            document.title = `${t('detective_title')} 🕵️‍♂️💻 — Open Food Facts`;
            document.getElementById('headerBrandTitle').textContent = t('detective_title');
            document.getElementById('headerBrandBadge').textContent = t('detective_badge');
            document.getElementById('guideTitleText').textContent = t('detective_guide_title');

            const isCollapsed = document.getElementById('guideBody').classList.contains('collapsed');
            document.getElementById('guideToggleBtn').textContent = isCollapsed ? t('guide_show') : t('guide_hide');

            document.getElementById('detectiveWarningTitle').textContent = t('detective_warning_title');
            document.getElementById('detectiveWarningDesc').textContent = t('detective_warning_desc');
            document.getElementById('btnSlackLabel').textContent = t('detective_slack_btn');
            document.getElementById('btnWikiLabel').textContent = t('detective_wiki_btn');

            document.getElementById('guideHeadline').textContent = t('detective_guide_headline');
            document.getElementById('step1Title').textContent = t('detective_step1_title');
            document.getElementById('step1Desc').textContent = t('detective_step1_desc');
            document.getElementById('step2Title').textContent = t('detective_step2_title');
            document.getElementById('step2Desc').textContent = t('detective_step2_desc');
            document.getElementById('step3Title').textContent = t('detective_step3_title');
            document.getElementById('step3Desc').textContent = t('detective_step3_desc');
            document.getElementById('step4Title').textContent = t('detective_step4_title');
            document.getElementById('step4Desc').textContent = t('detective_step4_desc');

            document.getElementById('guideTipText').innerHTML = `<strong>${t('detective_tip_text').split(':')[0]}:</strong> ${t('detective_tip_text').split(':').slice(1).join(':') || t('detective_tip_text')}`;

            document.getElementById('tabAllLabel').textContent = t('detective_tab_all');
            document.getElementById('tabMissingLabel').textContent = t('detective_tab_priority');
            document.getElementById('searchInput').placeholder = t('search_placeholder');
            document.getElementById('btnResetLabel').textContent = t('reset_btn');

            document.getElementById('footerSupportedLabel').textContent = t('footer_supported');
            document.getElementById('footerCitizenLabel').textContent = t('footer_citizen');
            document.getElementById('linkCitizenEn').textContent = t('footer_citizen_link_en');
            document.getElementById('linkCitizenFr').textContent = t('footer_citizen_link_fr');
            document.getElementById('footerStorageLabel').textContent = t('footer_storage');

            document.getElementById('modalTitle').textContent = t('modal_title');
            document.getElementById('modalSubtitle').textContent = t('modal_subtitle');
            document.getElementById('modalCountrySearch').placeholder = t('modal_search_placeholder');

            const switchLink = document.getElementById('switchGameLink');
            if (switchLink) {
                switchLink.textContent = t('switch_to_scan');
            }
        }

        function init() {
            if (!window.CAMPAIGN_STATS || !window.COUNTRIES_DATA) {
                console.error('Campaign data not loaded');
                return;
            }

            const countries = window.CAMPAIGN_STATS.countries;

            const countrySelect = document.getElementById('countrySelect');
            countrySelect.innerHTML = '';
            const sortedCodes = Object.keys(countries).sort((a, b) => countries[a].name.localeCompare(countries[b].name));
            sortedCodes.forEach(code => {
                const c = countries[code];
                const opt = document.createElement('option');
                opt.value = code;
                opt.textContent = `${c.flag} ${c.name}`;
                countrySelect.appendChild(opt);
            });

            const langSelect = document.getElementById('langSelect');
            langSelect.innerHTML = '';
            const sortedLangs = Object.keys(TRANSLATIONS).sort((a, b) => (LANGUAGE_NAMES[a] || a).localeCompare(LANGUAGE_NAMES[b] || b));
            sortedLangs.forEach(lang => {
                const opt = document.createElement('option');
                opt.value = lang;
                opt.textContent = LANGUAGE_NAMES[lang] || lang.toUpperCase();
                langSelect.appendChild(opt);
            });

            const urlLang = getParam('lang');
            const storedLang = localStorage.getItem('scan_champion_lang');
            const browserLang = (navigator.language || '').split('-')[0].toLowerCase();

            if (urlLang && TRANSLATIONS[urlLang]) {
                currentLang = urlLang;
            } else if (storedLang && TRANSLATIONS[storedLang]) {
                currentLang = storedLang;
            } else if (TRANSLATIONS[browserLang]) {
                currentLang = browserLang;
            } else {
                currentLang = 'en';
            }
            langSelect.value = currentLang;

            const urlCountry = getParam('country');
            const storedCountry = localStorage.getItem('scan_champion_country');

            if (urlCountry && countries[urlCountry.toLowerCase()]) {
                currentCountry = urlCountry.toLowerCase();
            } else if (storedCountry && countries[storedCountry.toLowerCase()]) {
                currentCountry = storedCountry.toLowerCase();
            } else {
                const detected = detectBrowserCountry(countries);
                if (detected) {
                    currentCountry = detected;
                }
            }

            if (currentCountry) {
                countrySelect.value = currentCountry;
                try {
                    localStorage.setItem('scan_champion_country', currentCountry);
                } catch (e) {}
            } else {
                openCountryModal();
            }

            countrySelect.addEventListener('change', (e) => {
                selectCountry(e.target.value);
            });

            langSelect.addEventListener('change', (e) => {
                selectLanguage(e.target.value, true);
            });

            document.getElementById('modalCountrySearch').addEventListener('input', () => {
                renderModalCountryGrid();
            });

            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    currentTab = btn.getAttribute('data-tab');
                    render();
                });
            });

            const searchInput = document.getElementById('searchInput');
            const clearBtn = document.getElementById('searchClearBtn');

            searchInput.addEventListener('input', (e) => {
                currentSearch = e.target.value.toLowerCase().trim();
                clearBtn.classList.toggle('visible', !!currentSearch);
                render();
            });

            clearBtn.addEventListener('click', () => {
                searchInput.value = '';
                currentSearch = '';
                clearBtn.classList.remove('visible');
                render();
                searchInput.focus();
            });

            document.getElementById('btnReset').addEventListener('click', resetCurrentCountry);

            const completedHeader = document.getElementById('completedHeader');
            completedHeader.addEventListener('click', () => {
                completedCollapsed = !completedCollapsed;
                completedHeader.classList.toggle('collapsed', completedCollapsed);
                document.getElementById('completedChecklist').classList.toggle('collapsed', completedCollapsed);
            });

            const guideBody = document.getElementById('guideBody');
            const guideToggle = document.getElementById('guideToggle');
            const guideToggleBtn = document.getElementById('guideToggleBtn');

            const isGuideCollapsed = localStorage.getItem('data_detective_guide_collapsed') === 'true';
            if (isGuideCollapsed) {
                guideBody.classList.add('collapsed');
            }

            guideToggle.addEventListener('click', () => {
                const collapsed = guideBody.classList.toggle('collapsed');
                guideToggleBtn.textContent = collapsed ? t('guide_show') : t('guide_hide');
                try {
                    localStorage.setItem('data_detective_guide_collapsed', collapsed ? 'true' : 'false');
                } catch (e) {}
            });

            updateSwitchLink();
            applyTranslations();
            renderModalCountryGrid();
            if (currentCountry) {
                render();
            }
        }

        function createItemNode(item, isChecked, isMissing) {
            const div = document.createElement('div');
            div.className = 'check-item' + (isChecked ? ' done' : '');
            div.setAttribute('data-tag', item.category_tag);

            const catUrl = getCategoryUrl(item.category_name);

            div.innerHTML = `
                <div class="check-box" aria-label="Mark category as completed">
                    <svg viewBox="0 0 24 24">
                        <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                </div>
                <div class="check-label-wrap">
                    <a href="${catUrl}" target="_blank" rel="noopener" class="check-label-link" title="${t('detective_open_category')}">
                        <span>${item.category_name}</span>
                        <span class="ext-icon" aria-hidden="true">↗</span>
                    </a>
                    ${(currentTab === 'all' && isMissing) ? '<span class="item-priority-dot" title="High Priority"></span>' : ''}
                </div>
            `;

            div.querySelector('.check-box').addEventListener('click', (e) => {
                e.stopPropagation();
                toggleItem(item.category_tag);
            });

            return div;
        }

        function render() {
            if (!currentCountry) return;
            const countryFull = window.COUNTRIES_DATA[currentCountry];
            if (!countryFull) return;

            const allCategories = countryFull.categories;
            const checkedSet = getCheckedTags(currentCountry);

            const missingCategories = allCategories.filter(c => !c.has_code);
            const totalMissing = missingCategories.length;
            const checkedMissing = missingCategories.filter(c => checkedSet.has(c.category_tag)).length;

            const totalAll = allCategories.length;
            const checkedAll = allCategories.filter(c => checkedSet.has(c.category_tag)).length;

            document.getElementById('badgeMissing').textContent = `${checkedMissing}/${totalMissing}`;
            document.getElementById('badgeAll').textContent = `${checkedAll}/${totalAll}`;

            const sourcePool = (currentTab === 'missing') ? missingCategories : allCategories;
            const currentCheckedCount = (currentTab === 'missing') ? checkedMissing : checkedAll;
            const currentTotalCount = sourcePool.length;

            const pct = currentTotalCount > 0 ? Math.round((currentCheckedCount / currentTotalCount) * 100) : 0;
            document.getElementById('progressBarFill').style.width = `${pct}%`;
            document.getElementById('progressSummary').textContent = t('detective_progress_summary', {
                checked: currentCheckedCount,
                total: currentTotalCount,
                pct: pct
            });

            let filtered = sourcePool;
            if (currentSearch) {
                filtered = sourcePool.filter(c => 
                    c.category_name.toLowerCase().includes(currentSearch) ||
                    c.category_tag.toLowerCase().includes(currentSearch)
                );
            }

            const activeItems = [];
            const completedItems = [];

            filtered.forEach(item => {
                const isChecked = checkedSet.has(item.category_tag);
                if (isChecked) {
                    completedItems.push(item);
                } else {
                    activeItems.push(item);
                }
            });

            const activeListEl = document.getElementById('activeChecklist');
            activeListEl.innerHTML = '';
            activeItems.forEach(item => {
                activeListEl.appendChild(createItemNode(item, false, !item.has_code));
            });

            const completedSection = document.getElementById('completedSection');
            const completedListEl = document.getElementById('completedChecklist');
            const completedHeaderLabel = document.getElementById('completedHeaderLabel');

            if (completedItems.length > 0) {
                completedSection.style.display = 'block';
                completedHeaderLabel.textContent = `✓ ${t('detective_completed_label', { count: completedItems.length })}`;
                completedListEl.innerHTML = '';
                completedItems.forEach(item => {
                    completedListEl.appendChild(createItemNode(item, true, !item.has_code));
                });
            } else {
                completedSection.style.display = 'none';
            }

            const emptyStateEl = document.getElementById('emptyState');
            if (filtered.length === 0) {
                emptyStateEl.style.display = 'block';
                if (currentSearch) {
                    emptyStateEl.innerHTML = `
                        <div class="empty-state">
                            <div class="empty-state-icon">🔍</div>
                            <div class="empty-state-title">${t('empty_search_title')}</div>
                            <div class="empty-state-desc">${t('empty_search_desc', { query: currentSearch })}</div>
                        </div>
                    `;
                } else if (currentTab === 'missing' && totalMissing === 0) {
                    emptyStateEl.innerHTML = `
                        <div class="empty-state">
                            <div class="empty-state-icon">🎉</div>
                            <div class="empty-state-title">${t('detective_empty_priority_title')}</div>
                            <div class="empty-state-desc">${t('detective_empty_priority_desc')}</div>
                        </div>
                    `;
                }
            } else if (activeItems.length === 0 && completedItems.length > 0 && !currentSearch) {
                emptyStateEl.style.display = 'block';
                emptyStateEl.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">🏆</div>
                        <div class="empty-state-title">${t('detective_empty_all_done_title', { count: completedItems.length })}</div>
                        <div class="empty-state-desc">${t('detective_empty_all_done_desc')}</div>
                    </div>
                `;
            } else {
                emptyStateEl.style.display = 'none';
            }
        }

        window.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
"""
    return html.replace(
        '__TRANSLATIONS_JSON__',
        json.dumps(TRANSLATIONS, ensure_ascii=False)
    ).replace(
        '__LANG_NAMES_JSON__',
        json.dumps(LANGUAGE_NAMES, ensure_ascii=False)
    )


def build_redirect_html(target_url):
    """Build redirect HTML for legacy URLs."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Redirecting to Data Detective...</title>
    <script>
        const currentUrl = new URL(window.location.href);
        const target = new URL("{target_url}", window.location.href);
        for (const [key, val] of currentUrl.searchParams.entries()) {{
            target.searchParams.set(key, val);
        }}
        window.location.replace(target.href);
    </script>
</head>
<body>
    <p>Redirecting to <a href="{target_url}">Data Detective</a>...</p>
</body>
</html>
"""


def build_scan_champion_html():
    """Build Scan Champion HTML file (with link to Data Detective in header)."""
    with open(os.path.join(BASE_DIR, 'photos-for-impact', 'index.html'), 'r', encoding='utf-8') as f:
        content = f.read()

    # Ensure link points to Data Detective
    content = content.replace('../taxonomy-wiz/', '../data-detective/')
    content = content.replace('Taxonomy Wiz', 'Data Detective')
    content = content.replace('🧑💻 At home? Data Detective', '🕵️‍♂️ At home? Data Detective')

    return content


def main():
    print("Building Scan Champion and Data Detective web hubs...")

    # 1. Build Data Detective HTML
    detective_html = build_data_detective_html()
    detective_dest_files = [
        os.path.join(BASE_DIR, 'data-detective', 'index.html'),
        os.path.join(BASE_DIR, 'release-website', 'data-detective', 'index.html'),
    ]
    for dest in detective_dest_files:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(detective_html.strip() + '\n')
        print(f"Generated {dest} successfully!")

    # 2. Copy data.js to data-detective folders
    src_data_js = os.path.join(BASE_DIR, 'photos-for-impact', 'data.js')
    if os.path.exists(src_data_js):
        for det_dir in ['data-detective', os.path.join('release-website', 'data-detective')]:
            dst = os.path.join(BASE_DIR, det_dir, 'data.js')
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src_data_js, dst)
            print(f"Copied data.js to {dst}")

    # 3. Update legacy taxonomy-wiz folders with redirect to data-detective
    redirect_html = build_redirect_html('../data-detective/')
    for wiz_dir in ['taxonomy-wiz', os.path.join('release-website', 'taxonomy-wiz')]:
        dst = os.path.join(BASE_DIR, wiz_dir, 'index.html')
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, 'w', encoding='utf-8') as f:
            f.write(redirect_html.strip() + '\n')
        print(f"Generated legacy redirect {dst}")

    # 4. Update Scan Champion with Data Detective switch link
    scan_html = build_scan_champion_html()
    scan_dest_files = [
        os.path.join(BASE_DIR, 'photos-for-impact', 'index.html'),
        os.path.join(BASE_DIR, 'release-website', 'photos-for-impact', 'index.html')
    ]
    for dest in scan_dest_files:
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(scan_html.strip() + '\n')
        print(f"Updated {dest} successfully!")

    print("All builds completed successfully!")


if __name__ == '__main__':
    main()
