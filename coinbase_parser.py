
import csv
import json
import sys
import os
from datetime import datetime
import cryptocompare

def get_portfolio_value(crypto_dict):
	"""
	Get total portfolio value including sales
	"""
	total_value = 0
	total_return = 0
	for asset in crypto_dict:
		c = crypto_dict[asset]
		total_value += c["market_value"]
		total_return += c["total_return"]

	result = {
		"portfolio_value": {
			"datetime": str(datetime.now()),
			"total_value": round(total_value, 2),
			"total_return": round(total_return, 2)
		},
		"portfolio": crypto_dict
	}
	return result

def get_current_prices(crypto_dict):
	"""
	Use cryptocompare API to get current prices on all crypto
	"""
	for asset in crypto_dict:
		c = crypto_dict[asset]
		price = cryptocompare.get_price(asset, currency="USD")[asset]["USD"]
		c["current_price"] = price
		c["market_value"] = round(c["amount"] * c["current_price"], 2)
		c["total_return"] = round(c["market_value"] - c["usd_spent"] + c["sold"]["total_usd"] + c["sent"] * price, 2)

def get_crypto_dict(trade_dict):
	"""
	Function for parsing trade data that was parsed from Coinbase and
	Coinbase Pro csv account statements
	"""
	crypto_dict = {}
	for trade_id in trade_dict:
		trade = trade_dict[trade_id]
		asset = trade["token"]
		if asset == "":
			continue
		
		# put new crypto in dict
		if trade["token"] not in crypto_dict and trade["token"] != "USD":
			crypto_dict[asset] = {
				"avg_cost": 0,
				"amount": 0,
				"usd_spent": 0,
				"sold": {
					"qty": [],
					"prices": [],
					"total_usd": 0
				},
				"sent": 0
			}

		# add values to dict
		if trade["type"] == "buy":
			crypto_dict[asset]["amount"] += trade["token_amount"]
			crypto_dict[asset]["usd_spent"] += trade["usd"]
		elif trade["type"] == "sell":
			crypto_dict[asset]["sold"]["qty"].append(round(trade["token_amount"], 4))
			crypto_dict[asset]["sold"]["prices"].append(round(trade["price"], 4))
		elif trade["type"] == "send":
			crypto_dict[asset]["sent"] += trade["sent"]

	# More calculations and rounding
	for asset in crypto_dict:
		c = crypto_dict[asset]

		# Calculations
		c["avg_cost"] = round(c["usd_spent"] / c["amount"], 4)
		c["amount"] -= sum(c["sold"]["qty"])
		c["amount"] -= c["sent"]

		# Rounding
		c["usd_spent"] = round(c["usd_spent"], 2)
		c["amount"] = round(c["amount"], 4)

		# Sells
		for i in range(len(c["sold"]["qty"])):
			c["sold"]["total_usd"] += c["sold"]["qty"][i] * c["sold"]["prices"][i]
			c["sold"]["total_usd"] = round(c["sold"]["total_usd"], 4)

	return crypto_dict


