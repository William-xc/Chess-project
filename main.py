#a 2 player chess game in python using python using pygame

import pygame

pygame.init()
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("2 player chess game")
font = pygame.font.Font('freesansbold.ttf' , 20)
big_font = pygame.font.Font('freesansbold.ttf', 50)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
timer = pygame.time.Clock()
fps = 60

#game variables and images
white_pieces = ['rook', 'knight' , 'bishop' , 'king' , 'queen' , 'bishop' , 'knight' , 'rook',
                'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']
#the board goes from 0 - 7 for the rows and columns 
white_pieces_location = [(0,0) , (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                         (0,1) , (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]


black_pieces = ['rook', 'knight' , 'bishop' , 'king' , 'queen' , 'bishop' , 'knight' , 'rook',
                'pawn','pawn','pawn','pawn','pawn','pawn','pawn','pawn']
black_pieces_location = [(0,7) , (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                         (0,6) , (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6)]

captured_white_pieces = []
captured_black_pieces = []

#0 = white turn but no selected piece , 1- white turn pieces selected, 2-black turn but no selected pieces, 3- black turn pieces selected 

#turn_step is used to keep track which phase we are in 
turn_step = 0
selection = 100 # which pieces is being selected, when no piece is selected you it will default on 100

valid_moves = []

#load in game piece images [q, k, r, k, p]
black_queen = pygame.image.load('images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (80,80))
black_queen_small = pygame.transform.scale(black_queen, (45,45))
black_king = pygame.image.load('images/black king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load('images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load('images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load('images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load('images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load('images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load('images/white king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load('images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load('images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load('images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load('images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

#draw the pieces on the board
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small, white_rook_small, white_bishop_small]

black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small, black_rook_small, black_bishop_small]


piece_list = ['pawn', 'queen' , 'king' , 'knight', 'rook' , 'bishop']

#check variables
counter = 0
winner = ''
game_over = False
 

#draw main game chess board
def draw_board():
    for i in range(32):
        column = i % 4 # 0, 1, 2, 3
        row = i // 4 
        if row%2 == 0: # if the row is even
            pygame.draw.rect(screen, 'light grey', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light grey', [700 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'gold', [0,800, WIDTH, 100],5) # where the captured pieces will be 
        pygame.draw.rect(screen, 'gold', [800,0, 200, HEIGHT],5)# where the captured pieces will be

        status_text = ['White: Select a piece to move', 'White: choose square',
                       'Black: Select a piece to move', 'Black: choose square']

        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20,820))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0,100*i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100*i, 0), (100*i, 800), 2)
        screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))


#draw pieces on the board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn': # just for pawns as they are smaller than other pieces
            screen.blit(white_pawn, (white_pieces_location[i][0] * 100 + 22, white_pieces_location[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index], (white_pieces_location[i][0] * 100 + 10, white_pieces_location[i][1] * 100 +10))

        if turn_step < 2:# it is whites turn 
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_pieces_location[i][0] * 100 + 1, white_pieces_location[i][1] * 100 + 1, 100,100],2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn': # just for pawns as they are smaller than other pieces
            screen.blit(black_pawn, (black_pieces_location[i][0] * 100 + 22, black_pieces_location[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index], (black_pieces_location[i][0] * 100 + 10, black_pieces_location[i][1] * 100 + 10))

        if turn_step >= 2:# it is black turn 
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_pieces_location[i][0] * 100 + 1, black_pieces_location[i][1] * 100 + 1, 100,100],2)
        
        
#check all pieces valid options on board
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list  = check_pawn(location, turn )
        
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        
        elif piece == 'knight':
            moves_list = check_knight(location, turn )
        
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn )
        
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        
        elif piece == 'king':
            moves_list = check_king(location, turn )

        
        all_moves_list.append(moves_list)
    return all_moves_list
      
#check queen valid moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_moves_list = check_rook(position, color)

    for i in range(len(second_moves_list)):
        moves_list.append(second_moves_list[i])

    return moves_list

#check king valid moves
def check_king(position, color):
    moves_list  = []
    if color == 'white':
         enemies_list = black_pieces_location
         friends_list = white_pieces_location
    else: # black
        enemies_list = white_pieces_location
        friends_list = black_pieces_location
    #8 possible moves
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)


    return moves_list


#check valid rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
         enemies_list = black_pieces_location
         friends_list = white_pieces_location
    else: # black
        enemies_list = white_pieces_location
        friends_list = black_pieces_location

    for i in range(4): #down(0),up(1), right(2), left(3) 
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0

        while path:
            #checks the valid move for the rook, and the rook is able to go in the right direction. it either has a friend, enemy, or end of board from the top, bottom, right or left
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and 0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

#check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
         enemies_list = black_pieces_location
         friends_list = white_pieces_location
    else: # black
        enemies_list = white_pieces_location
        friends_list = black_pieces_location
    #8 square to check for
    
    targets = [(1,2), (1,-2), (2,1), (2,-1), (-1,2), (-1,-2), (-2,1) , (-2,-1)] 
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1]) #check the target moves that the knight can go to from CURRENT position
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:#as long as it is within the board and not on a friend, append it
            moves_list.append(target)

    return moves_list

