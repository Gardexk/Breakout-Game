import pygame
import sys
import random
import enum

class GameState(enum.Enum):
    HAVENT_PLAYED = 1
    WON = 2
    LOST = 3

pygame.init()
Frame_Clock  = pygame.time.Clock()

Window_Width = 1280
Window_Height = 720
Window = pygame.display.set_mode((Window_Width, Window_Height))
pygame.display.set_caption('Breakout')
font1 = pygame.font.Font(None, 50)

paddle  = pygame.Rect(Window_Width / 2 - 60,  Window_Height - 100, 120,20 )
ball = pygame.Rect(Window_Width/2 - 20, Window_Height/2 - 20, 40, 40)

Menu_Surface = font1.render("Presiona Enter para jugar", False, 'White')
def MenuScreen(State):
    Play_Game = False
    while Play_Game == False:
        Window.fill('Black')
        Window.blit(Menu_Surface, (Window_Width/2 - 200, Window_Height/2 - 50))
        Score_Surface = font1.render(" ", False, 'White')
        if State == GameState.WON:
            Score_Surface = font1.render("¡Ganaste!", False, 'White')
        elif State == GameState.LOST:
            Score_Surface = font1.render("¡Perdiste!", False, 'White')
        Window.blit(Score_Surface, (Window_Width/2 - 200, Window_Height/2 - 150))
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    Play_Game = True
        pygame.display.flip()
        Frame_Clock.tick(60)

def GameLoop ():
    Ball_Speed_X = 5
    Ball_Speed_Y = 5
    Paddle_Speed = 0
    Balls_Left = 3
    Score = 0
    Play_Game = True
    # build the wall to break
    bricks = []
    for y in range(6):
        for x in range(13):
            bricks.append(pygame.Rect(100 * x,  50 * y, 80,30 ))
    ball.x = Window_Width/2 - 20
    ball.y =  Window_Height/2 - 20
    
    while Play_Game == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit Game
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: # if any key is pressed
                if event.key == pygame.K_LEFT:
                    Paddle_Speed -=15
                if event.key == pygame.K_RIGHT:
                    Paddle_Speed +=15
            if event.type == pygame.KEYUP: # if any key is released
                if event.key == pygame.K_LEFT:
                    Paddle_Speed +=15
                if event.key == pygame.K_RIGHT:
                    Paddle_Speed -=15
        paddle.x += Paddle_Speed # move the paddle

        # paddle collider
        if paddle.left <= 0:
            paddle.left = 0
        elif paddle.right >= Window_Width:
            paddle.right = Window_Width

        # ball collider
        if ball.left <= 0:
            ball.left = 0
            Ball_Speed_X *= -1
        elif ball.right >= Window_Width:
            ball.right = Window_Width
            Ball_Speed_X *= -1
        if ball.top <= 0:
            ball.top = 0
            Ball_Speed_Y *= -1
        ball.x += Ball_Speed_X
        ball.y += Ball_Speed_Y

        if ball.colliderect(paddle): # hit ball with paddle
            Ball_Speed_Y *= -1

        for y in bricks: # hit  bricks
            if ball.colliderect(y):
                bricks.remove(y)
                Ball_Speed_Y *= -1
                Score +=1
                if(len(bricks) == 0):
                    State = GameState.WON
                    Play_Game = False

        # if player looses ball   
        if ball.bottom >= Window_Height + 100:
            ball.x = random.randint(200, Window_Width - 200)
            ball.y = Window_Height/2 - 20
            Balls_Left -=1
            if Balls_Left < 0:
                State = GameState.LOST
                Play_Game = False # you loose
            
        Window.fill('Black')
        pygame.draw.rect(Window, 'blue', paddle)
        pygame.draw.ellipse(Window, 'White', ball)


        for brick in bricks:
            if brick.y / 50  <= 1:
                color = 'red'
            elif brick.y / 50 <= 3:
                color = 'green'
            else:
                color = 'orange'
            pygame.draw.rect(Window, color, brick)

        Player_Score_Surface = font1.render("Score: " + str(Score), False, 'White')
        Window.blit(Player_Score_Surface, (Window_Width -  200, Window_Height - 50))
        Balls_Left_Surface = font1.render("Pelotas Restantes: " + str(Balls_Left), False, 'White')
        Window.blit(Balls_Left_Surface, ( 20, Window_Height - 50))
        pygame.display.flip()
        Frame_Clock.tick(60)
    return State

gameState = GameState.HAVENT_PLAYED
while True:
    MenuScreen(gameState)
    gameState = GameLoop()