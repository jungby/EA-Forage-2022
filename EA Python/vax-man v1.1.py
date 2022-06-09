  
import pygame

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
yellow   = ( 255,255,0)

pygame.init()

Trollicon = pygame.image.load('images/Trollman.png')
pygame.display.set_icon(Trollicon)

#Add music
pygame.mixer.init()
pygame.mixer.music.load('slider.mp3')
pygame.mixer.music.play(-1, 0.0)

# MOVED UP TO BETTER ORGANIZATION
pygame.display.set_caption('Vax-Man (Electronic Arts - Forage)')
screen = pygame.display.set_mode([606, 606])
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)

clock = pygame.time.Clock()

# Height and width of Vaxman and ghosts
w = 303-16 #Width
p_h = (7*60)+19 #Vaxman height
m_h = (4*60)+19 #Monster height
b_h = (3*60)+19 #Binky height
i_w = 303-16-32 #Inky width
c_w = 303+(32-16) #Clyde width



pygame.font.init()
font = pygame.font.Font("emulogic.ttf", 12)

# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x,y,width,height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
  
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

# This creates all the walls in room 1
def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list=pygame.sprite.RenderPlain()
     
    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [ [0,0,6,600],
              [0,0,600,6],
              [0,600,606,6],
              [600,0,6,606],
              [300,0,6,66],
              [60,60,186,6],
              [360,60,186,6],
              [60,120,66,6],
              [60,120,6,126],
              [180,120,246,6],
              [300,120,6,66],
              [480,120,66,6],
              [540,120,6,126],
              [120,180,126,6],
              [120,180,6,126],
              [360,180,126,6],
              [480,180,6,126],
              [180,240,6,126],
              [180,360,246,6],
              [420,240,6,126],
              [240,240,42,6],
              [324,240,42,6],
              [240,240,6,66],
              [240,300,126,6],
              [360,240,6,66],
              [0,300,66,6],
              [540,300,66,6],
              [60,360,66,6],
              [60,360,6,186],
              [480,360,66,6],
              [540,360,6,186],
              [120,420,366,6],
              [120,420,6,66],
              [480,420,6,66],
              [180,480,246,6],
              [300,480,6,66],
              [120,540,126,6],
              [360,540,126,6]
            ]
     
    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        wall=Wall(item[0],item[1],item[2],item[3],blue)
        wall_list.add(wall)
        all_sprites_list.add(wall)
         
    # return our new list
    return wall_list

def setupGate(all_sprites_list):
      gate = pygame.sprite.RenderPlain()
      gate.add(Wall(282,242,42,2,white))
      all_sprites_list.add(gate)
      return gate

# This class represents the ball        
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):
     
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
 
        # Create an image of the block, and fill it with a color.
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
 
        self.rect = self.image.get_rect() 

# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):

    name = ""

    # Set speed vector
    change_x=0
    change_y=0
  
    # Constructor function
    def __init__(self,x,y, filename,name):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
   
        # Set height, width
        self.image = pygame.image.load(filename).convert_alpha()
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

        self.name = name

    # Clear the speed of the player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y
          
    # Find a new position for the player
    def update(self,walls,gate):

        # Get the old position, in case we need to go back to it
        old_x=self.rect.left
        new_x=old_x+self.change_x
        prev_x=old_x+self.prev_x
        self.rect.left = new_x
        
        old_y=self.rect.top
        new_y=old_y+self.change_y
        prev_y=old_y+self.prev_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:

            self.rect.left=old_x

        else:
            self.rect.top = new_y


            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                self.rect.top=old_y

        if gate != False:
          gate_hit = pygame.sprite.spritecollide(self, gate, False)
          if gate_hit:
            self.rect.left=old_x
            self.rect.top=old_y
    

