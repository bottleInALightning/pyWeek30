import pygame, time
pygame.init()
from code.obstacle import Obstacle
from code.dialog import Dialog

class Map:
    def __init__(self,var):
        self.current_map_path="./maps/map1.txt"
        self.current_map=None
        self.fountains = [BoostFountain(400, 400, 70, 70, var), HealthFountain(500, 600, 70, 70, var), StealthFountain(1000, 200, 70, 70, var)]
        self.load_map()#Current map gets assigned here
        self.var=var
        '''self.indices={  0:(pygame.image.load("./images/floor_sprite_test.png"),False,False,None),#img_path,Collision(obstacle),has_animation,anim_duration_min_max
                        1:("./images/temp_wall.png",True,False,[1,10]),
                        2:("./images/bush_animation_sprites.png",True,True,(5,15)),
                        3:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[0],False,False,None),#beach_left_one
                        4:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[1],False,False,None),#beach_left_two
                        5:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[2],False,False,None),#beach_corner_down_right
                        6:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[3],False,False,None),#beach_corner_up_left
                        7:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[4],False,False,None),#full_beach
                        8:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[5],False,False,None),#tiny_beach_part_up_left
                        9:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[6],False,False,None),#full water tile
                        10:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[7],False,False,None),#halfwater, half sand
                        11:(self.get_sprite_sheet((32,32),"./images/beach_water_sprites.png")[8],False,False,None),#swimming, platform
                        }'''
        img=pygame.image.load
        self.indices=[(i,False,False,None) for i in self.get_sprite_sheet((32,32),"./images/world_sprite_sheet.png")]
        self.indices.pop()
        
        self.indices.append(("./images/temp_wall.png",True,False,[0,0]))
        self.indices.append(("./images/bush_animation_sprites.png",True,True,(5,15)))
        self.indices.append((img("./images/floor_sprite_test.png"),False,False,None))
        
        #print(self.indices)
        
        #when it aint a obstacle the image should be 
        self.init_obstacles()

    def update(self):
        self.show()
        
    def load_map(self):
        with open(self.current_map_path,"r") as file:
            self.current_map=file.read()
        self.current_map=eval(self.current_map)
        
    
    def show(self):
        
        y=0
        for layer in self.current_map:
            x=0
            for number in layer:                                                  # all the obstacles should actually only be loaded once, but all the drawing stuff is supposed to 
                tx=y
                ty=x
                if number==27:#draw grass under bush
                    self.var.screen.blit(self.indices[28][0],((tx*self.var.boxes_size[0])-self.var.camera_scrolling.x,(ty*self.var.boxes_size[1])-self.var.camera_scrolling.y))
                    
                
                if self.indices[number][1]==False:#Its not interacting with its surounding
                    self.var.screen.blit(self.indices[number][0],((tx*self.var.boxes_size[0])-self.var.camera_scrolling.x,(ty*self.var.boxes_size[1])-self.var.camera_scrolling.y))
                x+=1
            
            y+=1
        
        for fountain in self.fountains:
            fountain.show()

    def init_obstacles(self):
        y=0
        for layer in self.current_map:
            x=0
            for number in layer:
                tx=y
                ty=x                                                  
                # all the obstacles should actually only be loaded once, but all the drawing stuff is supposed to 
                if self.indices[number][1]==True:#means it is an obstacle
                    self.var.obstacles.append(Obstacle(tx,ty,self.var,self.indices[number][0],self.indices[number][2],self.indices[number][3]))
                
                x+=1
            
            y+=1

    def get_sprite_sheet(self,size,file,pos=(0,0)):
        import pygame#file is path_to_file
        #Initial Values
        len_sprt_x,len_sprt_y = size #sprite size
        
        sprt_rect_x,sprt_rect_y = pos #where to find first sprite on sheet
        sheet = pygame.image.load(file).convert_alpha() #Load the sheet
        sheet_rect = sheet.get_rect()
        
        sprites = []
        
        image_size=(32,32)
    
        #print("row")
        for i in range(0,sheet_rect.width,size[0]):#columns
            #print("column")    
            sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
            sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
            sprites.append(sprite)
            sprt_rect_x += len_sprt_x
        sprt_rect_y += len_sprt_y
        sprt_rect_x = 0

        sprites=[pygame.transform.scale(i,(image_size[0],image_size[1])) for i in sprites]
        return sprites

class Fountain:
    dialog = Dialog(1000, 650, 100, 50, 'Filling up... ')

    def __init__(self, x, y, width, height, var):
        self.rect = pygame.Rect(x, y, width, height)
        self.interactable_area = pygame.Rect(x-50, y-50, width+100, height+100)
        self.var = var

        #self.var.obstacles.append(Obstacle())
    def show(self):
        for image in self.images:
            self.var.screen.blit(image, (self.rect.x-self.var.camera_scrolling.x, self.rect.y - self.var.camera_scrolling.y, *self.rect[2:]))
        #self.dialog.draw(self.var)
    
    def refill(self):
        for item in self.var.inventory.slots[:3]:
            if item.magic == self.magic:
                if item.empty:
                    #print(f'Re-filling {item.magic} potion')
                    self.dialog.show = True
                    item.empty = False
                else:
                    #print('Already full')
                    pass
                    


class BoostFountain(Fountain):
    #dialog = Dialog(800, 650, 50, 100, 'Filling up... ')
    magic = 'boost'
    images = [pygame.image.load('./images/purplefountain.png')]

class HealthFountain(Fountain):
    #dialog = Dialog(800, 650, 50, 100, 'Filling up... ')
    magic = 'health'
    images = [pygame.image.load('./images/greenfountain.png')]

class StealthFountain(Fountain):
    #dialog = Dialog(800, 650, 50, 100, 'Filling up... ')
    magic = 'stealth'
    images = [pygame.image.load('./images/yellowfountain.png')]  