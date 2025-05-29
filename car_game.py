#Thu vien
import pygame
from pygame.locals import *
import random
pygame.init()
#Mau nen
gray = (100,100,100)
green = (76,208,56)
yellow = (255,232,0)
red = (200,0,0)
white = (255,255,255)
#Tao cua so game
width = 500
height = 500
screen_size = (width, height)
#ve cua so game
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Game dua xe')
#Khởi tạo biến
Gameover = False
speed=1
score=0
#duong xe chay
road_width = 300 #do rong duong xe chay
#vach ke duong
market_width = 10
market_height = 50
#lane duong
lane_left = 150
lane_center = 250
lane_right = 350
lanes = [lane_left, lane_center, lane_right]
lane_move_y = 0

#Road and edge
road = (100,0,road_width,height)
#duong mau vang trong giao dien game
left_edge = (95,0,market_width,height)
right_edge = (395,0,market_width,height)

#vi tri ban dau xe cua nguoi choi
player_x = 250
player_y = 400

#cai dat fps
clock = pygame.time.Clock()
fps = 120

#doi tuong chuong ngai vat (vehicle)
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        #chinh kich thuoc xe 
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_heigh = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image,(new_width,new_heigh))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

#doi tuong xe cua nguoi choi
class playerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image,x,y)

#sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()
#tao xe nguoi choi (dong 95)
player = playerVehicle(player_x, player_y)
player_group.add(player)

#load xe luu thong
image_name = ['car1.png','car2.png','car3.png','car4.png']
vehicle_images = []
for name in image_name:
    image = pygame.image.load('images/' + name)
    vehicle_images.append(image)

#load hinh va cham
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

#vong lap xu ly game
running = True
while running:
    #Chinh frame hinh tren giay
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        #dieu khien xe
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0]> lane_left:
                player.rect.x -= 100
            if event.key == K_RIGHT and player.rect.center[0]< lane_right:
                player.rect.x += 100
            
            #check va cham khi dieu khien
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    Gameover = True

    #chekc va cham khi xe dung yen
    if pygame.sprite.spritecollide(player,vehicle_group,True):
        Gameover = True
        crash_rect.center = [player.rect.center[0],player.rect.top]

    #ve dia hinh co
    screen.fill(green)

    #ve duong chay
    pygame.draw.rect(screen, gray, road)

    #ve edge- hanh lang duong
    pygame.draw.rect(screen, yellow, left_edge)
    pygame.draw.rect(screen, yellow, right_edge)

    #ve lane duong
    lane_move_y+=speed * 2
    if lane_move_y >= market_height * 2:
        lane_move_y = 0
    for y in range (market_height* -2, height,market_height*2):
        pygame.draw.rect(screen, white,(lane_left + 45, y + lane_move_y, market_width, market_height))
        pygame.draw.rect(screen, white,(lane_center + 45, y + lane_move_y, market_width, market_height))

        #ve xe player
        player_group.draw(screen)

        #ve phuong tien giao thong
        if len(vehicle_group) < 2 :
            add_vehicle = True
            for vehicle in vehicle_group:
                if vehicle.rect.top < vehicle.rect.height * 1.5:
                    add_vehicle = False
            if add_vehicle:
                lane = random.choice(lanes)
                image = random.choice(vehicle_images)
                vehicle = Vehicle(image,lane,height/-2)
                vehicle_group.add(vehicle)
 

        # cho chuong ngai vat chay
        for vehicle in vehicle_group:
            vehicle.rect.y += speed

            #Remove vehicle
            if vehicle.rect.top >= height:
                vehicle.kill()
                score +=1
                # #tang toc do chay
                # if score > 0 and score % 10 ==0:
                #     speed += 1 
        #ve nhom xe luu thong
        vehicle_group.draw(screen)

        #hien thi diem
        font = pygame.font.Font(pygame.font.get_default_font(),16)
        text = font.render(f'Score: {score}', True, white)
        text_rect = text.get_rect()
        text_rect.center= (50,40)
        screen.blit(text, text_rect)
        if Gameover:
            screen.blit(crash,crash_rect)

            #hien thi choi tiep hay ko
            pygame.draw.rect(screen,red,(0,50,width,100))
            font = pygame.font.Font(pygame.font.get_default_font(),16)
            text = font.render(f'Game over! Play again? (Y / N)', True, white)
            text_rect = text.get_rect()
            text_rect.center= (width/2,100)
            screen.blit(text, text_rect)

    pygame.display.update()
    while Gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                Gameover =False
                running = False
            if event.type == KEYDOWN:
                if event.key == K_y:
                    #resetgame
                    Gameover= False
                    score = 0
                    speed = 1
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # exit game
                    Gameover = False
                    running = False

pygame.quit()