#Inheritime Player klassist
class Ghost(Player):
    spawn_time = 0
    turn = 0
    steps = 0

    def incrementTime(self,tick):
      self.spawn_time += tick

    # Change the speed of the ghost
    def changespeed(self,list,ghost,turn,steps,l):
      try:
        z=list[turn][2]
        if steps < z:
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps+=1
        else:
          if turn < l:
            turn+=1
          elif ghost == "clyde":
            turn = 2
          else:
            turn = 0
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps = 0
        return [turn,steps]
      except IndexError:
         return [0,0]

DIR_Pinky = [
[0,-30,4],
[15,0,9],
[0,15,11],
[-15,0,23],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,19],
[0,15,3],
[15,0,3],
[0,15,3],
[15,0,3],
[0,-15,15],
[-15,0,7],
[0,15,3],
[-15,0,19],
[0,-15,11],
[15,0,9]
]

DIR_Blinky = [
[0,-15,4],
[15,0,9],
[0,15,11],
[15,0,3],
[0,15,7],
[-15,0,11],
[0,15,3],
[15,0,15],
[0,-15,15],
[15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,3],
[-15,0,7],
[0,-15,3],
[15,0,15],
[0,15,15],
[-15,0,3],
[0,15,3],
[-15,0,3],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,11],
[0,-15,7],
[15,0,5]
]

DIR_Inky = [
[30,0,2],
[0,-15,4],
[15,0,10],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,3],
[0,-15,15],
[-15,0,15],
[0,15,3],
[15,0,15],
[0,15,11],
[-15,0,3],
[0,-15,7],
[-15,0,11],
[0,15,3],
[-15,0,11],
[0,15,7],
[-15,0,3],
[0,-15,3],
[-15,0,3],
[0,-15,15],
[15,0,15],
[0,15,3],
[-15,0,15],
[0,15,11],
[15,0,3],
[0,-15,11],
[15,0,11],
[0,15,3],
[15,0,1],
]

DIR_Clyde = [
[-30,0,2],
[0,-15,4],
[15,0,5],
[0,15,7],
[-15,0,11],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,7],
[0,15,15],
[15,0,15],
[0,-15,3],
[-15,0,11],
[0,-15,7],
[15,0,3],
[0,-15,11],
[15,0,9],
]

pinky_len = len(DIR_Pinky)-1
blinky_len = len(DIR_Blinky)-1
inky_len = len(DIR_Inky)-1
clyde_len = len(DIR_Clyde)-1

