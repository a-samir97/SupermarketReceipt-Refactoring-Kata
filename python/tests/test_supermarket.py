import pytest
from model_objects import Product
from model_objects import ProductUnit
from model_objects import SpecialOfferType
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


def test_ten_percent_discount():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)
    cart.add_item(toothbrush)

    receipt = teller.checks_out_articles_from(cart)

    assert 4.975 + 0.891 == pytest.approx(receipt.total_price(), 0.01)
    assert len(receipt.discounts) == 1
    assert 2 == len(receipt.items)
    # first item
    receipt_item = receipt.items[0]
    assert apples == receipt_item.product
    assert 1.99 == receipt_item.price
    assert 2.5 * 1.99 == pytest.approx(receipt_item.total_price, 0.01)
    assert 2.5 == receipt_item.quantity
    # second item
    receipt_item = receipt.items[1]
    assert toothbrush == receipt_item.product
    assert 0.99 == receipt_item.price
    assert 1 == receipt_item.quantity


def test_two_for_amount_discount():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, toothbrush, 1.5)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)

    receipt = teller.checks_out_articles_from(cart)

    assert 1.5 + 0.99 == pytest.approx(receipt.total_price())
    assert len(receipt.discounts) == 1
    assert 1 == len(receipt.items)
    receipt_item = receipt.items[0]
    assert toothbrush == receipt_item.product
    assert 0.99 == receipt_item.price
    assert 3 == receipt_item.quantity


def test_five_for_amount_discount():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, 2.5)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 7)

    receipt = teller.checks_out_articles_from(cart)

    assert 2.5 + 0.99 + 0.99 == pytest.approx(receipt.total_price())
    assert len(receipt.discounts) == 1
    assert 1 == len(receipt.items)
    receipt_item = receipt.items[0]
    assert toothbrush == receipt_item.product
    assert 0.99 == receipt_item.price
    assert 7 == receipt_item.quantity


def test_three_for_two_discount():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 7)

    receipt = teller.checks_out_articles_from(cart)

    assert 1.98 + 1.98 + 0.99 == pytest.approx(receipt.total_price())
    assert len(receipt.discounts) == 1
    assert 1 == len(receipt.items)
    receipt_item = receipt.items[0]
    assert toothbrush == receipt_item.product
    assert 0.99 == receipt_item.price
    assert 7 == receipt_item.quantity
