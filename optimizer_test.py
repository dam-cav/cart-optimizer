import unittest

from optimizer import (
  optimize_cart,
)

class OptimizerTest(unittest.TestCase):
  def test_when_splitted_order_is_better(self):
    wanted_products = [
      {
        'id': 'A',
        'name': 'CartaA',
        'quantity': 1,
      },
      {
        'id': 'B',
        'name': 'CartaB',
        'quantity': 1,
      },
    ]

    product_sellers = [
      {
        'id': '1',
        'name': 'Venditore1',
        'shipping': 10,
        'catalog': {
          'A': {
            'price': 50,
            'quantity': 1
          },
          'B': {
            'price': 20,
            'quantity': 1
          },
        }
      },
      {
        'id': '2',
        'name': 'Venditore2',
        'shipping': 30,
        'catalog': {
          'A': {
            'price': 19,
            'quantity': 1
          }
        }
      },
    ]

    result = optimize_cart(wanted_products, product_sellers)

    self.assertEqual(result['solvable'], True)
    self.assertEqual(result['total'], 79,)
    self.assertEqual(len(result['sellers']), 2)

  def test_when_unique_order_is_better(self):
    wanted_products = [
      {
        'id': 'A',
        'name': 'CartaA',
        'quantity': 1,
      },
      {
        'id': 'B',
        'name': 'CartaB',
        'quantity': 1,
      },
    ]

    product_sellers = [
      {
        'id': '1',
        'name': 'Venditore1',
        'shipping': 10,
        'catalog': {
          'A': {
            'price': 50,
            'quantity': 1
          },
          'B': {
            'price': 20,
            'quantity': 1
          },
        }
      },
      {
        'id': '2',
        'name': 'Venditore2',
        'shipping': 30,
        'catalog': {
          'A': {
            'price': 21,
            'quantity': 1
          }
        }
      },
    ]

    result = optimize_cart(wanted_products, product_sellers)

    self.assertEqual(result['solvable'], True)
    self.assertEqual(result['total'], 80)
    self.assertEqual(len(result['sellers']), 1)

  def test_need_to_buy_from_all_to_suit_quantity(self):
    wanted_products = [
      {
        'id': 'A',
        'name': 'CartaA',
        'quantity': 2,
      },
      {
        'id': 'B',
        'name': 'CartaB',
        'quantity': 1,
      },
    ]

    product_sellers = [
      {
        'id': '1',
        'name': 'Venditore1',
        'shipping': 10,
        'catalog': {
          'A': {
            'price': 50,
            'quantity': 1
          },
          'B': {
            'price': 20,
            'quantity': 1
          },
        }
      },
      {
        'id': '2',
        'name': 'Venditore2',
        'shipping': 30,
        'catalog': {
          'A': {
            'price': 21,
            'quantity': 1
          }
        }
      },
    ]

    result = optimize_cart(wanted_products, product_sellers)

    self.assertEqual(result['solvable'], True)
    self.assertEqual(result['total'], 131)
    self.assertEqual(len(result['sellers']), len(product_sellers))

  def test_requested_quantities_are_not_available(self):
    wanted_products = [
      {
        'id': 'A',
        'name': 'CartaA',
        'quantity': 2,
      },
    ]

    product_sellers = [
      {
        'id': '1',
        'name': 'Venditore1',
        'shipping': 30,
        'catalog': {
          'A': {
            'price': 21,
            'quantity': 1
          }
        }
      },
    ]

    result = optimize_cart(wanted_products, product_sellers)

    self.assertEqual(result['solvable'], False)
    self.assertEqual('total' in result, False)
    self.assertEqual('sellers' in result, False)
