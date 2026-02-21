from playwright.sync_api import Page


class SauceDemoInventoryPage:

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        self.page = page

        # Header
        self.shopping_cart_link = page.locator('data-test="shopping-cart-link"')

        # Burger menu
        self.open_menu_button = page.locator("#react-burger-menu-btn")
        self.close_menu_button = page.locator("#react-burger-cross-btn")
        self.logout_sidebar_link = page.locator('[data-test="logout-sidebar-link"]')
        self.reset_sidebar_link = page.locator('[data-test="reset-sidebar-link"]')
        self.about_sidebar_link = page.locator('[data-test="about-sidebar-link"]')
        self.all_items_sidebar_link = page.locator('[data-test="inventory-sidebar-link"]')

        # Sort dropdown
        self.product_sort_container = page.locator('[data-test="product-sort-container"]')
        self.active_option = page.locator('[data-test="active-option"]')

        # Inventory
        self.inventory_container = page.locator('[data-test="inventory-container"]')
        self.inventory_items = page.locator('[data-test="inventory-item"]')
        self.inventory_item_names = page.locator('[data-test="inventory-item-name"]')
        self.inventory_item_prices = page.locator('[data-test="inventory-item-price"]')

        # Add to cart buttons (ejemplos específicos)
        self.add_backpack_button = page.locator("#add-to-cart-sauce-labs-backpack")
        self.add_bike_light_button = page.locator("#add-to-cart-sauce-labs-bike-light")
        self.add_bolt_tshirt_button = page.locator("#add-to-cart-sauce-labs-bolt-t-shirt")
        self.add_fleece_jacket_button = page.locator("#add-to-cart-sauce-labs-fleece-jacket")
        self.add_onesie_button = page.locator("#add-to-cart-sauce-labs-onesie")
        self.add_red_tshirt_button = page.locator("#add-to-cart-test.allthethings()-t-shirt-(red)")

    def load(self) -> None:
        self.page.goto(self.URL)

    def open_menu(self) -> None:
        self.open_menu_button.click()

    def close_menu(self) -> None:
        self.close_menu_button.click()

    def logout(self) -> None:
        self.open_menu()
        self.logout_sidebar_link.click()

    def sort_by(self, value: str) -> None:
        """
        Values:
        - 'az'
        - 'za'
        - 'lohi'
        - 'hilo'
        """
        self.product_sort_container.select_option(value)

    def add_product_to_cart_by_name(self, product_name: str) -> None:
        self.page.locator(
            '[data-test="inventory-item"]',
            has=self.page.locator('[data-test="inventory-item-name"]', has_text=product_name)
        ).locator("button").click()

    def get_inventory_count(self) -> int:
        return self.inventory_items.count()

    def get_product_names(self) -> list:
        return self.inventory_item_names.all_text_contents()

    def get_product_prices(self) -> list:
        return self.inventory_item_prices.all_text_contents()