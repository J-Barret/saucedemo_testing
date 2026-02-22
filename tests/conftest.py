import pytest

from pages.login import SauceDemoLoginPage
from pages.inventory import SauceDemoInventoryPage
from pages.item_detail import SauceDemoItemDetailPage
from playwright.sync_api import Page

@pytest.fixture
def login_page(page: Page) -> SauceDemoLoginPage:
    return SauceDemoLoginPage(page)

@pytest.fixture
def inventory_page(page: Page) -> SauceDemoInventoryPage:
    return SauceDemoInventoryPage(page)

@pytest.fixture
def item_detail_page(page: Page) -> SauceDemoItemDetailPage:
    return SauceDemoItemDetailPage(page)