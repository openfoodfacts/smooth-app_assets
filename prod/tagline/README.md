## How to Update Messages in the Open Food Facts Mobile App
- This guide will help newcomers update the [`/prod/tagline/android/main.json`](https://github.com/openfoodfacts/smooth-app_assets/prod/tagline/android/main.json) file (used for the Android app), the equivalent iOS file, [`/prod/tagline/ios/main.json`](https://github.com/openfoodfacts/smooth-app_assets/prod/tagline/ios/main.json), and the web file, [`/prod/tagline/web/main.json`](https://github.com/openfoodfacts/smooth-app_assets/prod/tagline/web/main.json) (used for web applications like openfoodfacts-explorer and openfoodfacts-server). Additionally, it explains how to test these updates in the app's development mode before merging changes.
### 1. Understand the Structure of the File
The `main.json` file contains sections for:
- Campaigns: Messages related to donation, call to translations, or updates (new features, news…).
- Translations: Localized content for various languages.
- Tagline Feed: Specifies which campaigns/messages are shown in the app.
### 2. Decide on the Update
Determine the type of change:
- Add a new campaign: Add a new section under the news key.
- Modify an existing campaign: Update fields like `title`, `message`, `button_label`, `url`, etc.
- Add or update translations: Ensure translations are included for all supported languages.
- Update the tagline feed: Add new campaign IDs to the `tagline_feed` to make them visible in the app.
### 3. Edit the main.json File
- Open the file at [`prod/tagline/android/main.json`](https://github.com/openfoodfacts/smooth-app_assets/prod/tagline/android/main.json).
- Add a New Campaign (Example):

```json
"new_campaign_id": {
    "start_date": "2025-05-01 00:00:00",
    "end_date": "2025-06-01 23:59:59",
    "url": "https://example-campaign-url",
    "translations": {
        "default": {
            "title": "Test New Feature!",
            "message": "Try out our **new feature** and give us feedback!",
            "button_label": "Learn More",
            "url": "https://example-feedback-url",
            "image": {
                "url": "https://example.com/image.svg",
                "width": 0.2,
                "alt": "New Feature Image"
            }
        },
        "fr": {
            "title": "Testez la nouvelle fonctionnalité !",
            "message": "Essayez notre **nouvelle fonctionnalité** et donnez-nous votre avis !",
            "button_label": "En savoir plus",
            "url": "https://example-feedback-url-fr"
        }
        // Add other translations as needed
    }
}
- Update the Tagline Feed: Add the new campaign ID to the tagline_feed section:
JSON
"tagline_feed": {
    "default": {
        "news": [
            {
                "id": "existing_campaign_id"
            },
            {
                "id": "new_campaign_id"
            }
        ]
    }
}
```
### 4. Edit the Equivalent iOS and Web Files
- Repeat the changes in the [`prod/tagline/ios/main.json`](https://github.com/openfoodfacts/smooth-app_assets/prod/tagline/ios/main.json) file for the iOS app to keep the behavior consistent across platforms.
- Also repeat the changes in the [`prod/tagline/web/main.json`](https://github.com/openfoodfacts/smooth-app_assets/prod/tagline/web/main.json) file for web applications (openfoodfacts-explorer and openfoodfacts-server) to maintain consistency across all platforms.

### 5. Validate the JSON
- Use a JSON validator (e.g., [jsonlint.com](https://jsonlint.com)) to ensure there are no syntax errors. Note that we will soon have automated JSON linting built into this repository.

### 6. Test Changes in the App's Development Mode
- The Open Food Facts app has a development mode that allows testers to override the tagline URL to point to a custom JSON file. This feature is useful for testing updates before they are merged.

### Steps to Test
- Upload your updated `main.json` file to a URL accessible from the internet (Simplest option: push it to your development branch on GitHub).
- Ensure the hosted JSON URL is accessible
#### Enable Development Mode
- Open the app in development mode.
- Navigate to the settings or debug menu (ask the app maintainers if you’re unsure how to enable dev mode).
#### Override the Tagline URL
- In the app, find the option to override the tagline URL.
- Enter the URL of your hosted JSON file.
#### Test the Changes
- Verify that the new or updated campaigns display correctly in the app.
- Test translations, images, and links to ensure they work as expected.
### 7. Commit and Push Changes
- Create a new branch for your changes and push changes

### 8. Merge and Deploy
- Once approved, merge the changes into the main branch. They will be instantly visible by app users.

### Tips for Newcomers
- Use the app's dev mode to test changes thoroughly before merging.
- Collaborate with translators for any new content.
- If you encounter issues, ask [smooth-app](https://github.com/openfoodfacts/smooth-app) maintainers for guidance.