def parse_coinbase(filename):
	"""
	Function for parsing coinbase csv file
	"""
	f = open(filename, 'r')
	csv_reader = csv.reader(f, delimiter=',')

	trade_dict = {}
	for row in csv_reader:
		# skip first lines
		if len(row) == 0:
			continue
		if not row[0].startswith("2"):
			continue

		trade_id = row[0]
		trade_type = row[1]
		asset = row[2]
		amount = float(row[3])
		price = float(row[4])
		try:
			amount_usd = float(row[6])
		except ValueError:
			amount_usd = 0

		if trade_id not in trade_dict:
			trade_dict[trade_id] = {
				"usd": 0,
				"token": asset,
				"token_amount": 0,
				"type": "",
				"price": 0,
				"sent": 0
			}

		# Buy
		if trade_type == "Buy":
			trade_dict[trade_id]["type"] = "buy"
			trade_dict[trade_id]["usd"] += abs(amount_usd)
			trade_dict[trade_id]["token_amount"] += abs(amount)
			trade_dict[trade_id]["price"] = price

		# Sell
		elif trade_type == "Sell":
			trade_dict[trade_id]["type"] = "sell"
			trade_dict[trade_id]["usd"] += abs(amount_usd)
			trade_dict[trade_id]["token_amount"] += abs(amount)
			trade_dict[trade_id]["price"] = price

		# Rewards Income or Coinbase Earn
		elif trade_type == "Rewards Income" or trade_type == "Coinbase Earn":
			trade_dict[trade_id]["type"] = "buy"
			trade_dict[trade_id]["token_amount"] += abs(amount)
			trade_dict[trade_id]["price"] = price

		# Send
		elif trade_type == "Send":
			trade_dict[trade_id]["type"] = "send"
			trade_dict[trade_id]["sent"] += amount

		# Unhandled trade
		else:
			print(f"Unhandled trade type: {trade_type}")
			continue
	
	f.close()
	return trade_dict

def parse_coinbase_pro(filename):
	"""
	Function for parsing coinbase pro csv file
	"""
	f = open(filename, 'r')
	csv_reader = csv.reader(f, delimiter=',')

	trade_dict = {}
	for row in csv_reader:
		# skip first line
		if row[0] == "portfolio":
			continue

		# skip deposits and withdrawals
		if row[1] == "deposit" or row[1] == "withdrawal":
			continue

		trade_id = row[7]
		asset = row[5]
		amount = float(row[3])
		trade_type = row[1]

		if trade_id not in trade_dict:
			trade_dict[trade_id] = {
				"usd": 0,
				"token": "",
				"token_amount": 0,
				"type": "",
				"price": 0
			}

		# "match" could be a buy or sell, broken into multiple transactions
		# 	under the same trade id
		if trade_type == "match":
			# USD being spent to purchase the crypto
			if asset == "USD" and amount < 0:
				trade_dict[trade_id]["type"] = "buy"
				trade_dict[trade_id]["usd"] += abs(amount)
			
			# Crypto being received from buy
			elif asset != "USD" and amount > 0:
				trade_dict[trade_id]["token"] = asset
				trade_dict[trade_id]["token_amount"] += abs(amount)
			
			# USD being received from sell
			elif asset == "USD" and amount > 0:
				trade_dict[trade_id]["type"] = "sell"
				trade_dict[trade_id]["usd"] += abs(amount)
			
			# Crypto being sold
			elif asset != "USD" and amount < 0:
				trade_dict[trade_id]["token"] = asset
				trade_dict[trade_id]["token_amount"] += abs(amount)
		
		# Add fee as if it's part of the crypto's price
		elif trade_type == "fee":
			trade_dict[trade_id]["usd"] += abs(amount)
		
		# Unhandled trade type
		else:
			sys.stderr.write(f"Unhandled trade type: {trade_type}")
			continue
	f.close()

	# Calculate the price of the crypto at the time of the trade's occurrence
	for trade_id in trade_dict:
		trade_dict[trade_id]["price"] = \
			trade_dict[trade_id]["usd"] / trade_dict[trade_id]["token_amount"]

	return trade_dict

if __name__ == "__main__":
	# Parse csv files
	cb_dict = {}
	cbpro_dict = {}
	if os.path.exists("./coinbasepro.csv"):
		cbpro_dict = parse_coinbase_pro('coinbasepro.csv')
	if os.path.exists("./coinbase.csv"):
		cb_dict = parse_coinbase('coinbase.csv')

	# Merge Coinbase and Coinbase Pro trade data into one dict
	trade_dict = cbpro_dict
	trade_dict.update(cb_dict)

	# Parse trades
	crypto_dict = get_crypto_dict(trade_dict)
	get_current_prices(crypto_dict)
	result = get_portfolio_value(crypto_dict)
	
	f = open("coinbase_portfolio.json", 'w')
	f.write(json.dumps(result, indent=4))
	f.close()

