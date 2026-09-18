/**
 * Open Food Facts - Photos for Impact Campaign
 * Google Apps Script: Split Master Sheet into 32 Country Tabs + Leaderboard Dashboard
 * 
 * Instructions:
 * 1. Open your Google Spreadsheet: https://docs.google.com/spreadsheets/d/1LiO3IFgGZ2ftYpXLrFh8LpgBaTKBKeggz3jLwv8dxB8/edit
 * 2. Click Extensions > Apps Script
 * 3. Delete any code in the editor and paste this entire script.
 * 4. Click 'Run' (function: createPhotosForImpactTabs).
 * 5. Grant permissions when prompted. The script will reorganize the data within ~30-60 seconds!
 */

function createPhotosForImpactTabs() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheets()[0]; // Master sheet
  
  // Make sure we have the source data
  var data = sheet.getDataRange().getValues();
  if (data.length < 2) {
    SpreadsheetApp.getUi().alert('Master sheet does not contain enough data.');
    return;
  }
  
  var headers = data[0];
  var catIdx = headers.indexOf('Category');
  var countryIdx = headers.indexOf('Country');
  var offCountryIdx = headers.indexOf('off_country_id');
  var codeIdx = headers.indexOf('code');
  var recipeIdx = headers.indexOf('Is_needed_a_recipe ? Mano');
  
  if (catIdx === -1 || countryIdx === -1) {
    SpreadsheetApp.getUi().alert('Columns "Category" or "Country" not found in master sheet.');
    return;
  }

  // Country Metadata: Code, Flag, Languages
  var countryMeta = {
    'Austria': { flag: '🇦🇹', code: 'AT' },
    'Belgium': { flag: '🇧🇪', code: 'BE' },
    'Bulgaria': { flag: '🇧🇬', code: 'BG' },
    'Croatia': { flag: '🇭🇷', code: 'HR' },
    'Cyprus': { flag: '🇨🇾', code: 'CY' },
    'Czech Republic': { flag: '🇨🇿', code: 'CZ' },
    'Denmark': { flag: '🇩🇰', code: 'DK' },
    'Estonia': { flag: '🇪🇪', code: 'EE' },
    'Finland': { flag: '🇫🇮', code: 'FI' },
    'France': { flag: '🇫🇷', code: 'FR' },
    'Germany': { flag: '🇩🇪', code: 'DE' },
    'Greece': { flag: '🇬🇷', code: 'GR' },
    'Hungary': { flag: '🇭🇺', code: 'HU' },
    'Ireland': { flag: '🇮🇪', code: 'IE' },
    'Italy': { flag: '🇮🇹', code: 'IT' },
    'Latvia': { flag: '🇱🇻', code: 'LV' },
    'Lithuania': { flag: '🇱🇹', code: 'LT' },
    'Luxembourg': { flag: '🇱🇺', code: 'LU' },
    'Malta': { flag: '🇲🇹', code: 'MT' },
    'Montenegro': { flag: '🇲🇪', code: 'ME' },
    'Netherlands': { flag: '🇳🇱', code: 'NL' },
    'Norway': { flag: '🇳🇴', code: 'NO' },
    'Poland': { flag: '🇵🇱', code: 'PL' },
    'Portugal': { flag: '🇵🇹', code: 'PT' },
    'Romania': { flag: '🇷🇴', code: 'RO' },
    'Serbia': { flag: '🇷🇸', code: 'RS' },
    'Slovakia': { flag: '🇸🇰', code: 'SK' },
    'Slovenia': { flag: '🇸🇮', code: 'SI' },
    'Spain': { flag: '🇪🇸', code: 'ES' },
    'Sweden': { flag: '🇸🇪', code: 'SE' },
    'Switzerland': { flag: '🇨🇭', code: 'CH' },
    'United Kingdom': { flag: '🇬🇧', code: 'UK' }
  };

  // Group rows by Country
  var countryRows = {};
  for (var i = 1; i < data.length; i++) {
    var row = data[i];
    var country = (row[countryIdx] || '').toString().trim();
    if (!country) continue;
    if (!countryRows[country]) {
      countryRows[country] = [];
    }
    countryRows[country].append(row);
  }

  // Rename master sheet to _Raw_Master_Data to keep original untouched
  sheet.setName('_Raw_Master_Data');

  // Create Leaderboard Dashboard Tab
  var dashboardName = '📊 Leaderboard & Overview';
  var dashboardSheet = ss.getSheetByName(dashboardName);
  if (!dashboardSheet) {
    dashboardSheet = ss.insertSheet(dashboardName, 0);
  } else {
    dashboardSheet.clear();
  }

  // Format Dashboard Header
  dashboardSheet.getRange('A1:G1').merge()
    .setValue('📸 Photos for Impact — Representative Products Campaign')
    .setBackground('#2D72D2').setFontColor('#FFFFFF').setFontWeight('bold').setFontSize(14).setHorizontalAlignment('center');
  
  dashboardSheet.getRange('A2:G2').merge()
    .setValue('Tracking representative food coverage across 32 countries. Low-DAU countries need your photos to reach 100% coverage!')
    .setBackground('#F0F4F8').setFontColor('#333333').setFontStyle('italic').setHorizontalAlignment('center');

  dashboardSheet.getRange(4, 1, 1, 7).setValues([[
    'Flag', 'Country', 'Total Categories', 'In Database', 'Missing Barcode/Photos', '% Covered', 'Action'
  ]]).setBackground('#347644').setFontColor('#FFFFFF').setFontWeight('bold');

  var dashboardRow = 5;
  var sortedCountries = Object.keys(countryRows).sort();

  for (var c = 0; c < sortedCountries.length; c++) {
    var cName = sortedCountries[c];
    var meta = countryMeta[cName] || { flag: '🌍', code: cName.substring(0, 2).toUpperCase() };
    var tabName = meta.flag + ' ' + cName;
    
    // Create Country Tab
    var cSheet = ss.getSheetByName(tabName);
    if (!cSheet) {
      cSheet = ss.insertSheet(tabName);
    } else {
      cSheet.clear();
    }

    // Top KPI Summary Cards for Country Tab
    cSheet.getRange('A1:B1').merge().setValue(meta.flag + ' ' + cName + ' — Representative Products').setFontWeight('bold').setFontSize(13);
    cSheet.getRange('A2').setValue('Total Categories:').setFontWeight('bold');
    cSheet.getRange('B2').setFormula('=COUNTA(A6:A)');
    
    cSheet.getRange('A3').setValue('In Database:').setFontWeight('bold');
    cSheet.getRange('B3').setFormula('=COUNTIF(C6:C, "✅ In Database")');

    cSheet.getRange('C2').setValue('Missing Barcode / Photo:').setFontWeight('bold');
    cSheet.getRange('D2').setFormula('=COUNTIF(C6:C, "🔍 Needs Barcode") + COUNTIF(C6:C, "📸 Needs Photo")');

    cSheet.getRange('C3').setValue('Coverage %:').setFontWeight('bold');
    cSheet.getRange('D3').setFormula('=IF(B2>0, B3/B2, 0)').setNumberFormat('0.0%');

    // Headers for Country Tab
    cSheet.getRange(5, 1, 1, 8).setValues([[
      'Category Tag', 'Category Name', 'Status', 'Barcode (Code)', 'Open Food Facts', 'Hunger Games Link', 'Recipe?', 'Contributor'
    ]]).setBackground('#2D72D2').setFontColor('#FFFFFF').setFontWeight('bold');

    var rowsForThisCountry = countryRows[cName];
    var outTable = [];

    for (var r = 0; r < rowsForThisCountry.length; r++) {
      var sourceRow = rowsForThisCountry[r];
      var catTag = (sourceRow[catIdx] || '').toString().trim();
      var cleanName = catTag.replace(/^en:/, '').replace(/-/g, ' ');
      cleanName = cleanName.charAt(0).toUpperCase() + cleanName.slice(1);
      var barcode = (sourceRow[codeIdx] || '').toString().trim();
      var offCountry = (sourceRow[offCountryIdx] || ('en:' + cName.toLowerCase())).toString().trim();
      var status = barcode ? '✅ In Database' : '🔍 Needs Barcode';
      var offLink = barcode ? '=HYPERLINK("https://world.openfoodfacts.org/product/' + barcode + '", "View ' + barcode + '")' : 'Missing barcode';
      var hgLink = '=HYPERLINK("https://hunger.openfoodfacts.org/questions?value_tag=' + catTag + '&type=category&country=' + offCountry + '&sorted=true", "Categorize")';
      var recipe = (sourceRow[recipeIdx] || '').toString().trim();

      outTable.push([
        catTag, cleanName, status, barcode, offLink, hgLink, recipe, ''
      ]);
    }

    if (outTable.length > 0) {
      cSheet.getRange(6, 1, outTable.length, 8).setValues(outTable);
      
      // Add Dropdown Validation for Status Column (C)
      var rule = SpreadsheetApp.newDataValidation()
        .requireValueInList(['✅ In Database', '📸 Needs Photo', '🔍 Needs Barcode', '🎉 Completed'], true)
        .build();
      cSheet.getRange(6, 3, outTable.length, 1).setDataValidation(rule);
    }

    cSheet.setFrozenRows(5);
    cSheet.autoResizeColumns(1, 8);

    // Write row to Leaderboard Dashboard
    var cSheetId = cSheet.getSheetId();
    var sheetLink = '=HYPERLINK("#gid=' + cSheetId + '", "Open ' + cName + ' Tab ➔")';
    
    dashboardSheet.getRange(dashboardRow, 1, 1, 7).setValues([[
      meta.flag,
      cName,
      "='" + tabName + "'!B2",
      "='" + tabName + "'!B3",
      "='" + tabName + "'!D2",
      "='" + tabName + "'!D3",
      sheetLink
    ]]);
    dashboardSheet.getRange(dashboardRow, 6).setNumberFormat('0.0%');
    dashboardRow++;
  }

  // Dashboard Total Row
  dashboardSheet.getRange(dashboardRow, 1, 1, 7).setValues([[
    '🇪🇺', 'TOTAL / ALL COUNTRIES',
    '=SUM(C5:C' + (dashboardRow - 1) + ')',
    '=SUM(D5:D' + (dashboardRow - 1) + ')',
    '=SUM(E5:E' + (dashboardRow - 1) + ')',
    '=IF(C' + dashboardRow + '>0, D' + dashboardRow + '/C' + dashboardRow + ', 0)',
    'All 32 Countries'
  ]]).setBackground('#EBF3E8').setFontWeight('bold');
  dashboardSheet.getRange(dashboardRow, 6).setNumberFormat('0.0%');

  dashboardSheet.setFrozenRows(4);
  dashboardSheet.autoResizeColumns(1, 7);

  SpreadsheetApp.getUi().alert('Success! Created Leaderboard Overview and 32 country tabs with live tracking formulas.');
}
