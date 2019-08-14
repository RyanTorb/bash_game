import pygame
import gamebox

camera = gamebox.Camera(800, 500)
floor = gamebox.from_color(400, 400, "green", 500, 40)
game_on = 0

start_screen = [gamebox.from_text(400, 100, "Bash Bros: A Poorly Made Knock-off", "arial", 30, "red", True),
                gamebox.from_color(400, 220, "yellow", 150, 60), gamebox.from_color(400, 340, "yellow", 150, 60),
                gamebox.from_text(400, 220, 'Single Player', 'arial', 18, 'black', True),
                gamebox.from_text(400, 340, 'Two Player', 'arial', 18, 'black', True),
                gamebox.from_text(400, 480, "Game made by Ryan Torbic. All ideas are basically taken from Nintendo, "
                                            "but considering that there's been tons of derivatives of the Smash Bros "
                                            "franchise, nobody's going to begrudge me this.", "arial", 8, "white")]

choice_screen = [gamebox.from_text(400, 100, "Player One: Choose Your Character", 'arial', 24, 'black', True),
                 gamebox.from_text(400, 100, "Choose Your Character", 'arial', 24, 'black', True),
                 gamebox.from_image(200, 300, 'Red_test.png'), gamebox.from_image(600, 300, 'Green_test.png')]

item_screen = [gamebox.from_text(400, 450, "Warning: All of Two-Player is non-functional as of yet", 'arial', 18, 'black', True),
               gamebox.from_text(400, 100, "Items:", 'arial', 30, 'black', True),
               gamebox.from_color(200, 300, 'yellow', 150, 60), gamebox.from_color(600, 300, 'yellow', 150, 60),
               gamebox.from_text(200, 300, "ON", 'arial', 18, 'black',True),
               gamebox.from_text(600, 300, 'OFF', 'arial', 18, 'black', True)]

hearts_one = [gamebox.from_image(20, 20, 'Heart.gif'), gamebox.from_image(50, 20, 'Heart.gif'),
              gamebox.from_image(80, 20, 'Heart.gif'), gamebox.from_image(110, 20, 'Heart.gif'),
              gamebox.from_image(140, 20, 'Heart.gif')]

hearts_two = [gamebox.from_image(780, 20, 'Heart.gif'), gamebox.from_image(750, 20, 'Heart.gif'),
              gamebox.from_image(720, 20, 'Heart.gif'), gamebox.from_image(690, 20, 'Heart.gif'),
              gamebox.from_image(660, 20, 'Heart.gif')]

still_red = gamebox.from_image(200, 200, 'Red_test.png')
still_green = gamebox.from_image(600, 200, 'Green_test.png')
punch_red = gamebox.from_image(200, 200, 'Red_arms_test.png')
punch_green = gamebox.from_image(600, 200, 'Green_arms_test.png')

right_boundary = gamebox.from_color(-50, 250, "navy", 20, 620)
left_boundary = gamebox.from_color(850, 250, "navy", 20, 620)
bottom_boundary = gamebox.from_color(400, 550, 'navy', 880, 20)

grow = gamebox.from_color(400, 100, 'orange', 20, 20)

player_one = ""
player_two = ""
enemy = ""
punchman = ""
punchman_one = ""
punchman_two = ""
enemy_punchman = ""
lives_one = 5
lives_two = 5
winner = ""
counter = 0
timer = 0
enemy_p = False
items = False


