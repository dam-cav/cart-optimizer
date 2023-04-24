import re
from pulp import LpMinimize, LpProblem, LpVariable, lpSum , apis

def optimize_cart(wanted_products, product_sellers):
  '''
    this builds this linear programming problem:

    objective function to minimize costs:
    min( (BuyFromSellerX * SellerXShippingPrice + ...) +  (PickCardAFromSellerX * SellerXCardAPrice + ...) )

    subject to:
      1 - I must buy from at least one seller
      BuyFromSellerX + BuyFromSellerY + ... >= 1

      2 - if I buy card from one seller, I need to pay him shipping
      PickCardAFromSellerX + PickCardBFromSellerX + ... >= M * BuyFromSellerX
      PickCardAFromSellerY + PickCardBFromSellerY + ... >= M * BuyFromSellerY
      ... repeat for each seller

      3 - I must buy one unit of each requested card
      PickCardAFromSellerX + PickCardAFromSellerY + ... >= 1
      PickCardBFromSellerX + PickCardBFromSellerY + ... >= 1
      ... repeat for each required card
  '''

  wanted_products_ids = list(map((lambda p: p['id']), wanted_products))

  model = LpProblem(name="CartOptimization", sense=LpMinimize)
  objective_function = 0
  shipping_activator_value = len(wanted_products) + len(product_sellers)

  shippings_to_pay = []
  card_to_buy_by_card_id = {} # key is card_id
  card_to_buy_by_seller_id = {} # key is seller_id

  for seller in product_sellers:
    seller_id = seller['id']
    seller_name = seller['name']
    card_to_buy_by_seller_id[seller_id] = []

    # OBJECTIVE FUNCTION: builds (BuyFromSellerX * SellerXShippingPrice + ...) part
    shippings_to_pay.append(LpVariable(name="PaySeller{}Shipping".format(seller_name), cat="Binary"))
    objective_function += (seller['shipping'] * shippings_to_pay[-1])

    # OBJECTIVE FUNCTION: builds (PickCardAFromSellerX * SellerXCardAPrice + ...) part
    seller_matching_catalog = [
      {'id': card_id, 'price': card_value['price']}
      for card_id, card_value in seller['catalog'].items() if card_id in wanted_products_ids
    ]
    for card in seller_matching_catalog:
      card_id = card['id']
      if card_to_buy_by_card_id.get(card_id) == None:
        card_to_buy_by_card_id[card_id] = []

      # NOTE: variable name is used to get card id in the outputs
      card_seller_association = LpVariable(name="Card{}FromSeller{}".format(card_id, seller_name), lowBound=0, cat="Integer")
      card_to_buy_by_card_id[card_id].append(card_seller_association)
      card_to_buy_by_seller_id[seller_id].append(card_seller_association)
      objective_function += (card['price'] * card_to_buy_by_card_id[card_id][-1])

    # CONSTRAINT: I have to pay the shipment of a seller if I take even only one of his cards
    model += (lpSum(card_to_buy_by_seller_id[seller_id]) - shipping_activator_value * shippings_to_pay[-1] <= 0, "MustPay{}ShippingWhenBuyingFromIt".format(seller_name))

  # CONSTRAINT: I always have to pay at least one shipment
  model += (lpSum(shippings_to_pay) >= 1, "always_one_seller")

  # CONSTRAINT: I must take at least one unit of each required card
  for card_id, card_from_sellers in card_to_buy_by_card_id.items():
    model += (lpSum(card_from_sellers) >= 1, "get_card_{}".format(card_id))

  model += objective_function
  model.solve(apis.PULP_CBC_CMD(msg=False))

  # build output result
  result_sellers = {}
  for index, seller in enumerate(product_sellers):
    paying_shipping = shippings_to_pay[index].value() == 1

    # if I'm paying him shipping, I'm getting something
    if paying_shipping:
      result_sellers[seller['id']] = { 'shipping': seller['shipping'] }
      picked_cards = [c for c in card_to_buy_by_seller_id[seller['id']] if c.value() == 1]

      # TODO: I'm getting card id back from the LpVariable name, maybe find another way???
      result_sellers[seller['id']]['cards'] = [(re.search("^Card(.+)FromSeller.+$", c.name).group(1)) for c in picked_cards]

  return {
    'total': model.objective.value(),
    'sellers': result_sellers
  }
