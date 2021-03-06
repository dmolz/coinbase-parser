# coinbase-parser

## Instructions

1. Clone this repo

2. Generate and download your account statements in .csv format from [Coinbase](https://www.coinbase.com/reports) and/or [Coinbase Pro](https://pro.coinbase.com/profile/statements)

3. Move your account statements into the repo's directory and rename the Coinbase account statement to `coinbase.csv` and the Coinbase Pro account statement to `coinbasepro.csv`

4. Install Python3 if you haven't done so already

5. Install the requirements with `pip3 install -r requirements.txt`

6. Run the script with `python3 coinbase_parser.py`

Your portfolio will be stored in `coinbase_portfolio.json`

## Output

Example portfolio entry for MATIC:
```
{
    "MATIC": {
        "avg_cost": 0.3686,
        "amount": 347.3743,
        "usd_spent": 513.91,
        "sold": {
            "qty": [
                700.0,
                350.0
            ],
            "prices": [
                1.0413,
                2.4924
            ],
            "total_usd": 1598.1264
        },
        "sent": 0,
        "current_price": 2.074,
        "market_value": 720.45,
        "total_return": 1804.67
    }
}
```

**avg_cost:** Average cost of all MATIC purchased

**amount:** Amount of MATIC currently held on Coinbase/Pro

**usd_spent:** Total amount of USD spent on MATIC

**sold, qty:** List of amounts of MATIC sold during each sell order

**sold, prices:** List of prices MATIC was at during each sell order

**sold, total_usd:** Total USD accrued from sales of MATIC

**sent:** Total amount of MATIC that has been sent to another wallet.

**current_price:** Current price of MATIC in USD

**market_value:** Market value of all MATIC currently held

**total_return:** Sum of all MATIC currently held and previously sold minus total amount of USD spent (also subtracts what would be the market value of all that was sent to another wallet, will probably change that part in the future)

*NOTE:* Crypto that has been sent from Coinbase to other wallets will only show the total amount of that crypto that has been sent

At the top of the output JSON will also be an entry with your portfolio's current value (which calculates the value in USD of all assets currently held, not factoring in sales) and total return (which calculates the amount of current unrealized gains plus sales)
