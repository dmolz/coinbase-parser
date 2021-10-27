# coinbase-parser

## Instructions

Clone this repo

Download your account statements in .csv format from coinbase.com and/or pro.coinbase.com

Move your account statements into the repo's directory and rename the Coinbase account statement to `coinbase.csv` and the Coinbase Pro account statement to `coinbasepro.csv`

Run `python3 coinbase_parser.py`

Your portfolio will be stored in `coinbase_portfolio.json`

## Output

Example portfolio entry for MATIC:
```
{
	"MATIC": {
        "avg_cost": 0.3685626328056357, 
        "amount": 347.37426439,
        "usd_spent": 513.91425,
        "sold": {
            "qty": [
                0.6,
                696.4,
                350.0
            ],
            "prices": [
                1.0418835000000002,
                1.0412804999999998,
                2.4924
            ],
            "total_usd": 1598.1128703
        },
        "sent": 0
}
```

**avg_cost:** Average cost of all MATIC purchased

**amount:** Amount of MATIC currently held on Coinbase/Pro

**usd_spent:** Total amount of USD spent on MATIC

**sold, qty:** List of amounts of MATIC sold during each sell order

**sold, prices:** List of prices MATIC was at during each sell order

**sold, total_usd:** Total USD accrued from sales of MATIC

**sent:** Total amount of MATIC that has been sent to another wallet.

*NOTE:* Crypto that has been sent from Coinbase to other wallets will only show the total amount of that crypto that has been sent