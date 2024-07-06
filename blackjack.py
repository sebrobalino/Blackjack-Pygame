import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen resolution
resolution = (1000, 800)

# Colors
orange = (255, 165, 0)
green = (0, 128, 0)
blue = (0, 0, 128)
red = (128, 0, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption("Blackjack")

# Define button positions and dimensions
button_font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)
input_font = pygame.font.SysFont(None, 48)
hit_button = pygame.Rect(800, 700, 80, 50)
stand_button = pygame.Rect(900, 700, 80, 50)
next_button = pygame.Rect(850, 650, 100, 50)
leave_button = pygame.Rect(825, 720, 150, 50)
play_button = pygame.Rect(400, 400, 200, 50)
thanks_button = pygame.Rect(375, 600, 250, 50)
peek_button = pygame.Rect(850, 600, 120, 50)
bet_button_width = 80
bet_button_height = 50
bet_button_spacing = 10
total_bet_buttons_width = 3 * bet_button_width + 2 * bet_button_spacing
bet_buttons_x = (resolution[0] - total_bet_buttons_width) // 2
bet_buttons_y = 600
bet10_button = pygame.Rect(bet_buttons_x, bet_buttons_y, bet_button_width, bet_button_height)
bet50_button = pygame.Rect(bet_buttons_x + bet_button_width + bet_button_spacing, bet_buttons_y, bet_button_width, bet_button_height)
bet100_button = pygame.Rect(bet_buttons_x + 2 * (bet_button_width + bet_button_spacing), bet_buttons_y, bet_button_width, bet_button_height)
toggle_button = pygame.Rect(400, 20, 200, 50)  # Adjusted toggle button size

# Buttons for bankrupt state
give_up_button = pygame.Rect(450, 400, 100, 50)
more_money_button = pygame.Rect(300, 500, 400, 50)

# Initialize game state variables
player_balance = 0
starting_balance = 0
bet_amount = 0
show_scores = True
bet_error_message = ""
input_text = ""
input_active = False
game_started = False
title_screen = True
end_game_screen = False
dealer_peeked = False

