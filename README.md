# 🥭 Mango Explorer

## 📖 Introduction

This guide will show you how to load and run a customisable marketmaker that runs on [Mango Markets](https://mango.markets) using the [mango-explorer](https://github.com/blockworks-foundation/mango-explorer/) library.

There are plenty of ways to do this. This document shows only one possible approach.


## 🪜 Prerequisites

1. [Installation and Dependencies](1.Installation.md) - shows you how to set up a Python virtual environment and pip install `mango-explorer`. (_Optional - feel free to skip if you're comfortable doing this on your own._)
2. [Devnet Wallet Creation](2.Wallet.md) - shows you how to create a Solana `Keypair` file and prepare it for devnet with some devnet SOL and devnet USDC. (_Optional - feel free to skip if you're comfortable doing this on your own._)
3. [Devnet Mango Account Creation](3.MangoAccount.md) - shows you how to create a Mango Account on devnet and deposit devnet USDC into it. (_Optional - feel free to skip if you're comfortable doing this on your own._)
4. [Code Walkthrough](4.CodeWalkthrough.md) - takes you through the code in `marketmaker.py` line by line. (_Optional - feel free to skip if you're comfortable doing this on your own._)


# 🏃 Running the Marketmaker

That's a lot of setup to get you to this stage but some of it was skippable if you already had a Python venv, Solana wallet and a Mango Account. And if you didn't, you do now!

You can now start the marketmaker by running:
```
python marketmaker.py
```

No parameters are required - all the parameters and options for running the marketmaker are in the code.

When you run it you should see a lot of output, with large 'pulses' of output every 10 seconds or so. (You can tweak the volume of logging and the pulse interval in the code.)


# 🛵 Next Steps

If you've got this far, congratulations! You're now running a marketmaker on devnet.

Things you can do now:
* experiment with different parameters to see how that changes the orders.
* experiment with different `Element`s to filter orders or bias prices or quantities in certain circumstances. (Want to shift the prices in your orders if you've built up too much inventory? Can do!)
* create your own custom `Element`s to change order quantities or prices based on new criteria. (Want to widen the spread when volatility is high? Create a custom `Element`!)


# 🦮 Support

[🥭 Mango Markets](https://mango.markets/) support is available at: [Docs](https://docs.mango.markets/) | [Discord](https://discord.gg/67jySBhxrg) | [Twitter](https://twitter.com/mangomarkets) | [Github](https://github.com/blockworks-foundation) | [Email](mailto:hello@blockworks.foundation)