def tick(keys):
    global game_on, player_one, player_two, enemy, punchman, punchman_one, punchman_two, \
        lives_one, lives_two, winner, counter, enemy_punchman, enemy_p, items, item_screen, items_obj, grow, timer
    camera.clear("light blue")

    if game_on == 0:
        for i in range(len(start_screen)):
            camera.draw(start_screen[i])
        if camera.mouseclick:
            x, y = camera.mouse
            if start_screen[3].contains(x, y):
                game_on = 2
            if start_screen[4].contains(x, y):
                game_on = 5

    if game_on == 2:
        for i in range(1, len(item_screen)):
            camera.draw(item_screen[i])
        if camera.mouseclick:
            x, y = camera.mouse
            if item_screen[4].contains(x, y):
                items = True
                game_on = 3
            if item_screen[5].contains(x, y):
                items = False
                game_on = 3


    # one player choice
    if game_on == 3:
        for i in range(1, len(choice_screen)):
            camera.draw(choice_screen[i])
        if camera.mouseclick:
            x, y = camera.mouse
            if choice_screen[2].contains(x, y):
                player_one = still_red
                punchman = punch_red
                enemy = still_green
                enemy_punchman = punch_green
                player_one.center = [200, 100]
                enemy.center = [600, 100]
                camera.draw(gamebox.from_text(400, 400, "Press Space to Start", "arial", 24, 'black', True))
                if pygame.K_SPACE in keys:
                    game_on = 4
                    timer = 0
                    counter = 0
            if choice_screen[3].contains(x, y):
                player_one = still_green
                punchman = punch_green
                enemy = still_red
                enemy_punchman = punch_red
                player_one.center = [200, 100]
                enemy.center = [600, 100]
                camera.draw(gamebox.from_text(400, 400, "Press Space to Start", "arial", 24, 'black', True))
                if pygame.K_SPACE in keys:
                    game_on = 4
                    timer = 0
                    counter = 0

    # one player game
    if game_on == 4:
        camera.draw(floor)
        if pygame.K_SPACE not in keys:
            camera.draw(player_one)
            if enemy_p and player_one.x >= 400 and enemy_punchman.touches(player_one):
                player_one.speedx += .4
            if enemy_p and player_one.x < 400 and enemy_punchman.touches(player_one):
                player_one.speedx -= .4
        elif pygame.K_SPACE in keys:
            camera.draw(punchman)
            if punchman.touches(enemy) and enemy.x >= 400 and not enemy_p:
                enemy.speedx += .4
            elif punchman.touches(enemy) and enemy.x < 400 and not enemy_p:
                enemy.speedx -= .4
            if enemy_p and punchman.touches(enemy_punchman) and player_one.touches(floor) and enemy.touches(floor):
                player_one.speedy -= 8
                enemy.speedy -= 8
        camera.draw(enemy)
        if player_one.touches(floor):
            player_one.move_to_stop_overlapping(floor)
            if pygame.K_UP in keys:
                player_one.speedy -= 8
        if enemy.touches(floor):
            enemy.move_to_stop_overlapping(floor)
        if player_one.speedx != 0 and not player_one.touches(enemy_punchman):
            if pygame.K_RIGHT in keys:
                player_one.speedx += .15
            if pygame.K_LEFT in keys:
                player_one.speedx -= .15
        if player_one.speedx == 0 and not player_one.touches(enemy_punchman):
            player_one.speedx = 0
        player_one.speedy += .3
        enemy.speedy += .3
        if pygame.K_RIGHT in keys:
            player_one.x += 3
        if pygame.K_LEFT in keys:
            player_one.x -= 3
        if player_one.touches(bottom_boundary) or player_one.touches(right_boundary) or \
                player_one.touches(left_boundary):
            player_one.center = [400, 100]
            player_one.speedy = 0
            player_one.speedx = 0
            lives_one -= 1
        if enemy.touches(bottom_boundary) or enemy.touches(right_boundary) or \
                enemy.touches(left_boundary):
            enemy.center = [400, 100]
            enemy.speedy = 0
            enemy.speedx = 0
            lives_two -= 1
        if lives_one == 5:
            for i in range(len(hearts_one)):
                camera.draw(hearts_one[i])
        if lives_one == 4:
            for i in range(len(hearts_one) - 1):
                camera.draw(hearts_one[i])
        if lives_one == 3:
            for i in range(len(hearts_one) - 2):
                camera.draw(hearts_one[i])
        if lives_one == 2:
            for i in range(len(hearts_one) - 3):
                camera.draw(hearts_one[i])
        if lives_one == 1:
            for i in range(len(hearts_one) - 4):
                camera.draw(hearts_one[i])
        if lives_one == 0:
            winner = "CPU Wins!"
            game_on = 8
        if lives_two == 5:
            for i in range(len(hearts_two)):
                camera.draw(hearts_two[i])
        if lives_two == 4:
            for i in range(len(hearts_two) - 1):
                camera.draw(hearts_two[i])
        if lives_two == 3:
            for i in range(len(hearts_two) - 2):
                camera.draw(hearts_two[i])
        if lives_two == 2:
            for i in range(len(hearts_two) - 3):
                camera.draw(hearts_two[i])
        if lives_two == 1:
            for i in range(len(hearts_two) - 4):
                camera.draw(hearts_two[i])
        if lives_two == 0:
            winner = "Player One Wins!"
            game_on = 8

        # Finished CPU controls
        if counter < 90:
            camera.draw(enemy_punchman)
            enemy_p = True
        if 90 < counter < 210:
            enemy_p = False
        if counter > 210:
            counter = 0
        enemy.speedx -= .001 * (enemy.x - 400)
        if enemy.x > 580 and enemy.touches(floor) or enemy.x < 220 and enemy.touches(floor):
            enemy.speedy -= 8

        #Items stuff (unfinished)
        if items:

            if timer >= 180:
                camera.draw(grow)
            if timer >= 360:
                grow.speedy += .3
            if grow.touches(floor):
                grow.move_to_stop_overlapping(floor)
                grow.speedy = 0


        grow.x += grow.speedx
        grow.y += grow.speedy
        enemy.x += enemy.speedx
        enemy.y += enemy.speedy
        player_one.x += player_one.speedx
        player_one.y += player_one.speedy
        punchman.x = player_one.x
        punchman.y = player_one.y
        enemy_punchman.x = enemy.x
        enemy_punchman.y = enemy.y

    if game_on == 5:
        for i in range(len(item_screen)):
            camera.draw(item_screen[i])
        if camera.mouseclick:
            x, y = camera.mouse
            if item_screen[4].contains(x, y):
                game_on = 6
            if item_screen[5].contains(x, y):
                game_on = 6


    # two player choice
    if game_on == 6:
        camera.draw(choice_screen[0])
        for i in range(2, len(choice_screen)):
            camera.draw(choice_screen[i])
        if camera.mouseclick:
            x, y = camera.mouse
            if choice_screen[2].contains(x, y):
                player_one = still_red
                punchman_one = punch_red
                player_two = still_green
                punchman_two = punch_green
                camera.draw(gamebox.from_text(400, 400, "Press Space to Start", "arial", 24, 'black', True))
                if pygame.K_SPACE in keys:
                    game_on = 7
            if choice_screen[3].contains(x, y):
                player_one = still_green
                punchman_one = punch_green
                player_two = still_red
                punchman_two = punch_red
                camera.draw(gamebox.from_text(400, 400, "Press Space to Start", "arial", 24, 'black', True))
                if pygame.K_SPACE in keys:
                    game_on = 7

    # two player game
    if game_on == 7:
        camera.draw(floor)
        if pygame.K_SPACE not in keys:
            camera.draw(player_two)
        elif pygame.K_SPACE in keys:
            camera.draw(punchman_two)
        if pygame.K_v not in keys:
            camera.draw(player_one)
        elif pygame.K_v in keys:
            camera.draw(punchman_one)
            if punchman_one.touches(player_two) and player_two.x >= 400:
                player_two.speedx += 12
            elif punchman_one.touches(player_two) and player_two.x < 400:
                player_two.speedx -= 12
        if player_one.touches(floor):
            player_one.move_to_stop_overlapping(floor)
            if pygame.K_w in keys:
                player_one.speedy -= 8
        if player_two.touches(floor):
            player_two.move_to_stop_overlapping(floor)
            if pygame.K_UP in keys:
                player_two.speedy -= 8
        player_one.speedy += .3
        player_two.speedy += .3
        if pygame.K_d in keys:
            player_one.x += 3
        if pygame.K_a in keys:
            player_one.x -= 3
        if pygame.K_RIGHT in keys:
            player_two.x += 3
        if pygame.K_LEFT in keys:
            player_two.x -= 3
        if player_one.touches(bottom_boundary) or player_one.touches(right_boundary) or \
                player_one.touches(left_boundary):
            player_one.center = [400, 100]
            player_one.speedx = 0
            player_one.speedy = 0
            lives_one -= 1
        if player_two.touches(bottom_boundary) or player_two.touches(right_boundary) or \
                player_two.touches(left_boundary):
            player_two.center = [400, 100]
            player_two.speedx = 0
            player_two.speedy = 0
            lives_two -= 1
        if lives_one == 5:
            for i in range(len(hearts_one)):
                camera.draw(hearts_one[i])
        if lives_one == 4:
            for i in range(len(hearts_one) - 1):
                camera.draw(hearts_one[i])
        if lives_one == 3:
            for i in range(len(hearts_one) - 2):
                camera.draw(hearts_one[i])
        if lives_one == 2:
            for i in range(len(hearts_one) - 3):
                camera.draw(hearts_one[i])
        if lives_one == 1:
            for i in range(len(hearts_one) - 4):
                camera.draw(hearts_one[i])
        if lives_one == 0:
            winner = "Player Two Wins!"
            game_on = 8
        if lives_two == 5:
            for i in range(len(hearts_two)):
                camera.draw(hearts_two[i])
        if lives_two == 4:
            for i in range(len(hearts_two) - 1):
                camera.draw(hearts_two[i])
        if lives_two == 3:
            for i in range(len(hearts_two) - 2):
                camera.draw(hearts_two[i])
        if lives_two == 2:
            for i in range(len(hearts_two) - 3):
                camera.draw(hearts_two[i])
        if lives_two == 1:
            for i in range(len(hearts_two) - 4):
                camera.draw(hearts_two[i])
        if lives_two == 0:
            winner = "Player One Wins!"
            game_on = 8
        player_one.x += player_one.speedx
        player_two.x += player_two.speedx
        player_two.y += player_two.speedy
        player_one.y += player_one.speedy
        punchman_one.x = player_one.x
        punchman_one.y = player_one.y
        punchman_two.x = player_two.x
        punchman_two.y = player_two.y

    if game_on == 8:
        camera.draw(gamebox.from_text(400, 180, winner, 'arial', 36, 'black', True))
        camera.draw(gamebox.from_text(400, 220, "Press B to go to Start Screen", 'arial', 24, 'black', True))
        if pygame.K_b in keys:
            lives_one = 5
            lives_two = 5
            game_on = 0

    counter += 1
    timer += 1
    camera.display()


ticks_per_second = 60

gamebox.timer_loop(ticks_per_second, tick)
