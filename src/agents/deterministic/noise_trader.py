from typing import Dict, List
import random
from agents.base_agent import BaseAgent
from agents.agents_api import TradeDecision, OrderType, OrderDetails

class NoiseTrader(BaseAgent):
    """
    Noise trader that randomly buys, sells, or holds.
    Represents irrational/random trading behavior that adds noise to markets.
    Always uses market orders for immediate execution.
    """

    def __init__(self,
                 max_trade_proportion: float = 0.3,  # Max 30% of cash/holdings per trade
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_trade_proportion = max_trade_proportion

    def make_decision(self, market_state: Dict, history: List, round_number: int) -> TradeDecision:
        price = market_state['price']

        # Calculate total portfolio value
        portfolio_value = self.available_cash + (self.total_shares * price)

        # Randomly choose action: 0=hold, 1=buy, 2=sell
        action = random.randint(0, 2)

        # Hold
        if action == 0:
            return TradeDecision(
                orders=[],
                replace_decision="Add",
                reasoning="Randomly chose to hold this round",
                valuation=price,
                valuation_reasoning="No valuation - noise trader",
                price_prediction_reasoning="Random expectations",
                price_prediction_t=price,
                price_prediction_t1=price,
                price_prediction_t2=price,
            )

        # Random dollar amount to trade (10-30% of portfolio)
        trade_proportion = random.uniform(0.1, self.max_trade_proportion)
        dollar_amount = portfolio_value * trade_proportion
        quantity = max(1, int(dollar_amount / price))

        # Buy
        if action == 1:
            # Check if we have enough cash for the trade
            max_affordable = int(self.available_cash / price)

            if max_affordable == 0:
                return TradeDecision(
                    orders=[],
                    replace_decision="Add",
                    reasoning="Want to buy but insufficient cash",
                    valuation=price,
                    valuation_reasoning="No valuation - noise trader",
                    price_prediction_reasoning="Random expectations",
                    price_prediction_t=price,
                    price_prediction_t1=price,
                    price_prediction_t2=price,
                )

            # Limit quantity to what we can afford
            quantity = min(quantity, max_affordable)

            order = OrderDetails(
                decision="Buy",
                quantity=quantity,
                order_type=OrderType.MARKET
            )

            return TradeDecision(
                orders=[order],
                replace_decision="Replace",
                reasoning=f"Randomly chose to buy {quantity} shares at market price",
                valuation=price,
                valuation_reasoning="No valuation - noise trader",
                price_prediction_reasoning="Random expectations",
                price_prediction_t=price,
                price_prediction_t1=price * random.uniform(0.95, 1.05),
                price_prediction_t2=price * random.uniform(0.95, 1.05),
            )

        # Sell
        else:
            if self.total_shares == 0:
                return TradeDecision(
                    orders=[],
                    replace_decision="Add",
                    reasoning="Want to sell but no shares to sell",
                    valuation=price,
                    valuation_reasoning="No valuation - noise trader",
                    price_prediction_reasoning="Random expectations",
                    price_prediction_t=price,
                    price_prediction_t1=price,
                    price_prediction_t2=price,
                )

            # Limit quantity to what we own
            quantity = min(quantity, self.total_shares)

            order = OrderDetails(
                decision="Sell",
                quantity=quantity,
                order_type=OrderType.MARKET
            )

            return TradeDecision(
                orders=[order],
                replace_decision="Replace",
                reasoning=f"Randomly chose to sell {quantity} shares at market price",
                valuation=price,
                valuation_reasoning="No valuation - noise trader",
                price_prediction_reasoning="Random expectations",
                price_prediction_t=price,
                price_prediction_t1=price * random.uniform(0.95, 1.05),
                price_prediction_t2=price * random.uniform(0.95, 1.05),
            )
