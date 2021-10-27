# portfolio-tracker

## Instructions

Clone this repo

Download your account statements in .csv format from coinbase.com and/or pro.coinbase.com

Move your account statements into the repo's directory and rename the Coinbase account statement to `coinbase.csv` and the Coinbase Pro account statement to `coinbasepro.csv`

Run `python3 coinbase_parser.py`

Your portfolio will be stored in `coinbase_portfolio.json`

Example portfolio entry for MATIC:
```
{
	"MATIC": {
        "avg_cost": 0.3685626328056357, # Average cost of all MATIC purchased
        "amount": 347.37426439, 		# Amount of MATIC currently held
        "usd_spent": 513.91425,			# Total amount of USD spent on MATIC
        "sold": {
            "qty": [					# List of quantities of MATIC
                0.6,					  across multiple sales
                696.4,
                350.0
            ],
            "prices": [					# List of prices MATIC was at when each
                1.0418835000000002,		  sale occurred
                1.0412804999999998,
                2.4924
            ],
            "total_usd": 1598.1128703	# Total USD accrued from sales of MATIC
        },
        "sent": 0						# Total amount of MATIC that has been
    }									  sent to another wallet
}
```

Crypto that has been sent from Coinbase to other wallets will only show the total amount of that crypto that has been sent