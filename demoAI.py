def demoAI(player_socket, check_winner, is_draw):
    print("Starting a game with AI...")
    board = [['' for _ in range(3)] for _ in range(3)]#môi trường
    ai_symbol = 'O'
    player_symbol = 'X'

    try:
        player_socket.send("MATCH_FOUND X".encode('utf-8'))  
        while True:

            print("Waiting for player's move...")
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
                        break
                    elif is_draw(board):
                        player_socket.send("DRAW".encode('utf-8'))
                        print("Game is a draw!")
                        break
   
                    #AI đi, thêm code AI vào đoạn này
                    move_made = False
                    for i in range(3):
                        for j in range(3):
                            if board[i][j] == '':
                                board[i][j] = ai_symbol
                                player_socket.send(f"OPPONENT_MOVE {i} {j}".encode('utf-8'))
                                print(f"AI moved to {i}, {j}")
                                move_made = True
                                break
                        if move_made:
                            break

                    if check_winner(board, ai_symbol):
                        player_socket.send("LOSE".encode('utf-8'))
                        print("AI wins!")
                        break
                    elif is_draw(board):
                        player_socket.send("DRAW".encode('utf-8'))
                        print("Game is a draw!")
                        break
                else:
                    player_socket.send("INVALID_MOVE".encode('utf-8'))
    except Exception as e:
        print(f"Error in demoAI: {e}")
    finally:
        player_socket.close()
        print("Game with AI ended.")
