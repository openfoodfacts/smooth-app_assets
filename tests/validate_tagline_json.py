#!/usr/bin/env python3
"""
Validate tagline JSON files against the schema expected by the smooth-app.

This script validates the structure of tagline JSON files to ensure they comply
with the expected format defined in:
https://github.com/openfoodfacts/smooth-app/blob/develop/packages/smooth_app/lib/data_models/news_feed/newsfeed_json.dart
"""

import json
import sys
import os


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_non_empty_string(value, field_name, allow_none=True):
    """Validate that a value is a non-empty string if present."""
    if value is None:
        if allow_none:
            return
        raise ValidationError(f"{field_name} is required and cannot be None")
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string, got {type(value).__name__}")
    if not value.strip():
        raise ValidationError(f"{field_name} must not be empty")


def validate_color(value, field_name):
    """Validate that a color value starts with '#'."""
    if value is None:
        return
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string, got {type(value).__name__}")
    if not value.startswith('#'):
        raise ValidationError(f"{field_name} must start with '#', got '{value}'")


def validate_image(image, field_name, is_default_translation=False):
    """Validate an image object."""
    if image is None:
        return
    
    if not isinstance(image, dict):
        raise ValidationError(f"{field_name} must be an object, got {type(image).__name__}")
    
    # Validate url
    url = image.get('url')
    if is_default_translation and url is not None:
        # If image is present in default translation, url must be non-empty
        validate_non_empty_string(url, f"{field_name}.url", allow_none=False)
    elif url is not None:
        validate_non_empty_string(url, f"{field_name}.url")
    
    # Validate width (must be between 0.0 and 1.0 if present)
    width = image.get('width')
    if width is not None:
        if not isinstance(width, (int, float)):
            raise ValidationError(f"{field_name}.width must be a number, got {type(width).__name__}")
        if width < 0.0 or width > 1.0:
            raise ValidationError(f"{field_name}.width must be between 0.0 and 1.0, got {width}")
    
    # Validate alt (must not be empty if present)
    alt = image.get('alt')
    if alt is not None:
        validate_non_empty_string(alt, f"{field_name}.alt")


def validate_style(style, field_name):
    """Validate a style object."""
    if style is None:
        return
    
    if not isinstance(style, dict):
        raise ValidationError(f"{field_name} must be an object, got {type(style).__name__}")
    
    color_fields = [
        'title_background',
        'title_text_color',
        'title_indicator_color',
        'message_background',
        'message_text_color',
        'button_background',
        'button_text_color',
        'content_background_color'
    ]
    
    for color_field in color_fields:
        validate_color(style.get(color_field), f"{field_name}.{color_field}")


def validate_translation(translation, locale, field_name, is_default=False):
    """Validate a translation object."""
    if not isinstance(translation, dict):
        raise ValidationError(f"{field_name} must be an object, got {type(translation).__name__}")
    
    # For default translation, title and message are required
    if is_default:
        title = translation.get('title')
        message = translation.get('message')
        
        if title is None:
            raise ValidationError(f"{field_name}.title is required for 'default' translation")
        validate_non_empty_string(title, f"{field_name}.title", allow_none=False)
        
        if message is None:
            raise ValidationError(f"{field_name}.message is required for 'default' translation")
        validate_non_empty_string(message, f"{field_name}.message", allow_none=False)
    else:
        # For non-default translations, fields are optional but must not be empty if present
        if 'title' in translation:
            validate_non_empty_string(translation.get('title'), f"{field_name}.title")
        if 'message' in translation:
            validate_non_empty_string(translation.get('message'), f"{field_name}.message")
    
    # url and button_label must not be empty if present
    if 'url' in translation:
        validate_non_empty_string(translation.get('url'), f"{field_name}.url")
    if 'button_label' in translation:
        validate_non_empty_string(translation.get('button_label'), f"{field_name}.button_label")
    
    # Validate images
    validate_image(translation.get('image'), f"{field_name}.image", is_default_translation=is_default)
    validate_image(translation.get('image_dark'), f"{field_name}.image_dark", is_default_translation=is_default)


def validate_news_item(news_id, news_item, field_name):
    """Validate a news item."""
    if not isinstance(news_item, dict):
        raise ValidationError(f"{field_name} must be an object, got {type(news_item).__name__}")
    
    # url is required and must not be empty
    url = news_item.get('url')
    if url is None:
        raise ValidationError(f"{field_name}.url is required")
    validate_non_empty_string(url, f"{field_name}.url", allow_none=False)
    
    # translations is required and must contain 'default'
    translations = news_item.get('translations')
    if translations is None:
        raise ValidationError(f"{field_name}.translations is required")
    if not isinstance(translations, dict):
        raise ValidationError(f"{field_name}.translations must be an object, got {type(translations).__name__}")
    if 'default' not in translations:
        raise ValidationError(f"{field_name}.translations must contain 'default' key")
    
    # Validate each translation
    for locale, translation in translations.items():
        is_default = (locale == 'default')
        validate_translation(translation, locale, f"{field_name}.translations.{locale}", is_default)
    
    # min_launches must be a non-negative integer if present
    min_launches = news_item.get('min_launches')
    if min_launches is not None:
        if not isinstance(min_launches, int):
            raise ValidationError(f"{field_name}.min_launches must be an integer, got {type(min_launches).__name__}")
        if min_launches < 0:
            raise ValidationError(f"{field_name}.min_launches must be non-negative, got {min_launches}")
    
    # Validate style if present
    validate_style(news_item.get('style'), f"{field_name}.style")


