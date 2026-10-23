import os
import traceback
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from config.settings import TARGET_SITE, BROWSER, HEADLESS, BASE_URL, PAGE_LOAD_TIMEOUT_SECONDS
from utilities.logger import get_logger
from utilities.screenshot_manager import save_screenshot

logger = get_logger("shopsphere")


def pytest_configure(config):
    config.option.htmlpath = str(Path(__file__).parent / "reports" / "report.html") if not getattr(config.option, "htmlpath", None) else config.option.htmlpath


def _browser_options(browser_name: str):
    if browser_name == "edge":
        options = EdgeOptions()
    else:
        options = ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return options


@pytest.fixture(scope="session")
def selected_site():
    return {"name": TARGET_SITE, "base_url": BASE_URL}


@pytest.fixture(scope="session")
def browser_name():
    return BROWSER


@pytest.fixture
def driver(browser_name, request):
    options = _browser_options(browser_name)
    if browser_name == "edge":
        browser = webdriver.Edge(options=options)
    else:
        browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(PAGE_LOAD_TIMEOUT_SECONDS)
    browser.execute_cdp_cmd("Page.setDownloadBehavior", {"behavior": "deny", "downloadPath": ""})
    browser.implicitly_wait(5)
    request.node._shopsphere_driver = browser
    yield browser
    browser.quit()


@pytest.fixture(autouse=True)
def failure_evidence(request, driver):
    yield
    report = request.node.report_call if hasattr(request.node, "report_call") else None
    if report and report.failed:
        path = save_screenshot(driver, request.node.name, TARGET_SITE, BROWSER)
        logger.error(
            "FAILED %s | site=%s browser=%s url=%s screenshot=%s",
            request.node.nodeid, TARGET_SITE, BROWSER, driver.current_url, path,
        )
        logger.error(traceback.format_exc())


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if call.when == "call":
        setattr(item, "report_call", report)
