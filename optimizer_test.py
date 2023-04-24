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
      },
      {
        'id': 'B',
        'name': 'CartaA',
      },
    ]

    product_sellers = [
      {
        'id': '1',
        'name': 'Venditore1',
        'shipping': 10,
        'catalog': {
          'A': {
            'price': 50
          },
          'B': {
            'price': 20
          },
        }
      },
      {
        'id': '2',
        'name': 'Venditore2',
        'shipping': 30,
        'catalog': {
          'A': {
            'price': 19
          }
        }
      },
    ]

    result = optimize_cart(wanted_products, product_sellers)

    self.assertEqual(result['total'], 79,)
    self.assertEqual(len(result['sellers']), 2)

  def test_when_unique_order_is_better(self):
    wanted_products = [
      {
        'id': 'A',
        'name': 'CartaA',
      },
      {
        'id': 'B',
        'name': 'CartaA',
      },
    ]

    product_sellers = [
      {
        'id': '1',
        'name': 'Venditore1',
        'shipping': 10,
        'catalog': {
          'A': {
            'price': 50
          },
          'B': {
            'price': 20
          },
        }
      },
      {
        'id': '2',
        'name': 'Venditore2',
        'shipping': 30,
        'catalog': {
          'A': {
            'price': 21
          }
        }
      },
    ]

    result = optimize_cart(wanted_products, product_sellers)

    self.assertEqual(result['total'], 80)
    self.assertEqual(len(result['sellers']), 1)
