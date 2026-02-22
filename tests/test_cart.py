from pathlib import Path
import json
import pytest

from playwright.sync_api import Page, expect
from pages.login import SauceDemoLoginPage
from pages.inventory import SauceDemoInventoryPage
from pages.cart import SauceDemoCartPage
from pages.checkout_step_one import SauceDemoCheckoutStepOnePage

auth_path = (Path(__file__).parent.parent / 'test_data' / 'auth.json').resolve()
with auth_path.open('r', encoding='utf-8') as f:
    auth_data = json.load(f)


usernames_ok = auth_data['usernames_ok']

@pytest.fixture(scope='function', autouse=True)
def inventory_module_setup(
        username: str,
        page: Page,
        login_page: SauceDemoLoginPage,
        inventory_page: SauceDemoInventoryPage):

    login_page.load()
    login_page.login(username=username, password=auth_data['password'])
    expect(page).to_have_url(inventory_page.URL, timeout=1500)
    expect(inventory_page.inventory_container).to_be_visible()

    return inventory_page

@pytest.mark.parametrize("username", usernames_ok)
def test_navigate_cart(inventory_page: SauceDemoInventoryPage, cart_page: SauceDemoCartPage):
    inventory_page.go_to_cart()
    assert cart_page.page_title.is_visible()
    assert cart_page.get_title_name() == cart_page.TITLE
    cart_page.continue_shopping()
    expect(inventory_page.inventory_container).to_be_visible()

@pytest.mark.parametrize("username", usernames_ok)
def test_add_remove_items(inventory_page: SauceDemoInventoryPage, cart_page: SauceDemoCartPage):

    product_names = inventory_page.get_product_names()

    inventory_page.click_product_to_cart_by_name(product_names[0])
    inventory_page.click_product_to_cart_by_name(product_names[1])
    inventory_page.click_product_to_cart_by_name(product_names[5])

    inventory_page.go_to_cart()
    assert cart_page.page_title.is_visible()
    assert cart_page.get_title_name() == cart_page.TITLE

    #check all products are in cart
    assert cart_page.get_cart_count() == 3
    products_in_cart = cart_page.get_product_names()
    assert product_names[0] in products_in_cart
    assert product_names[1] in products_in_cart
    assert product_names[5] in products_in_cart

    #remove specific product
    cart_page.remove_product_by_name(product_names[5])
    products_in_cart = cart_page.get_product_names()
    assert product_names[5] not in products_in_cart

@pytest.mark.parametrize("username", usernames_ok)
def test_remove_all_items(inventory_page: SauceDemoInventoryPage, cart_page: SauceDemoCartPage):

    product_names = inventory_page.get_product_names()

    inventory_page.click_product_to_cart_by_name(product_names[0])
    inventory_page.click_product_to_cart_by_name(product_names[1])
    inventory_page.click_product_to_cart_by_name(product_names[5])

    inventory_page.go_to_cart()
    assert cart_page.page_title.is_visible()
    assert cart_page.get_title_name() == cart_page.TITLE

    #check all products are in cart
    assert cart_page.get_cart_count() == 3
    products_in_cart = cart_page.get_product_names()
    assert product_names[0] in products_in_cart
    assert product_names[1] in products_in_cart
    assert product_names[5] in products_in_cart

    #remove all items
    cart_page.remove_product_by_name(product_names[0])
    cart_page.remove_product_by_name(product_names[1])
    cart_page.remove_product_by_name(product_names[5])
    products_in_cart = cart_page.get_product_names()
    assert not products_in_cart

@pytest.mark.parametrize("username", usernames_ok)
def test_saved_progress_continue_shopping(inventory_page: SauceDemoInventoryPage, cart_page: SauceDemoCartPage):

    product_names = inventory_page.get_product_names()

    inventory_page.click_product_to_cart_by_name(product_names[0])
    inventory_page.click_product_to_cart_by_name(product_names[1])
    inventory_page.click_product_to_cart_by_name(product_names[5])

    inventory_page.go_to_cart()
    assert cart_page.page_title.is_visible()
    assert cart_page.get_title_name() == cart_page.TITLE

    #check all products are in cart
    assert cart_page.get_cart_count() == 3
    products_in_cart = cart_page.get_product_names()
    assert product_names[0] in products_in_cart
    assert product_names[1] in products_in_cart
    assert product_names[5] in products_in_cart

    #remove specific product
    cart_page.remove_product_by_name(product_names[5])
    products_in_cart = cart_page.get_product_names()
    assert product_names[5] not in products_in_cart

    cart_page.continue_shopping()
    expect(inventory_page.inventory_container).to_be_visible()

    #check added items are still added in inventory page (no progress was lost)
    assert inventory_page.is_remove_button_visible(product_names[0]) is True
    assert inventory_page.is_remove_button_visible(product_names[1]) is True
    assert inventory_page.is_remove_button_visible(product_names[5]) is False

@pytest.mark.parametrize("username", usernames_ok)
def test_continue_to_checkout(
        inventory_page: SauceDemoInventoryPage,
        cart_page: SauceDemoCartPage,
        checkout_step_one_page: SauceDemoCheckoutStepOnePage):

    product_names = inventory_page.get_product_names()

    inventory_page.click_product_to_cart_by_name(product_names[0])
    inventory_page.click_product_to_cart_by_name(product_names[1])
    inventory_page.click_product_to_cart_by_name(product_names[5])

    inventory_page.go_to_cart()
    assert cart_page.page_title.is_visible()
    assert cart_page.get_title_name() == cart_page.TITLE

    #check all products are in cart
    assert cart_page.get_cart_count() == 3
    products_in_cart = cart_page.get_product_names()
    assert product_names[0] in products_in_cart
    assert product_names[1] in products_in_cart
    assert product_names[5] in products_in_cart


    cart_page.proceed_to_checkout()
    assert checkout_step_one_page.page_title.is_visible()
    assert checkout_step_one_page.get_title_name() == checkout_step_one_page.TITLE


