# Local-currency donation offers

Proposal for [issue #82](https://github.com/openfoodfacts/smooth-app_assets/issues/82).
No feed or client behavior is changed by this document.

## Recommended scope

Offer suggested donations in supported local currencies while keeping campaign
`raised`, `goal`, and `currency` in their actual source currency, currently EUR.
Suggested donations are independently chosen price points, not converted campaign
figures. This approach needs no exchange-rate service.

Issue #82 does not yet distinguish suggested donations from converted fundraising
totals. Maintainers should confirm this scope before implementation.

## Existing behavior and checkout findings

- The daily updater owns the canonical campaign figures in the Android, iOS, and
  web feeds. Mobile and web meters format those amounts in the published currency.
- The app's `DonationOffer` also reads that currency for its donation tiers. The
  web banner similarly uses its funding currency for the `amounts` attribute.
  Changing the campaign currency to localize tiers would therefore relabel the
  fundraising totals. Adding an unread optional field alone would change no UI.
- Mobile already has `UserPreferences.userCurrencyCode`, initialized from the
  configured country when possible. Web has separate country and language signals;
  language selects copy, not a donation currency.
- On 22 October 2026 the live Donorbox form exposed 49 currency choices. Requests
  with USD 5, INR 199, and JPY 500 selected the requested currency, amount, and monthly
  interval. An unknown code fell back to EUR. These were form inspections, not
  completed payments.
- The live website's V2 donation-page script reads amount and interval parameters,
  then chooses USD for its Americas list and EUR elsewhere. It does not read the
  requested currency. The V1/V2 experiment must be checked before promising that a
  local-currency web banner will reach a matching checkout.

## Minimum implementation

1. **Assets:** publish a small, maintainer-approved set of donation offers in one
   optional block separate from campaign funding. Key offers by ISO 4217 currency
   code and validate each tier against that currency's precision and the campaign's
   checkout minimum. Preserve existing fields, URLs, tracking, and translations.
   Publish the new data only with a verified consumer; do not duplicate the campaign
   or scrape converted campaign totals. The daily figures updater remains unchanged.
2. **Mobile:** read and validate the optional offers in the existing news model and
   `DonationOffer`. Use the existing currency preference when a valid offer exists.
   Otherwise retain the existing EUR offer. Treat an offer's currency and amounts as
   one unit: never combine a local currency with fallback EUR amounts. Keep the meter
   in EUR, and pass the selected currency, amount, and interval to the existing
   Donorbox destination without dropping tracking parameters.
3. **Web, if included in the first release:** consume the same offers in the banner
   with a host-provided currency choice. Keep the meter in its funding currency.
   The website checkout bridge also needs to honor and validate that choice in both
   experiment variants rather than overwrite it. Preserve localized donation URLs
   and tracking; do not silently switch donation providers or bypass the website.

Old clients continue using the current EUR fields and ignore the optional block.
Missing, invalid, or unsupported offers fall back to the current EUR experience.
Use `intl` / `Intl.NumberFormat` for symbols, separators, and currency precision;
do not infer currency from language or hand-code symbol positions.

The app's scans-per-unit estimate is calibrated to EUR. Local tiers must not reuse
that estimate unchanged: omit the claim unless maintainers supply a justified local
anchor. The same applies to fixed EUR amounts embedded in web banner copy.

## Decisions needed

- Confirm suggested donations, with campaign totals remaining EUR, as the scope.
- Choose the first consumers: mobile plus assets is the smaller initial slice;
  web also depends on the website checkout bridge.
- Approve the initial currencies and donation tiers. The table attached in
  [smooth-app #7675](https://github.com/openfoodfacts/smooth-app/pull/7675) is useful
  input, not an approved checkout contract: its VND profile is absent from the
  form's currency menu. The exposed minimum-amount table also changes with the
  form's initial currency. Validate the intended entry path rather than treating
  the EUR form's converted minimums as universal limits or putting them into code.
- Confirm currency-based offers initially, or specify a rule for different tiers
  within the same currency. Do not silently adopt the draft's global USD fallback;
  retaining the current EUR fallback preserves existing behavior.

## Acceptance checks

- Current EUR behavior and campaign percentages stay unchanged in every consumer.
- Supported offers reach checkout with the same currency, amount, and interval;
  verify both website experiment variants if web is included.
- Unknown country, missing currency, invalid offers, and unsupported currencies
  safely retain EUR. Explicit currency preference takes precedence over country.
- JPY uses zero fractional digits; currencies allowing fractional donations retain
  their permitted precision. Formatting follows the viewer's locale.
- Old clients still parse the feed; new clients without offer data keep working.
- URLs and tracking parameters survive the handoff. Non-EUR offers do not show an
  unadjusted EUR impact estimate or a contradictory fixed-EUR donation amount.
- Updater tests, feed schema validation, and JSON lint pass for all three platforms.
  Add preservation/validation tests for the new block and focused consumer tests
  when the approved implementation is made.

## References

- [Assets #73](https://github.com/openfoodfacts/smooth-app_assets/pull/73) and
  [#78](https://github.com/openfoodfacts/smooth-app_assets/pull/78): canonical figures,
  daily updates, and backward compatibility.
- [Mobile #7675](https://github.com/openfoodfacts/smooth-app/pull/7675): remote offers,
  non-Euro users, and the draft country tiers.
- [Web #616](https://github.com/openfoodfacts/openfoodfacts-webcomponents/pull/616)
  and [#630](https://github.com/openfoodfacts/openfoodfacts-webcomponents/issues/630):
  funding meter, banner variants, and checkout links.
- [Live donation page](https://world.openfoodfacts.org/donate-to-open-food-facts) and
  [Donorbox form](https://donorbox.org/embed/help-open-food-facts-stay-afloat).
