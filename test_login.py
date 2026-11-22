from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"
INVENTORY_URL = BASE_URL + "inventory.html"
CART_URL = BASE_URL + "cart.html"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
PRODUCT = "Sauce Labs Backpack"


def sign_in(page: Page, password: str) -> None:
    page.goto(BASE_URL)
    page.locator('[data-test="username"]').fill(USERNAME)
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()


def add_backpack(page: Page) -> None:
    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")


def test_login_page_is_displayed(page: Page) -> None:
    page.goto(BASE_URL)
    expect(page.locator('[data-test="username"]')).to_be_visible()
    expect(page.locator('[data-test="password"]')).to_be_visible()
    expect(page.locator('[data-test="login-button"]')).to_be_visible()


def test_successful_login(page: Page) -> None:
    sign_in(page, PASSWORD)
    expect(page).to_have_url(INVENTORY_URL)
    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()


def test_add_product_to_cart(page: Page) -> None:
    sign_in(page, PASSWORD)
    add_backpack(page)


def test_product_is_displayed_in_cart(page: Page) -> None:
    sign_in(page, PASSWORD)
    add_backpack(page)
    page.locator('[data-test="shopping-cart-link"]').click()
    expect(page).to_have_url(CART_URL)
    cart = page.locator('[data-test="cart-list"]')
    expect(cart).to_be_visible()
    item = cart.locator('[data-test="inventory-item-name"]')
    expect(item).to_have_count(1)
    expect(item).to_be_visible()
    expect(item).to_have_text(PRODUCT)


def test_login_with_invalid_password(page: Page) -> None:
    sign_in(page, "wrong_password")
    error = page.locator('[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username and password do not match")
    expect(page).to_have_url(BASE_URL)
