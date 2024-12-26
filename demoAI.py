from dyna import train_dyna_q
import random

def demoAI(player_socket, check_winner, is_draw, algorithm):
    
    print("Starting a game with AI...")
    board = [['' for _ in range(3)] for _ in range(3)]#môi trường
  
    player_symbol = random.choice(['X', 'O'])
    ai_symbol = 'O' if player_symbol == 'X' else 'X'
    
    check_win = 0
    cur_player = "X"

    match algorithm:
        case "DYNA":
            trained_agent = train_dyna_q()
        case _:
            print(f"there is no {algorithm} now")
            return

    try:
        player_socket.send(f"MATCH_FOUND {player_symbol}".encode('utf-8'))  
        while True:
            if cur_player == player_symbol:
                print(f"ai: {ai_symbol} + player: {player_symbol}")
                cur_player = ai_symbol
                data = player_socket.recv(2048).decode('utf-8')
                if not data:
                    print("Player disconnected.")
                    break
                if data.startswith("MOVE"):
                    _, row, col = data.split()
                    row, col = int(row), int(col)

                    if board[row][col] == '':
                        board[row][col] = player_symbol
                        print(f"Player moved to {row}, {col}")
                        player_socket.send(f"VALID_MOVE {row} {col}".encode('utf-8'))


                        if check_winner(board, player_symbol):
                            player_socket.send("WIN".encode('utf-8'))
                            print("Player wins!")
                            check_win = 1
                            
                        elif is_draw(board):
                            player_socket.send("DRAW".encode('utf-8'))
                            print("FFFFFF AI is a draw!")
                            check_win = 1
                    else:
                        player_socket.send("INVALID_MOVE".encode('utf-8'))

                elif data.startswith("REPLAY") :
                    check_win = 0
                    board = [['' for _ in range(3)] for _ in range(3)] 
                    player_symbol = random.choice(['X', 'O'])
                    ai_symbol = 'O' if player_symbol == 'X' else 'X' 
                    cur_player = "X"
                    player_socket.send(f"REPLAY_OK {player_symbol}".encode('utf-8'))  # Thông báo cho người đang chơi                                  
                    print(f"Game  reset for replay.")

                elif data.startswith("SURRENDER") :
                    player_socket.send("LOSE".encode('utf-8'))

            elif cur_player == ai_symbol:
                cur_player = player_symbol
                if check_win == 0:
                    print(f"ai: {ai_symbol} + player: {player_symbol}")
                    
                    available_actions = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
                    move = trained_agent.select_action(board, available_actions)
                    row, col = move
                    board[row][col] = ai_symbol

                    player_socket.send(f"OPPONENT_MOVE {row} {col}".encode('utf-8'))
                    print(f"AI moved to {row}, {col}")
                        

                    if check_winner(board, ai_symbol) :
                        player_socket.send("LOSE".encode('utf-8'))
                        print("AI wins!")

                    elif is_draw(board):
                        player_socket.send("DRAW".encode('utf-8'))
                        print("Game is a draw!")

              
    except Exception as e:
        print(f"Error in demoAI: {e}")
  