#check valid bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
         enemies_list = black_pieces_location
         friends_list = white_pieces_location
    else: # black
        enemies_list = white_pieces_location
        friends_list = black_pieces_location

    for i in range(4): #up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and 0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain*y)))
                if (position[0] + (chain*x), position[1] + (chain*y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


#Check valid pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_pieces_location and (position[0], position[1] + 1) not in black_pieces_location and position[1] < 7:
            moves_list.append((position[0], position[1] + 1)) # can you go one square up as a pawn 

        if (position[0], position[1] + 2) not in white_pieces_location and (position[0], position[1] + 2) not in black_pieces_location and position[1] == 1:
            moves_list.append((position[0], position[1] + 2)) #can you go up 2 squares in the begining of the game 
        
        if(position[0] + 1, position[1] + 1) in black_pieces_location: # right attack from pawn
            moves_list.append((position[0]+1, position[1] + 1))

        if(position[0] - 1, position[1] + 1) in black_pieces_location: # left attack from pawn
            moves_list.append((position[0] -1, position[1] + 1))


    if color == 'black':
        if (position[0], position[1] - 1) not in white_pieces_location and (position[0], position[1] - 1) not in black_pieces_location and position[1] > 0:
            moves_list.append((position[0], position[1] - 1)) # can you go one square up as a pawn 

        if (position[0], position[1] - 2) not in white_pieces_location and (position[0], position[1] - 2) not in black_pieces_location and position[1] == 6:
            moves_list.append((position[0], position[1] - 2)) #can you go up 2 squares in the begining of the game 
        
        if(position[0] + 1, position[1] - 1) in white_pieces_location: # right attack from pawn
            moves_list.append((position[0]+1, position[1] - 1))

        if(position[0] - 1, position[1] - 1) in white_pieces_location: # left attack from pawn
            moves_list.append((position[0] -1, position[1] - 1))
    return moves_list


#check for valid moves for selected piece
def check_valid_moves():
    if turn_step < 2: # white turn
        options_list = white_options

    else: # black turn 
        options_list = black_options

    valid_options = options_list[selection]
    return valid_options



#draw valid moves on the screen
def draw_valid(moves):
    if turn_step < 2: #white
        color = 'red'
    else: #black 
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50),5)

        
#draw captured pieces
def draw_captured():
    for i in range(len(captured_white_pieces)):
        captured_piece = captured_white_pieces[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825,5 + 50*i))

    for i in range(len(captured_black_pieces)):
        captured_piece = captured_black_pieces[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925,5 + 50*i))

#check and draw a flashing sqaure around king if in check
def draw_check():
    #checked = False
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_pieces_location[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_pieces_location[king_index][0] * 100 + 1, white_pieces_location[king_index][1] * 100 + 1, 100,100], 5)

    else:
         if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_pieces_location[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_pieces_location[king_index][0] * 100 + 1, black_pieces_location[king_index][1] * 100 + 1, 100, 100], 5)

def draw_game_over():
    pygame.draw.rect(screen, 'black', [200,200,400,50])
    screen.blit(font.render(f'{winner} won the game!', True, 'white' ),(210,210))
    screen.blit(font.render(f'press ENTER to restart', True, 'white' ),(210,240))












#main game loop
black_options = check_options(black_pieces, black_pieces_location, 'black')
white_options = check_options(white_pieces, white_pieces_location, 'white')
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()

    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    #any event that happens(when you move the pieces with your mouse or with the keyboard)
    #event handling 
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: #if you exit it out of the game(the little red x in the top right corner)
            run = False # close the game
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over: #it is a left mouse click 

            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            if turn_step < 2:#white player
                if click_coords == (8,8) or click_coords == (9,8):
                    winner = 'black'
                if click_coords in white_pieces_location:
                    selection = white_pieces_location.index(click_coords)

                    if turn_step == 0:#white player has selected a piece
                        turn_step = 1

                if click_coords in valid_moves and selection != 100:
                    white_pieces_location[selection] = click_coords
                    if click_coords in black_pieces_location:
                        black_piece = black_pieces_location.index(click_coords)
                        captured_white_pieces.append(black_pieces[black_piece])

                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_pieces_location.pop(black_piece)

                    black_options = check_options(black_pieces, black_pieces_location, 'black')

                    white_options = check_options(white_pieces, white_pieces_location, 'white')

                    turn_step = 2
                    selection = 100
                    valid_moves = []

            if turn_step > 1:#black player
                if click_coords == (8,8) or click_coords == (9,8):
                    winner = 'white'
                if click_coords in black_pieces_location:
                    selection = black_pieces_location.index(click_coords)

                    if turn_step == 2:#black player has selected a piece
                        turn_step = 3

                if click_coords in valid_moves and selection != 100:
                    black_pieces_location[selection] = click_coords
                    if click_coords in white_pieces_location:
                        white_piece = white_pieces_location.index(click_coords)
                        captured_black_pieces.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_pieces_location.pop(white_piece)

                    black_options = check_options(black_pieces, black_pieces_location, 'black')

                    white_options = check_options(white_pieces, white_pieces_location, 'white')
                    
                    turn_step = 0
                    selection = 100
                    valid_moves = []
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_pieces_location = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_pieces_location = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_pieces_location, 'black')
                white_options = check_options(white_pieces, white_pieces_location, 'white')

    
    
    
    
    
    
    
    
    if winner != '':
            game_over = True
            draw_game_over()





    
    pygame.display.flip() #display the game and the changes that have happened
pygame.quit