def startGame():

  all_sprites_list = pygame.sprite.RenderPlain()
  block_list = pygame.sprite.RenderPlain()
  monsta_list = pygame.sprite.RenderPlain()
  pacman_collide = pygame.sprite.RenderPlain()
  wall_list = setupRoomOne(all_sprites_list)
  gate = setupGate(all_sprites_list)

  # Create the player paddle object
  Pacman = Player( w, p_h, "images/Trollman.png" , "Vax-man" )
  all_sprites_list.add(Pacman)
  pacman_collide.add(Pacman)
   
  Blinky = Ghost( w, b_h, "images/Blinky.png" , "Blinky" )
  monsta_list.add(Blinky)
  all_sprites_list.add(Blinky)

  Pinky = Ghost( w, m_h, "images/Pinky.png" , "Pinky" )
  monsta_list.add(Pinky)
  all_sprites_list.add(Pinky)
   
  Inky = Ghost( i_w, m_h, "images/Inky.png" , "Inky" )
  monsta_list.add(Inky)
  all_sprites_list.add(Inky)
   
  Clyde = Ghost( c_w, m_h, "images/Clyde.png" , "Clyde" )
  monsta_list.add(Clyde)
  all_sprites_list.add(Clyde)

  # Draw the grid
  for row in range(19):
      for column in range(19):
          if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
              continue
          else:
            block = Block(yellow, 4, 4)

            # Set a random location for the block
            block.rect.x = (30*column+6)+26
            block.rect.y = (30*row+6)+26

            b_collide = pygame.sprite.spritecollide(block, wall_list, False)
            p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
            if b_collide:
              continue
            elif p_collide:
              continue
            else:
              # Add the block to the list of objects
              block_list.add(block)
              all_sprites_list.add(block)

  points = len(block_list)
  score = 0
  done = False


  while done == False:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              done=True

          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,-30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,30)

          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,-30)
          
      # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
   
      # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
      Pacman.update(wall_list,gate)

      for ghost in monsta_list:
        directionList = list()
        ghostName = ""
        directionLength = list()

        if ghost.name == "Pinky":
          directionList = DIR_Pinky
          ghostName = False
          directionLength = pinky_len
        elif ghost.name == "Blinky":
          directionList = DIR_Blinky
          ghostName = False
          directionLength = blinky_len
        elif ghost.name == "Inky":
          directionList = DIR_Inky
          ghostName = False
          directionLength = inky_len
        elif ghost.name == "Clyde":
          directionList = DIR_Clyde
          ghostName = "clyde"
          directionLength = clyde_len
        
        returned = ghost.changespeed(directionList,ghostName,ghost.turn,ghost.steps,directionLength)
        ghost.turn = returned[0]
        ghost.steps = returned[1]
        ghost.changespeed(directionList,ghostName,ghost.turn,ghost.steps,directionLength)
        ghost.update(wall_list,False)

      # See if the Vaxman block has collided with anything.
      blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
       
      # Check the list of collisions.
      if len(blocks_hit_list) > 0:
          score +=len(blocks_hit_list)
      
      # LOGIC ABOVE
   
      # DRAW BELOW
      screen.fill(black)
      wall_list.draw(screen)
      gate.draw(screen)
      all_sprites_list.draw(screen)
      monsta_list.draw(screen)

      text = font.render("Score: "+str(score)+"/"+str(points), True, white)
      screen.blit(text, [15, 15])

      ghost_counter_txt = font.render("Ghosts left: "+str(len(monsta_list)), True, white)
      screen.blit(ghost_counter_txt, [15, 37])

      if score == points:
        doNext("Congratulations, you won!",145,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)
      
      # Kills a ghost
      monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, True)

      if (len(monsta_list) > 128):
        doNext("Game Over",235,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)      

      # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      
      pygame.display.flip()

      clock.tick(10)

      for ghost in monsta_list:
        ghost.incrementTime(0.1)
        
        if (ghost.spawn_time > 30):
          ghost.spawn_time = 0
          NewGhost = Ghost( w, m_h, "images/Pinky.png" , "Pinky" )

          if ghost.name == "Pinky":
            NewGhost = Ghost( w, m_h, "images/Pinky.png" , "Pinky" )
          elif ghost.name == "Blinky":
            NewGhost = Ghost( w, b_h, "images/Blinky.png" , "Blinky" )
          elif ghost.name == "Inky":
            NewGhost = Ghost( i_w, m_h, "images/Inky.png" , "Inky" )
          elif ghost.name == "Clyde":
            NewGhost = Ghost( c_w, m_h, "images/Clyde.png" , "Clyde" )

          NewGhost.spawn_time = 0
          monsta_list.add(NewGhost)
          all_sprites_list.add(NewGhost)
      

def doNext(message,left,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate):
  while True:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()

          if event.key == pygame.K_RETURN:
            del all_sprites_list
            del block_list
            del monsta_list
            del pacman_collide
            del wall_list
            del gate
            startGame()

      #Grey background
      w = pygame.Surface((400,200))  # the size of your rect
      w.set_alpha(10)                # alpha level
      w.fill((128,128,128))           # this fills the entire surface
      screen.blit(w, (100,200))    # (0,0) are the top-left coordinates

      #Won or lost
      text1=font.render(message, True, white)
      screen.blit(text1, [left, 233])

      text2=font.render("To play again, press ENTER.", True, white)
      screen.blit(text2, [135, 303])
      text3=font.render("To quit, press ESCAPE.", True, white)
      screen.blit(text3, [165, 333])

      pygame.display.flip()

      clock.tick(10)

startGame()

pygame.quit()