def validate_feed_locale_item(item, field_name):
    """Validate a feed locale item."""
    if not isinstance(item, dict):
        raise ValidationError(f"{field_name} must be an object, got {type(item).__name__}")
    
    # id is required and must not be empty
    item_id = item.get('id')
    if item_id is None:
        raise ValidationError(f"{field_name}.id is required")
    validate_non_empty_string(item_id, f"{field_name}.id", allow_none=False)
    
    # Validate override if present
    override = item.get('override')
    if override is not None:
        if not isinstance(override, dict):
            raise ValidationError(f"{field_name}.override must be an object, got {type(override).__name__}")
        
        # url must not be empty if present
        if 'url' in override:
            validate_non_empty_string(override.get('url'), f"{field_name}.override.url")
        
        # Validate style if present
        validate_style(override.get('style'), f"{field_name}.override.style")


def validate_feed_locale(locale_data, field_name):
    """Validate a feed locale object."""
    if not isinstance(locale_data, dict):
        raise ValidationError(f"{field_name} must be an object, got {type(locale_data).__name__}")
    
    # news is required and must be an array
    news = locale_data.get('news')
    if news is None:
        raise ValidationError(f"{field_name}.news is required")
    if not isinstance(news, list):
        raise ValidationError(f"{field_name}.news must be an array, got {type(news).__name__}")
    
    # Validate each news item in the feed
    for i, item in enumerate(news):
        validate_feed_locale_item(item, f"{field_name}.news[{i}]")


def validate_tagline_feed(tagline_feed, news_ids, field_name="tagline_feed", check_references=True):
    """Validate the tagline_feed section."""
    if not isinstance(tagline_feed, dict):
        raise ValidationError(f"{field_name} must be an object, got {type(tagline_feed).__name__}")
    
    # Must contain 'default' key
    if 'default' not in tagline_feed:
        raise ValidationError(f"{field_name} must contain 'default' key")
    
    # Validate each locale
    for locale, locale_data in tagline_feed.items():
        validate_feed_locale(locale_data, f"{field_name}.{locale}")
        
        # Check that all referenced news IDs exist (only if news section is valid)
        if check_references:
            news = locale_data.get('news', [])
            for i, item in enumerate(news):
                item_id = item.get('id')
                if item_id and item_id not in news_ids:
                    raise ValidationError(
                        f"{field_name}.{locale}.news[{i}].id references non-existent news item '{item_id}'"
                    )


def validate_tagline_json(data, file_path=""):
    """Validate the complete tagline JSON structure."""
    prefix = f"[{file_path}] " if file_path else ""
    errors = []
    
    if not isinstance(data, dict):
        errors.append(f"{prefix}Root must be an object, got {type(data).__name__}")
        return errors
    
    # Validate 'news' section
    news = data.get('news')
    if news is None:
        errors.append(f"{prefix}'news' key is required at root level")
    elif not isinstance(news, dict):
        errors.append(f"{prefix}'news' must be an object, got {type(news).__name__}")
    else:
        for news_id, news_item in news.items():
            try:
                validate_news_item(news_id, news_item, f"news.{news_id}")
            except ValidationError as e:
                errors.append(f"{prefix}{e}")
    
    # Validate 'tagline_feed' section
    tagline_feed = data.get('tagline_feed')
    if tagline_feed is None:
        errors.append(f"{prefix}'tagline_feed' key is required at root level")
    elif not isinstance(tagline_feed, dict):
        errors.append(f"{prefix}'tagline_feed' must be an object, got {type(tagline_feed).__name__}")
    else:
        # Only validate news ID references if news section is valid
        if isinstance(news, dict):
            news_ids = set(news.keys())
            try:
                validate_tagline_feed(tagline_feed, news_ids, check_references=True)
            except ValidationError as e:
                errors.append(f"{prefix}{e}")
        else:
            # Still validate tagline_feed structure, but skip reference checks
            try:
                validate_tagline_feed(tagline_feed, set(), check_references=False)
            except ValidationError as e:
                errors.append(f"{prefix}{e}")
    
    return errors


def validate_file(file_path):
    """Validate a single JSON file."""
    print(f"Validating {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"[{file_path}] Invalid JSON: {e}"]
    except FileNotFoundError:
        return [f"[{file_path}] File not found"]
    
    return validate_tagline_json(data, file_path)


def main():
    """Main entry point."""
    # Get the script directory and project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Check if files are provided as command-line arguments
    if len(sys.argv) > 1:
        json_files = sys.argv[1:]
    else:
        # Default to the standard tagline JSON files
        json_files = [
            os.path.join(project_root, 'prod', 'tagline', 'android', 'main.json'),
            os.path.join(project_root, 'prod', 'tagline', 'ios', 'main.json'),
            os.path.join(project_root, 'prod', 'tagline', 'web', 'main.json'),
        ]
    
    all_errors = []
    
    for json_file in json_files:
        if os.path.exists(json_file):
            errors = validate_file(json_file)
            all_errors.extend(errors)
        else:
            print(f"Warning: {json_file} does not exist, skipping...")
    
    if all_errors:
        print("\n" + "=" * 60)
        print("VALIDATION FAILED")
        print("=" * 60)
        for error in all_errors:
            print(f"  ✗ {error}")
        print(f"\nTotal errors: {len(all_errors)}")
        sys.exit(1)
    else:
        print("\n" + "=" * 60)
        print("VALIDATION PASSED")
        print("=" * 60)
        print("All tagline JSON files are valid!")
        sys.exit(0)


if __name__ == '__main__':
    main()
