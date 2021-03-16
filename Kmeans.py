import pygame
import math
from random import randint
from sklearn.cluster import KMeans


# hàm tính khoảng cách giữa các points tới label
p1 = [12,10]
p2 = [8, 5]
def cal_distance(p1,p2):
	return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]) )

# print(cal_distance(p1,p2)) 


pygame.init()

#COLOR 
BACKGROUND = (214, 214, 214)
BLACK = (0, 0, 0)
BACKGROUND_PANEL = (249, 255, 230)
WHITE = (255,255,255)
YELLOW = (255,255,0)
RED = (255,0,0)
LIME = 	(0,255,0)
BLUE = 	(0,0,255)
CYAN = 	(0,255,255)
MAGENTA = 	(255,0,255)
ORANGE  = (255,165,0)
PINK = (255,51,255)
CORAL = (255,127,80)

COLORS = [RED, YELLOW, LIME, BLUE, CYAN, MAGENTA, ORANGE, PINK, CORAL]


def draw_btn(str):
	font = pygame.font.SysFont('sans', 40)
	return font.render(str, True, WHITE)
# btn +
text_plus = draw_btn('+')
# btn -
text_minus = draw_btn('-')
# btn Run
text_run = draw_btn('Run')
# btn Random
text_random = draw_btn('Random')
# btn Algorithm
text_algorithm = draw_btn('Algorithm')
#btn Reset
text_reset = draw_btn('Reset')


screen = pygame.display.set_mode((1100,700))
pygame.display.set_caption("kmeans visualization")
running = True
clock = pygame.time.Clock()
k = 0
error = 0
points = []
clusters = []
labels = []

font = pygame.font.SysFont('sans', 40)
font_small = pygame.font.SysFont('sans', 20)



# font = pygame.font.SysFont('sans', 40)
# text_plus = font.render('+', True, WHITE)


while running:
	clock.tick(60)
	screen.fill(BACKGROUND)
	mouse_x, mouse_y = pygame.mouse.get_pos()


	#DRAW INTERFACE 
	#DRAW PANEL 
	pygame.draw.rect(screen, BLACK, (50, 50, 600, 400))
	pygame.draw.rect(screen, BACKGROUND_PANEL, (55, 55, 590, 390))

	#K BUTTON +
	pygame.draw.rect(screen, BLACK, (700, 50, 50, 50))
	screen.blit(text_plus, (710, 50))

	# BUTTON - 
	pygame.draw.rect(screen, BLACK, (800, 50, 50, 50))
	screen.blit(text_minus, (810, 50))

	# K VALUE
	text_k = font.render('K =' + str(k),True, BLACK)
	screen.blit(text_k, (900, 50))

	# RUN BTN
	pygame.draw.rect(screen, BLACK, (700, 150, 150, 50))
	screen.blit(text_run, (730, 150))

	#RANDOM BTN
	pygame.draw.rect(screen, BLACK, (700, 250, 150, 50))
	screen.blit(text_random, (710, 250))

	#RESET BTN
	pygame.draw.rect(screen, BLACK, (700, 350, 150, 50))
	screen.blit(text_reset, (710, 350))

	# Algorithm button
	pygame.draw.rect(screen, BLACK, (700,350,150,50))
	screen.blit(text_algorithm, (700,350))

	# Error text
	if (clusters != [] and labels != []):
		error = 0
		for i in range(len(points)):
			error += cal_distance(points[i], clusters[labels[i]])
			
	text_error = font.render("Error = " + str(int(error)), True, BLACK)
	screen.blit(text_error, (700,450))

	# Reset button
	pygame.draw.rect(screen, BLACK, (700,550,150,50))
	screen.blit(text_reset, (700,550))

	
	#END DRAW INTERFACE

	# Draw mouse position when mouse is in panel
	if 50 < mouse_x < 650 and 50 < mouse_y < 450:
		text_mouse = font_small.render("(" + str(mouse_x - 50) + "," + str(mouse_y - 50) + ")", True, BLACK)
		screen.blit(text_mouse, (mouse_x + 10, mouse_y))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			#CREATE POINT IN PANEL 
			if 50 < mouse_x < 650 and 50 < mouse_y < 450:
				labels = []
				point = [mouse_x - 50, mouse_y - 50]
				points.append(point)
				# print(points)

			# Change K button +
			if 700 < mouse_x < 750 and 50 < mouse_y < 100:
				if k < len(COLORS):
					k += 1
			# Change K button -
			if 	800 < mouse_x < 850 and 50 < mouse_y < 100:
				if k > 0:
					k -= 1
			# Run BUTTON
			if 700 < mouse_x < 850 and 150 < mouse_y < 200:
				labels = []
				# points = [[196, 141], [192, 240], [192, 240]]
				for p in points:
					distances_to_cluster = []
					# k = 2 --> clusters = [[447, 285], [355, 160]]
					for c in clusters:
						distance = cal_distance(p,c)
						distances_to_cluster.append(distance)
					if(distances_to_cluster != []):
						min_distance = min(distances_to_cluster)
						label = distances_to_cluster.index(min_distance)
						labels.append(label)

				# update new clusters to the central 
				for i in range(len(clusters)):
					sum_x = 0
					sum_y = 0
					count = 0
					for j in range(len(points)):
						# 0 1 2 3 4 = 5 points
						if labels[j] == i: # nếu label màu [j] = cluster màu [i]
							sum_x += points[j][0]
							sum_y += points[j][1]
							count += 1 

					if count != 0:
						new_cluster_x = sum_x / count
						new_cluster_y = sum_y / count
						clusters[i] = [new_cluster_x, new_cluster_y]


			# Random BUTTON
			if 700 < mouse_x < 850 and 250 < mouse_y < 300:
				
				clusters = []
				for i in range(k):
					if k > len(COLORS):
						print('not valid')
					else:
						random_point = [randint(0, 580), randint(0, 380)]
						clusters.append(random_point)
						# print(clusters)
			# Algorithm
			if 700 < mouse_x < 850 and 350 < mouse_y < 400:
				kmeans = KMeans(n_clusters = k ).fit(points)
				labels = kmeans.predict(points)
				clusters = kmeans.cluster_centers_
			# Reset BUTTON
			if 700 < mouse_x < 850 and 550 < mouse_y < 600:
				k = 0
				error = 0
				points = []
				clusters = []
				labels = []
		

		# DRAW  CLUSTER
	for i in range(len(clusters)):
		pygame.draw.circle(screen, COLORS[i], (int(clusters[i][0]) + 50, int(clusters[i][1]) + 50), 10)

		# DRAW POINT 
	for i in range(len(points)):
		pygame.draw.circle(screen,BLACK,(points[i][0] + 50, points[i][1] + 50) , 6)

		if labels == []:
			pygame.draw.circle(screen,WHITE,(points[i][0] + 50, points[i][1] + 50) , 5)
		else:
			pygame.draw.circle(screen,COLORS[labels[i]],(points[i][0] + 50, points[i][1] + 50) , 5)

			
	
	pygame.display.flip()

pygame.quit()