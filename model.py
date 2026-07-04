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

# Step 4 - red_black_card_game_value (not yet solved)
# TODO: implement

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

# Step 9 - uncertainty_spread (not yet solved)
# TODO: implement

# Step 10 - inventory_skewed_quotes (not yet solved)
# TODO: implement

# Step 11 - update_fair_value_from_trade (not yet solved)
# TODO: implement

# Step 12 - update_remaining_card_value (not yet solved)
# TODO: implement

# Step 13 - run_market_making_episode (not yet solved)
# TODO: implement

# Step 14 - summarize_episode_pnls (not yet solved)
# TODO: implement

