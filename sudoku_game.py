import pygame 
import random
import time
import re
import sudoku_solver

HEIGHT = 550
WIDTH = 700
background_color = (251, 247, 245)


def format_time(secs):
	sec = secs%60
	minute = secs//60
	hour = minute//60
	return " " + str(minute) + ":" + str(sec)


def show_incorrect(win, incorrect):
	label_font = pygame.font.SysFont("Gadugi", 50)
	str_incorrect = ""
	for i in range(0, incorrect):
		str_incorrect += "X"
	incorrect_label = label_font.render(str_incorrect, True, (255,0,0))
	win.blit(incorrect_label, (50,510))


def clear_time(win):
	cover = pygame.Rect(340,510,300,200)
	pygame.draw.rect(win, background_color, cover)


def show_time(win, play_time):
	clear_time(win)
	label_font = pygame.font.SysFont("Gadugi", 50)
	time_label = label_font.render("Time: " + play_time, True, (0,0,0))
	win.blit(time_label, (340, 510))


def winner(win, board):
	return not any("0" in x for x in board)


def insert(win, position, play_time):
	label_font = pygame.font.SysFont("Gadugi", 50)
	i,j = position[1], position[0]
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.KEYDOWN:
				if board_original[i-1][j-1] != "0":
					return
				if event.key == 48:
					return
				if 0 < event.key - 48 < 10:
					if not sudoku_solver.valid(board, event.key-48, (i-1,j-1)):
						value = label_font.render(str(event.key - 48), True, (255,0,0))
						win.blit(value, (position[0]*50+15, position[1]*50+10))
						pygame.display.update()
						pygame.time.delay(1000)
						win.fill(background_color)
						draw_board(win, board,play_time)
						global incorrect
						incorrect += 1
						show_incorrect(win, incorrect)
						if incorrect == 5:
							lose_rect = pygame.Rect(0,0, 525,550)
							pygame.draw.rect(win, background_color, lose_rect)
							lose_label = label_font.render("You Lose!", True, (0,0,0))
							win.blit(lose_label, (157, 100))
							
							draw_high_scores(win)
							global no_time
							no_time = True
						return
					value = label_font.render(str(event.key - 48), True, (0,0,139))
					win.blit(value, (position[0]*50+15, position[1]*50+10))
					board[i-1][j-1] = event.key-48
					pygame.display.update()
					return

def draw_high_scores(win):
	label_font = pygame.font.SysFont("Gadugi", 50)
	hs_label = label_font.render("High Scores", True, (0,0,0))
	win.blit(hs_label, (150,200))
	hs_font = pygame.font.SysFont("Gadugi", 35)
	top5 = sudoku_solver.get_high_scores("high_scores.txt")
	for i in range(0,len(top5)):
		high_scores = hs_font.render(top5[i][0]+": "+top5[i][1].strip(), True, (0,0,139))
		win.blit(high_scores,(200,250+i*50))


def draw_menu(win, board):
	mouse = pygame.mouse.get_pos()
	label_font = pygame.font.SysFont("Gadugi", 50)
	sudoku_label = label_font.render("Sudoku", True, (0,0,0))
	win.blit(sudoku_label, (535,100))
	small_font = pygame.font.SysFont('Arial', 20)
		
	new_game = small_font.render('New Game', True, (0,0,0))
	ng_button = pygame.Rect(540,200,120,30)

	if 540 <= mouse[0] <= 660 and 200 <= mouse[1] < 230:
		pygame.draw.rect(win, [153,204,255], ng_button)
	else: 
		pygame.draw.rect(win, background_color, ng_button)
	win.blit(new_game, (550, 207))

	return ng_button



def draw_board(win, board, play_time):
	win.fill(background_color)
	label_font = pygame.font.SysFont("Gadugi", 50)

	for i in range(0, 10):
		if i%3 == 0:
			pygame.draw.line(win, (0,0,0), (50+50*i, 50), (50+50*i, 500), 4)
			pygame.draw.line(win, (0,0,0), (50, 50+50*i), (500, 50+50*i), 4)

		pygame.draw.line(win, (0,0,0), (50+50*i, 50), (50+50*i, 500), 2)
		pygame.draw.line(win, (0,0,0), (50, 50+50*i), (500, 50+50*i), 2)
	pygame.display.update()

	for i in range(0, len(board[0])):
		for j in range(0, len(board[0])):
			if 0 < int(board[i][j]) < 10:
				if board_original[i][j] == "0":
					value = label_font.render(str(board[i][j]), True, (0,0,139))
				else:
					value = label_font.render(str(board[i][j]), True, (0,0,0))
				win.blit(value, (65+50*j, 60+50*i))
	show_time(win, play_time)
	show_incorrect(win, incorrect)


def draw_win_board(win, board, time_completed):
	win_rect = pygame.Rect(0,0, 525,550)
	pygame.draw.rect(win, background_color, win_rect)
	label_font = pygame.font.SysFont("Gadugi", 50)

	str_final_time = "It took you " + format_time(time_completed)
	time_label = label_font.render(str_final_time, True, (0,0,0))
	win.blit(time_label, (150, 115))
	won_label = label_font.render("You win!", True, (0,0,0))
	win.blit(won_label, (200,75))
	draw_high_scores(win)


def check_score(win, time_completed, high_scores):
	time = format_time(time_completed)
	t_mid = (re.search(":", time)).start()
	min_time = time[:t_mid]
	sec_time = time[t_mid+1:]
	for i in range(0,len(high_scores)):
		score = high_scores[i][1]
		mid = (re.search(":", score)).start()
		minute = int(score[:mid])
		second = int(score[mid + 1:].strip())
		if int(min_time) < int(minute):
			return sudoku_solver.update_high_score("high_scores.txt", time, high_scores, i)
		elif int(min_time) == minute:
			if int(sec_time) < second:
				return sudoku_solver.update_high_score("high_scores.txt", time, high_scores, i)
	return high_scores


def main():
	pygame.init()
	win = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Sudoku")
	win.fill(background_color)
	start = time.time()

	global board
	draw_board(win, board, "0")
	global no_time
	global paused
	global incorrect
	while True:
		play_time = round(time.time() - start)
		time_display = format_time(play_time)
		ng_button = draw_menu(win, board)
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = event.pos
				if ng_button.collidepoint(mouse_pos):
					global board_original
					board_original = sudoku_solver.get_rand_board("input.in")
					board = [row[:] for row in board_original]
					win.fill(background_color)
					draw_board(win, board, format_time(play_time))
					no_time = False
					incorrect = 0 
					paused = False
					main()
				else: 
					insert(win, (mouse_pos[0]//50, mouse_pos[1]//50), time_display)
					if winner(win, board):
						time_completed = round(time.time() - start)
						highscores = sudoku_solver.get_high_scores("high_scores.txt")
						win.fill(background_color)
						new_hs = check_score(win, time_completed, highscores)
						
						draw_win_board(win, board, time_completed)
						draw_menu(win,board)
						no_time = True
		if not no_time:
			show_time(win, time_display)


board_original = sudoku_solver.get_rand_board("input.in")
board = [row[:] for row in board_original]
incorrect = 0
paused = False
no_time = False
main()
