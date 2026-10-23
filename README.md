# ShopSphere Selenium Automation

ShopSphere is a Selenium WebDriver 4 + pytest project for one selected practice storefront at a time. The default target is Automation Exercise. SauceDemo and DemoBlaze are implemented behind the same configuration and factory, and running one target does not require the other two sites.

## Requirements

- Windows 10/11
- Python 3.11 or newer
- Google Chrome or Microsoft Edge
- Internet access for the selected practice site

## Setup

```powershell
cd C:\Users\Giris\Documents\ShopSphere
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Select a website

Set `TARGET_SITE` in `config/settings.py` or use an environment variable:

```python
TARGET_SITE = "automation_exercise"
```

Supported values are `saucedemo`, `automation_exercise`, and `demoblaze`. Automation Exercise is the default. Base URLs are derived from the selection.

```powershell
$env:SHOPSPHERE_SITE="saucedemo"
$env:SHOPSPHERE_BROWSER="edge"
$env:SHOPSPHERE_HEADLESS="true"
```

## Run

```powershell
.\run_tests.ps1
.\run_tests.ps1 -Browser edge -Headless
```

Direct pytest equivalent:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -v --html=reports\report.html --self-contained-html
.\.venv\Scripts\python.exe -m unittest tests/test_unittest_comparison.py
```

Batch launcher:

```bat
run_tests.bat
```

## Architecture

- `config/settings.py`: selected site, URL, browser, wait, and page-load settings.
- `conftest.py`: browser fixtures, Selenium Manager setup, teardown, and failure evidence.
- `pages/base_page.py`: explicit waits and reusable interactions.
- `pages/*_pages.py`: site-specific locators and workflows.
- `pages/site_factory.py`: returns only the page object for the selected site.
- `tests/`: pytest scenarios and one unittest comparison.
- `data/`: JSON and CSV test data.
- `utilities/`: logging, screenshots, and data readers.

Selectors live in page objects. Tests contain workflow assertions. Selenium Manager resolves compatible browser drivers.

## Scenario Traceability

| ID | Scenario | Default implementation | Expected result | Status |
|---|---|---|---|---|
| TC01 | Search products | `test_tc01_search_products` | Search reveals matching product and price | Executed |
| TC02 | Add to cart | `test_tc02_add_to_cart` | Item appears in cart | Executed |
| TC03 | Change quantity | `test_tc03_change_quantity` | Quantity and total update | Executed for Automation Exercise; unsupported on SauceDemo and DemoBlaze |
| TC04 | Remove final item | `test_tc04_remove_last_item` | Empty cart is shown | Executed |
| TC05 | Incomplete checkout | `test_tc05_incomplete_checkout` | Validation shown; order not completed | Executed |
| TC06 | Successful checkout | `test_tc06_successful_checkout` | Confirmation is displayed | Executed |
| TC07 | Invalid coupon | `test_tc07_coupon_limitation` | N/A | Unsupported by all three selected public implementations |
| TC08 | New tab | `test_tc08_new_tab_navigation` | New tab becomes active; original tab restored | Executed |

## Reports and Evidence

- HTML report: `reports/report.html`
- Failure screenshots: `screenshots/`
- Execution log: `logs/shopsphere.log`
- Site availability or third-party ad instability should be treated as environmental failure, not silently converted to pass.

## Known Limitations

- SauceDemo has login, inventory, sorting, cart, and checkout, but no search, editable quantities, or coupon field.
- Automation Exercise has search, quantity, cart, and checkout, but no coupon field.
- DemoBlaze has categories, product details, alerts, cart, and purchase modal, but no conventional quantity or coupon controls.
- Automation Exercise advert overlays may interrupt click coordinates; the shared click helper falls back to JavaScript clicking only after normal Selenium interception.

## Faculty Demonstration

1. Open `config/settings.py` and show the one-line `TARGET_SITE` selection.
2. Run `run_tests.ps1` from PowerShell.
3. Show the passing/skipped pytest summary and traceability table.
4. Open `reports/report.html`.
5. Open a failed-test screenshot only if intentionally demonstrating evidence capture.
6. Switch to `saucedemo` or `demoblaze`, run the launcher, and show that only that site is addressed.
7. Run the unittest class and explain its lifecycle methods and assertion.