# Create a deck of cards
suits = ['hearts', 'diamonds', 'clubs', 'spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
deck = [f'{rank}_of_{suit}.png' for suit in suits for rank in ranks]

# Load and resize card images
def load_card_image(card_filename):
    image = pygame.image.load(f'cards/{card_filename}')
    return pygame.transform.scale(image, (150, 200))  # Resize to 150x200 pixels

# Get the value of a card
def get_card_value(card_filename):
    rank = card_filename.split('_')[0]
    if rank in ['jack', 'queen', 'king']:
        return 10
    elif rank == 'ace':
        return 11
    else:
        return int(rank)

# Calculate the value of a hand
def calculate_hand_value(hand, reveal_all=True):
    value = 0
    num_aces = 0
    for i, card in enumerate(hand):
        if not reveal_all and i == 0:  # Skip the first card if not revealing all
            continue
        card_value = get_card_value(card)
        if card_value == 11:
            num_aces += 1
        value += card_value
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

# Deal cards to player and dealer
def deal_cards(deck, num_cards):
    return random.sample(deck, num_cards)

def reset_game():
    global player_cards, dealer_cards, player_turn, winner, bet_amount, bet_error_message, dealer_peeked
    player_cards = deal_cards(deck, 2)
    dealer_cards = deal_cards(deck, 2)
    player_turn = True
    winner = None
    bet_amount = 0
    bet_error_message = ""
    dealer_peeked = False

reset_game()

# Main game loop
running = True
font = pygame.font.SysFont(None, 48)
betting_phase = False
bankrupt_phase = False

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if title_screen:
                if play_button.collidepoint(event.pos):
                    input_active = True
            elif end_game_screen:
                if thanks_button.collidepoint(event.pos):
                    running = False
            elif bankrupt_phase:
                if give_up_button.collidepoint(event.pos):
                    running = False
                elif more_money_button.collidepoint(event.pos):
                    player_balance = 500
                    reset_game()
                    betting_phase = True
                    bankrupt_phase = False
            elif betting_phase:
                if bet10_button.collidepoint(event.pos) and bet_amount + 10 <= player_balance:
                    bet_amount += 10
                    bet_error_message = ""
                elif bet50_button.collidepoint(event.pos) and bet_amount + 50 <= player_balance:
                    bet_amount += 50
                    bet_error_message = ""
                elif bet100_button.collidepoint(event.pos) and bet_amount + 100 <= player_balance:
                    bet_amount += 100
                    bet_error_message = ""
                elif bet_amount > 0 and bet_error_message == "":
                    player_hand_value = calculate_hand_value(player_cards)
                    if player_hand_value == 21 and len(player_cards) == 2:
                        winner = 'Blackjack! Player Wins 3:2!'
                        player_balance += int(bet_amount * 1.5)
                        player_turn = False
                        betting_phase = False
                    else:
                        betting_phase = False
                else:
                    bet_error_message = "You cannot bet more than your balance!"
            else:
                if hit_button.collidepoint(event.pos) and player_turn and bet_amount > 0:
                    player_cards.append(deal_cards(deck, 1)[0])
                    player_hand_value = calculate_hand_value(player_cards)
                    if player_hand_value > 21:
                        winner = 'Player Busted! Dealer Wins!'
                        player_balance -= bet_amount
                        player_turn = False
                elif stand_button.collidepoint(event.pos) and player_turn and bet_amount > 0:
                    player_turn = False
                    dealer_hand_value = calculate_hand_value(dealer_cards)
                    while dealer_hand_value < 17:
                        dealer_cards.append(deal_cards(deck, 1)[0])
                        dealer_hand_value = calculate_hand_value(dealer_cards)
                    if dealer_hand_value > 21:
                        winner = 'Dealer Busted! Player Wins!'
                        player_balance += bet_amount
                    elif dealer_hand_value > player_hand_value:
                        winner = 'Dealer Wins!'
                        player_balance -= bet_amount
                    elif dealer_hand_value < player_hand_value:
                        winner = 'Player Wins!'
                        player_balance += bet_amount
                    else:
                        winner = 'Push! It\'s a Tie!'
                elif next_button.collidepoint(event.pos) and winner is not None:
                    reset_game()
                    if player_balance == 0:
                        bankrupt_phase = True
                    else:
                        betting_phase = True
                elif leave_button.collidepoint(event.pos) and winner is not None:
                    title_screen = False
                    end_game_screen = True
                elif peek_button.collidepoint(event.pos) and not dealer_peeked:
                    dealer_peeked = True
                    dealer_hand_value = calculate_hand_value(dealer_cards, reveal_all=True)
                    if dealer_hand_value == 21:
                        winner = 'Dealer Blackjack! Dealer Wins!'
                        player_balance -= bet_amount
                        player_turn = False
                elif toggle_button.collidepoint(event.pos):
                    show_scores = not show_scores
        elif event.type == KEYDOWN:
            if input_active:
                if event.key == K_RETURN:
                    try:
                        starting_balance = int(input_text)
                        player_balance = starting_balance
                        input_active = False
                        title_screen = False
                        betting_phase = True
                    except ValueError:
                        input_text = ""
                elif event.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    if title_screen:
        screen.fill(orange)
        title_text = large_font.render('BLACKJACK', True, white)
        screen.blit(title_text, (resolution[0] // 2 - title_text.get_width() // 2, resolution[1] // 3 - title_text.get_height() // 2))
        
        pygame.draw.rect(screen, white, play_button)
        play_text = button_font.render('Play', True, black)
        screen.blit(play_text, (play_button.x + (play_button.width - play_text.get_width()) // 2, play_button.y + (play_button.height - play_text.get_height()) // 2))

        if input_active:
            input_box = pygame.Rect(400, 600, 200, 50)
            pygame.draw.rect(screen, white, input_box)
            input_text_surface = input_font.render(input_text, True, black)
            screen.blit(input_text_surface, (input_box.x + 10, input_box.y + 10))
            prompt_text = button_font.render('Enter Buy-In Amount:', True, white)
            screen.blit(prompt_text, (resolution[0] // 2 - prompt_text.get_width() // 2, 550))

    elif end_game_screen:
        screen.fill(yellow)
        final_balance_text = font.render(f'Your Final Balance is ${player_balance}', True, black)
        screen.blit(final_balance_text, (resolution[0] // 2 - final_balance_text.get_width() // 2, resolution[1] // 3 - final_balance_text.get_height() // 2))

        if player_balance > starting_balance:
            result_text = font.render(f'You Won ${player_balance - starting_balance}', True, black)
        elif player_balance < starting_balance:
            result_text = font.render(f'You Lost ${starting_balance - player_balance}', True, black)
        else:
            result_text = font.render('You Broke Even', True, black)
        
        screen.blit(result_text, (resolution[0] // 2 - result_text.get_width() // 2, resolution[1] // 2 - result_text.get_height() // 2))

        pygame.draw.rect(screen, white, thanks_button)
        thanks_text = button_font.render('Thanks For Playing!', True, black)
        screen.blit(thanks_text, (thanks_button.x + (thanks_button.width - thanks_text.get_width()) // 2, thanks_button.y + (thanks_button.height - thanks_text.get_height()) // 2))

    elif bankrupt_phase:
        screen.fill(red)
        bankrupt_text = font.render('You went bankrupt!', True, white)
        screen.blit(bankrupt_text, (resolution[0] // 2 - bankrupt_text.get_width() // 2, 300))
        
        pygame.draw.rect(screen, white, give_up_button)
        give_up_text = button_font.render('Give Up', True, black)
        screen.blit(give_up_text, (give_up_button.x + (give_up_button.width - give_up_text.get_width()) // 2, give_up_button.y + (give_up_button.height - give_up_text.get_height()) // 2))
        
        pygame.draw.rect(screen, white, more_money_button)
        more_money_text = button_font.render("I'm Broke... I need more money", True, black)
        screen.blit(more_money_text, (more_money_button.x + (more_money_button.width - more_money_text.get_width()) // 2, more_money_button.y + (more_money_button.height - more_money_text.get_height()) // 2))
    elif betting_phase:
        screen.fill(blue)
        bet_title_text = font.render('Place Your Bet', True, white)
        screen.blit(bet_title_text, (resolution[0] // 2 - bet_title_text.get_width() // 2, 400))
        
        # Draw betting buttons
        pygame.draw.rect(screen, white, bet10_button)
        pygame.draw.rect(screen, white, bet50_button)
        pygame.draw.rect(screen, white, bet100_button)
        bet10_text = button_font.render('$10', True, black)
        bet50_text = button_font.render('$50', True, black)
        bet100_text = button_font.render('$100', True, black)
        screen.blit(bet10_text, (bet10_button.x + (bet10_button.width - bet10_text.get_width()) // 2, bet10_button.y + (bet10_button.height - bet10_text.get_height()) // 2))
        screen.blit(bet50_text, (bet50_button.x + (bet50_button.width - bet50_text.get_width()) // 2, bet50_button.y + (bet50_button.height - bet50_text.get_height()) // 2))
        screen.blit(bet100_text, (bet100_button.x + (bet100_button.width - bet100_text.get_width()) // 2, bet100_button.y + (bet100_button.height - bet100_text.get_height()) // 2))

        # Display balance and bet amount in the betting phase
        balance_text = font.render(f'Balance: ${player_balance}', True, white)
        bet_text = font.render(f'Bet: ${bet_amount}', True, white)
        screen.blit(balance_text, (resolution[0] // 2 - balance_text.get_width() // 2 , 200))
        screen.blit(bet_text, (resolution[0] // 2 - bet_text.get_width() // 2 , 300))

        # Display error message if the bet is more than the balance
        if bet_error_message:
            error_text = font.render(bet_error_message, True, white)
            screen.blit(error_text, (resolution[0] // 2 - error_text.get_width() // 2, 700))
    else:
        screen.fill(green)

        # Draw player cards with overlap
        for i, card in enumerate(player_cards):
            card_image = load_card_image(card)
            card_rect = card_image.get_rect(topleft=(100 + i * 80, 500))  # Adjust position with overlap
            screen.blit(card_image, card_rect)

        # Draw dealer cards with overlap
        for i, card in enumerate(dealer_cards):
            card_image = load_card_image(card)
            if player_turn and i == 0:  # Show one dealer card face down
                card_image = pygame.transform.scale(pygame.image.load('cards/back.png'), (150, 200))
            card_rect = card_image.get_rect(topleft=(100 + i * 80, 100))  # Adjust position with overlap
            screen.blit(card_image, card_rect)

        # Draw game buttons if there is no winner
        if winner is None:
            pygame.draw.rect(screen, white, hit_button)
            pygame.draw.rect(screen, white, stand_button)
            hit_text = button_font.render('Hit', True, black)
            stand_text = button_font.render('Stand', True, black)
            screen.blit(hit_text, (hit_button.x + (hit_button.width - hit_text.get_width()) // 2, hit_button.y + (hit_button.height - hit_text.get_height()) // 2))
            screen.blit(stand_text, (stand_button.x + (stand_button.width - stand_text.get_width()) // 2, stand_button.y + (stand_button.height - stand_text.get_height()) // 2))

        if winner is not None:
            result_text = font.render(winner, True, white)
            screen.blit(result_text, (resolution[0] // 2 - result_text.get_width() // 2, 350))
            pygame.draw.rect(screen, white, next_button)
            next_text = button_font.render('Next', True, black)
            screen.blit(next_text, (next_button.x + (next_button.width - next_text.get_width()) // 2, next_button.y + (next_button.height - next_text.get_height()) // 2))
            pygame.draw.rect(screen, white, leave_button)
            leave_text = button_font.render('Leave Table', True, black)
            screen.blit(leave_text, (leave_button.x + (leave_button.width - leave_text.get_width()) // 2 , leave_button.y + (leave_button.height - leave_text.get_height()) // 2))

        # Display player and dealer scores if show_scores is True
        if show_scores:
            player_hand_value = calculate_hand_value(player_cards)
            dealer_hand_value = calculate_hand_value(dealer_cards, reveal_all=False if player_turn else True)
            player_text = font.render(f'Player: {player_hand_value}', True, white)
            dealer_text = font.render(f'Dealer: {dealer_hand_value}', True, white)
            screen.blit(player_text, (50, 450))
            screen.blit(dealer_text, (50, 50))

        # Draw toggle button for showing/hiding scores
        pygame.draw.rect(screen, white, toggle_button)
        toggle_text = button_font.render('Show Score?', True, black)
        screen.blit(toggle_text, (toggle_button.x + (toggle_button.width - toggle_text.get_width()) // 2, toggle_button.y + (toggle_button.height - toggle_text.get_height()) // 2))

        # Display balance and bet amount in the game phase
        balance_text = font.render(f'Balance: ${player_balance}', True, white)
        bet_text = font.render(f'Bet: ${bet_amount}', True, white)
        screen.blit(balance_text, (650, 50))
        screen.blit(bet_text, (650, 100))

        # Draw the "Peek" button if the dealer's face-up card is 10, J, Q, K, or A and the dealer hasn't peeked yet
        if not dealer_peeked and get_card_value(dealer_cards[1]) in [10, 11]:  # Checking the second card (face-up card)
            pygame.draw.rect(screen, white, peek_button)
            peek_text = button_font.render('Peek', True, black)
            screen.blit(peek_text, (peek_button.x + (peek_button.width - peek_text.get_width()) // 2, peek_button.y + (peek_button.height - peek_text.get_height()) // 2))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
