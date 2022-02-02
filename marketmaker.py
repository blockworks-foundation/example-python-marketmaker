import logging
import mango
import mango.marketmaking
import time

from datetime import datetime
from decimal import Decimal

from mango.marketmaking.orderchain.chain import Chain
from mango.marketmaking.orderchain.ratioselement import RatiosElement
from mango.marketmaking.orderchain.roundtolotsizeelement import RoundToLotSizeElement

MARKET = "BTC-PERP"
ORACLE = "ftx"
PULSE_INTERVAL = 10

mango.setup_logging(logging.DEBUG, False)

print("Started at", datetime.now())
print("Press Control-C to quit")
try:
    context = mango.ContextBuilder.build(
        cluster_name="devnet", stale_data_pauses_before_retry=[0.1, 0.2, 0.3, 0.5, 1]
    )

    wallet = mango.Wallet.load("id.json")
    group = mango.Group.load(context, context.group_address)
    accounts = mango.Account.load_all_for_owner(context, wallet.address, group)
    if len(accounts) == 0:
        raise Exception(f"No Mango Accounts for wallet {wallet.address}")
    account = accounts[0]

    # Set up the market
    market_stub = context.market_lookup.find_by_symbol(MARKET)
    if market_stub is None:
        raise Exception(f"Could not find market {MARKET}")
    market = mango.ensure_market_loaded(context, market_stub)

    instruction_builder = mango.PerpMarketInstructionBuilder(
        context, wallet, market, group, account
    )

    # Set up the oracle
    oracle_provider: mango.OracleProvider = mango.create_oracle_provider(
        context, ORACLE
    )
    oracle = oracle_provider.oracle_for_market(context, market)

    # Set up the marketmaker chain
    ratios_element = RatiosElement(
        mango.OrderType.POST_ONLY_SLIDE, [Decimal("0.001")], [Decimal("0.05")], False
    )
    round_to_lot_size_element = RoundToLotSizeElement()
    desired_orders_chain = Chain([ratios_element, round_to_lot_size_element])

    order_reconciler = mango.marketmaking.ToleranceOrderReconciler(
        Decimal("0.001"), Decimal("0.001")
    )

    model_state_builder = mango.marketmaking.PerpPollingModelStateBuilder(
        account.address, market, oracle, group.address, group.cache
    )

    market_maker = mango.marketmaking.MarketMaker(
        wallet,
        market,
        instruction_builder,
        desired_orders_chain,
        order_reconciler,
        None,
    )

    while True:
        context.client.require_data_from_fresh_slot()
        model_state = model_state_builder.build(context)
        market_maker.pulse(context, model_state)

        time.sleep(PULSE_INTERVAL)
except KeyboardInterrupt:
    pass
except Exception as ex:
    print(ex)

payer = mango.CombinableInstructions.from_wallet(wallet)
cancel_all = instruction_builder.build_cancel_all_orders_instructions()
cancel_all_signatures = (payer + cancel_all).execute(context)
print(f"Cleaning up - cancelling all perp orders: {cancel_all_signatures}")
print("\nStopped at", datetime.now())
