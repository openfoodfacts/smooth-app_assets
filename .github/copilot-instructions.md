# Open Food Facts Mobile App Assets

**Always reference these instructions first and only fallback to search or bash commands when you encounter unexpected information that does not match the info here.**

This repository contains static assets for the Open Food Facts mobile application, including JSON configuration files for in-app announcements/taglines and associated image assets. The repository serves both Android and iOS versions of the mobile app.

## Working Effectively

### Repository Setup and Validation
- Install Node.js (any version 14+ works, current system has 20.19.4)
- Install JSON validator: `npm install -g jsonlint` -- takes ~0.5 seconds, shows deprecation warning (normal)
- Validate Android JSON: `jsonlint 'prod/tagline/android/main.json'` -- takes ~0.13 seconds
- Validate iOS JSON: `jsonlint 'prod/tagline/ios/main.json'` -- takes ~0.13 seconds
- **Complete validation workflow**: `jsonlint 'prod/tagline/android/main.json' && jsonlint 'prod/tagline/ios/main.json'` -- takes ~0.25 seconds total

### Key Repository Structure
```
prod/tagline/
├── README.md                    # Detailed update instructions
├── android/
│   ├── main.json               # Android app tagline configuration
│   └── assets/                 # Android image assets (SVG files)
│       ├── donation_campaign/
│       ├── off/
│       ├── openprices_campaign/
│       └── translation_campaign_2025/
├── ios/
│   ├── main.json               # iOS app tagline configuration  
│   └── assets/                 # iOS image assets (SVG files)
│       ├── donation_campaign/
│       ├── off/
│       ├── openprices_campaign/
│       └── translation_campaign_2025/
```

### Making Changes to Taglines/Announcements
1. **Always edit both platform files**: 
   - `prod/tagline/android/main.json`
   - `prod/tagline/ios/main.json`
2. **Always validate JSON syntax**: `jsonlint 'prod/tagline/android/main.json' && jsonlint 'prod/tagline/ios/main.json'`
3. **Always maintain consistency** between Android and iOS versions
4. **Always validate before committing**: JSON syntax errors will break the mobile app

### JSON File Structure
Each main.json contains:
- `news`: Campaign definitions with translations, dates, URLs, and images
- `tagline_feed`: Specifies which campaigns are shown in the app

Example campaign structure:
```json
"campaign_id": {
  "start_date": "2025-01-01 00:00:00",
  "end_date": "2025-12-31 23:59:59", 
  "url": "https://example.com",
  "translations": {
    "default": {
      "title": "Campaign Title",
      "message": "Campaign message with **markdown** support",
      "button_label": "Learn More",
      "image": {
        "url": "https://example.com/image.svg",
        "width": 0.2,
        "alt": "Image description"
      }
    },
    "fr": { "title": "Titre français", ... }
  }
}
```

## Validation

### JSON Validation (Required Before All Commits)
- Run: `jsonlint 'prod/tagline/android/main.json'`
- Run: `jsonlint 'prod/tagline/ios/main.json'`
- **Both commands must succeed** - any JSON syntax error breaks the mobile app
- Validation is very fast (~0.13 seconds per file)
- CI workflow automatically validates JSON files on push
- **Expected warning**: `npm warn deprecated nomnom@1.8.1` during jsonlint installation - this is normal and can be ignored

### Testing Changes in Mobile App
- **Cannot run the mobile app directly** - this repository only contains assets
- **Testing requires the Open Food Facts mobile app** in development mode:
  1. Push changes to a branch on GitHub to make JSON accessible via URL
  2. Enable development mode in the Open Food Facts mobile app
  3. Override the tagline URL to point to your branch's JSON file
  4. Verify campaigns display correctly with proper translations and images

### Image Asset Validation
- Images are stored in platform-specific `assets/` directories
- **External image URLs may not be accessible** during development (this is normal)
- SVG format is preferred for scalability
- Always include `alt` text for accessibility
- Use relative width values (e.g., 0.2 = 20% of container width)

## Common Tasks

### Adding a New Campaign
1. Add campaign definition to both `android/main.json` and `ios/main.json`
2. Add corresponding image assets to both `android/assets/` and `ios/assets/`  
3. Include the campaign ID in the `tagline_feed` section
4. Provide translations for all supported languages (minimum: default, fr)
5. Validate JSON syntax: `jsonlint 'prod/tagline/android/main.json' && jsonlint 'prod/tagline/ios/main.json'`

### Updating Existing Campaign
1. Modify the same campaign in both platform JSON files
2. Update associated assets if needed
3. Maintain consistency between Android and iOS versions
4. Always validate: `jsonlint 'prod/tagline/android/main.json' && jsonlint 'prod/tagline/ios/main.json'`

### Repository Information from Common Commands

#### Repository Root Contents
```bash
$ ls -la
.git/
.github/
README.md
prod/
```

#### Main JSON Files Are Large
- `prod/tagline/android/main.json` - 586 lines with multiple campaigns and translations
- `prod/tagline/ios/main.json` - 586 lines, identical content structure to Android

#### Available Asset Folders
```bash
$ ls prod/tagline/android/assets/ && echo "---iOS---" && ls prod/tagline/ios/assets/
donation_campaign  off  openprices_campaign  translation_campaign_2025
---iOS---
donation_campaign  off  openprices_campaign  translation_campaign_2025
```

#### Node.js and npm Information
```bash
$ node --version && npm --version
v20.19.4
10.8.2
```

#### Sample JSON Validation Output
```bash
$ jsonlint 'prod/tagline/android/main.json' > /dev/null && echo "Android JSON valid"
Android JSON valid

$ jsonlint 'prod/tagline/ios/main.json' > /dev/null && echo "iOS JSON valid"  
iOS JSON valid
```

## Key Constraints and Important Notes

### No Build Process
- **This repository does not build or compile anything**
- **No complex dependencies** - only requires Node.js and jsonlint
- **No test suite** beyond JSON syntax validation
- **No runtime application** - only static asset files

### Platform Synchronization Critical  
- **Always update both Android and iOS files** when making changes
- **Inconsistencies between platforms** will cause different behavior in Android vs iOS apps
- **Asset folder structures must match** between platforms

### External Dependencies
- **Image URLs may not be accessible** from development environment (firewall/network restrictions)
- **This is normal and expected** - images are served from production CDN
- **Focus on JSON structure validation** rather than image accessibility

### CI/CD Integration
- **GitHub Actions automatically validates** JSON files on push/PR
- **Uses Node.js 14** in CI (but any 14+ version works locally)
- **Workflow file**: `.github/workflows/lint-json.yml`
- **Must pass validation** before merge is allowed

### Performance Expectations
- **JSON validation**: ~0.13 seconds per file, ~0.25 seconds for both files
- **Installation time**: ~0.5 seconds for jsonlint (shows deprecation warning - this is normal)
- **No long-running operations** in this repository
- **No timeout concerns** - all operations complete in under 1 second

## Emergency Troubleshooting

### JSON Validation Fails
- Check for missing commas, brackets, or quotes
- Use online JSON validator like jsonlint.com for detailed error location
- Compare with working JSON structure from existing campaigns

### Changes Not Appearing in App
- Verify the campaign is included in `tagline_feed` section
- Check date ranges (start_date/end_date) are current
- Ensure both Android and iOS JSON files are updated
- Confirm the mobile app is pointing to the correct JSON URL

### Asset Images Not Loading
- **Expected during development** due to network restrictions
- **Will work in production** once merged to main branch
- Focus on JSON structure rather than image accessibility during development