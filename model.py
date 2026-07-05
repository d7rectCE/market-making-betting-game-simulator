"""
Market-Making & Betting-Game Simulator

Assembled from your step-by-step solutions.
"""

import numpy as np

# Step 1 - expected_value
def expected_value(values, probabilities):
    values = np.array(values)
    probabilities = np.array(probabilities)
    
    E = np.sum(values * probabilities)
    return E

# Step 2 - one_reroll_die_value
def one_reroll_die_value(sides):
    faces = np.arange(1, sides + 1)
    mu = expected_value(faces, np.ones(sides) / sides)

    values_under_policy = np.maximum(faces, mu)
    value = expected_value(values_under_policy, np.ones(sides) / sides)
    
    reroll_faces = [int(f) for f in faces[faces < mu]]
    
    return {
        'value': float(value),  
        'reroll_faces': reroll_faces
    }

# Step 3 - pay_per_reroll_die_game
def pay_per_reroll_die_game(sides, reroll_cost):
    best_value = -float('inf')
    best_threshold = 1
    
    for t in range(1, sides + 1):
        N = sides
        V_t = (t + N) / 2 - ((t - 1) / (N - t + 1) * reroll_cost)
        
        if V_t > best_value:
            best_value = V_t
            best_threshold = t
    return {
        'threshold': best_threshold,
        'value': best_value
    }

# Step 4 - red_black_card_game_value
from functools import lru_cache
def red_black_card_game_value(num_red, num_black):
    
    @lru_cache(maxsize=None)
    def V(r, b):
        if r == 0:
            return 0.0
        if b == 0:
            return float(r)
        
        total = r + b
        draw_red = (r / total) * (1 + V(r - 1, b))
        draw_black = (b / total) * (-1 + V(r, b - 1))
        cont = draw_red + draw_black
        
        return max(0.0, cont)

    value = V(num_red, num_black)
    
    def continuation_value():
        r, b = num_red, num_black
        if r == 0:
            return 0.0
        if b == 0:
            return float(r)
        
        total = r + b
        draw_red = (r / total) * (1 + V(r - 1, b))
        draw_black = (b / total) * (-1 + V(r, b - 1))
        return draw_red + draw_black
    
    cont = continuation_value()
    stop_now = cont <= 0.0
    
    return {'value': value, 'stop_now': stop_now}

# Step 5 - make_quotes
def make_quotes(fair_value, spread_width):
    bid = fair_value - spread_width/2
    ask = fair_value + spread_width/2
    return {
        "bid": bid,
        "ask": ask
    }

# Step 6 - execute_trade
def execute_trade(state, side, bid, ask, size=1):
    cash = state['cash']
    inventory = state['inventory']
    
    if side == 'buy':
        cash += size * ask 
        inventory -= size
    if side == 'sell':
        cash += size * -bid 
        inventory += size
        
    return {
        'cash': cash,
        'inventory': inventory
    }

# Step 7 - mark_to_market_pnl
def mark_to_market_pnl(cash, inventory, settlement_value):
    return cash + inventory * settlement_value

# Step 8 - adverse_selection_loss
def adverse_selection_loss(fair_value, bid, ask, informed_values, informed_probabilities):
    informed_values = np.array(informed_values)
    informed_probabilities = np.array(informed_probabilities)
    
    ask_loss = np.maximum(informed_values - ask, 0.0)
    bid_loss = np.maximum(bid - informed_values, 0.0)
    
    expected_loss = np.sum(informed_probabilities * ask_loss) + np.sum(informed_probabilities * bid_loss)
    
    return float(expected_loss)

# Step 9 - uncertainty_spread
def uncertainty_spread(base_spread, uncertainty):
    s = base_spread + uncertainty
    return s

# Step 10 - inventory_skewed_quotes
def inventory_skewed_quotes(fair_value, spread_width, inventory, skew_strength):
    half = spread_width / 2
    shift = inventory * skew_strength
    mid = fair_value - shift
    return {'bid': mid - half, 'ask': mid + half}

# Step 11 - update_fair_value_from_trade
def update_fair_value_from_trade(fair_value, side, bid, ask, adjustment):
    half_spread = (ask - bid) / 2
    
    if side == 'buy':
        direction = 1
    elif side == 'sell':
        direction = -1
    else:
        direction = 0
        
    new_fair = fair_value + direction * (adjustment * half_spread)
    return new_fair

# Step 12 - update_remaining_card_value (not yet solved)
# TODO: implement

# Step 13 - run_market_making_episode
def run_market_making_episode(true_value, counterparty_sides, initial_fair_value, config):
    base_spread = config.get('base_spread', 0.0)
    uncertainty = config.get('uncertainty', 0.0)
    skew_strength = config.get('skew_strength', 0.0)
    belief_adjustment = config.get('belief_adjustment', 0.0)
    
    cash = 0.0
    inventory = 0
    fair_value = float(initial_fair_value)
    history = []
    
    for side in counterparty_sides:
        spread_width = uncertainty_spread(base_spread, uncertainty)
        quotes = inventory_skewed_quotes(fair_value, spread_width, inventory, skew_strength)
        bid = quotes['bid']
        ask = quotes['ask']
        
        current_state = {'cash': cash, 'inventory': inventory}
        new_state = execute_trade(current_state, side, bid, ask, size=1)
        cash = new_state['cash']
        inventory = new_state['inventory']
        fair_value = update_fair_value_from_trade(fair_value, side, bid, ask, belief_adjustment)
        
        history.append({
            'bid': bid,
            'ask': ask,
            'side': side,
            'cash': cash,
            'inventory': inventory,
            'fair_value': fair_value
        })
        
    final_pnl = mark_to_market_pnl(cash, inventory, true_value)
    
    return {
        'pnl': final_pnl,
        'cash': cash,
        'inventory': inventory,
        'fair_value': fair_value,
        'history': history
    }

# Step 14 - summarize_episode_pnls
def summarize_episode_pnls(pnls):
    pnls = np.array(pnls)
    return {
        'mean': np.mean(pnls),
        'std': np.std(pnls),
        'worst': np.min(pnls)
    }

