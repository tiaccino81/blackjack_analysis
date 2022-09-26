# By Theodore Iaccino
# This program simulates a user-specified number of blackjack hands and records relevant metrics
# Analysis of the hands can be found at blackjack_analysis.r, where we attempt to recreate 'Basic Strategy'
# Results are recorded in 'hit.csv' and 'stand.csv'
# Blackjack rules can be found @ https://bicyclecards.com/how-to-play/blackjack/

import random
import pandas as pd
from tqdm import tqdm
from IPython.display import display

# Creating the 6 deck shoe
deck = [2,3,4,5,6,7,8,9,10,10,10,10,11] * 6

# Standing hands will be kept here
results_stand = {
    'PC1': [],
    'PC2': [],
    'DC1': [],
    'DC2': [],
    'DC3': [],
    'Player_Total': [],
    'Dealer_Total': [],
    'Result': []
}

# Hitting hands will be kept here
results_hit = {
    'PC1': [],
    'PC2': [],
    'PC3': [],
    'DC1': [],
    'DC2': [],
    'DC3': [],
    'player_open_total': [],
    'Player_Total': [],
    'Dealer_Total': [],
    'Result': []
}

hands_played = 0
player_wins = 0
player_bj = 0

def play():
    global hands_played
    global player_wins
    global player_bj

    # holds the dealers cards
    dealer_cards = []

    #Used cards will be stored here so that they can not be dealt twice. these will be returned to the deck at the end of the hand
    cards_dealt = []

    # we want to hit 50% of the time. The results will be placed into two different dictionaries depending on the move.
    if hands_played % 2 == 0:
        hit_or_stand = 'H'

    else:
        hit_or_stand = 'S'

    hands_played += 1

    # players first two cards
    player_card_1 = random.choice(deck)
    # will be replaced after completion of the hand
    deck.remove(player_card_1)

    player_card_2 = random.choice(deck)
    deck.remove(player_card_2)

    # if the player hits, he will be dealt a third card
    if hit_or_stand == 'H':
        player_card_3 = random.choice(deck)

    # if the player does not hit, he will not receive another card
    else:
        player_card_3 = 'NA'

    #players second ace can be played as 1
    if player_card_1 == 11 and player_card_2 == 11:
        player_card_2 = 1

    ace_count = 0

    #dealer stands on soft 16
    while sum(dealer_cards) <= 16:
        current_dealer_card = random.choice(deck)

        if current_dealer_card == 11 and sum(dealer_cards) + current_dealer_card <= 21 and ace_count < 1:
            ace_count += 1

        elif current_dealer_card == 11:
            current_dealer_card = 1
            ace_count += 1

        dealer_cards.append(current_dealer_card)


    # Players initial total
    player_total = player_card_1 + player_card_2
    player_open_total = player_total

    # If the player was dealt a third card, we will add it to the total
    if player_card_3 != 'NA':
        player_total += player_card_3

    # adding up the dealers cards
    dealer_total = sum(dealer_cards)

    # game logic
    #player busts
    if player_total > 21:
        result = 'L'

    #player and dealer push (tie)
    elif player_total == dealer_total:
       result = 'P'

    elif player_total == 21:
        result = 'W'
        player_bj += 1

    elif player_total <= 21 and dealer_total > 21:
        result = 'W'

    elif player_total <= 21 and player_total > dealer_total:
        result = 'W'

    else:
        result = 'L'

    #return cards to deck for next hand
    #deck.append(cards_dealt)
    deck.append(player_card_1)
    deck.append(player_card_2)

    # Adding hand details and result to the results dictionary FOR WHEN WE HIT
    if hit_or_stand == 'H':
        results_hit["PC1"].append(player_card_1)
        results_hit['PC2'].append(player_card_2)

        results_hit['PC3'].append(player_card_3)

        results_hit['DC1'].append(dealer_cards[0])
        results_hit['DC2'].append(dealer_cards[1])
        if len(dealer_cards) == 3:
            results_hit['DC3'].append(dealer_cards[2])
        else:
            results_hit['DC3'].append('NA')
        results_hit["player_open_total"].append(player_open_total)

        results_hit["Player_Total"].append(player_total)
        results_hit['Dealer_Total'].append(dealer_total)
        results_hit['Result'].append(result)

    # Adding hand details and result to the results dictionary FOR WHEN WE STAND
    if hit_or_stand == 'S':
        results_stand["PC1"].append(player_card_1)
        results_stand['PC2'].append(player_card_2)

        results_stand['DC1'].append(dealer_cards[0])
        results_stand['DC2'].append(dealer_cards[1])
        if len(dealer_cards) == 3:
            results_stand['DC3'].append(dealer_cards[2])
        else:
            results_stand['DC3'].append('NA')

        results_stand["Player_Total"].append(player_total)
        results_stand['Dealer_Total'].append(dealer_total)
        results_stand['Result'].append(result)

    if result == 'W':
        player_wins +=1

# how many hands are to be played?
req_iterations = int(input('Desired Hands Played: '))

for i in tqdm(range(req_iterations), desc = 'Simulating Hands...'):
    #pass
    play()

win_pct = player_wins / req_iterations
print('\nWin Percentage: %', win_pct)

bj_pct = player_bj / req_iterations * 100
print('Blackjack Percentage (Target = 4.8%): %',bj_pct, '\n')

stand = pd.DataFrame(results_stand)
print('STANDING SAMPLE (SEE STAND.CSV)')
display(stand)

hit = pd.DataFrame(results_hit)
print('HITTING SAMPLE (SEE HIT.CSV)' )
display(hit)

hit.to_csv('hit.csv')
stand.to_csv('stand.csv')

