import pygame as pg
from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import math
import random
white=(255, 255, 255)
black=(0, 0, 0)
class Stars :
    def __init__(self):
        self.pos=[]
        num_stars = 100
        for _ in range(num_stars):
            x = random.uniform(-3,3)
            y = random.uniform(-3,3)
            r=random.uniform(0.001,0.005)
            self.pos.append((x,y,r))
    def draw(self):
        for star in self.pos:
            draw_filledcircle(star[2],5,(1,1,1),star[0],star[1])     
def DrawCube(x1, y1, z1, x2, y2, z2):
    glBegin(GL_LINE_LOOP)
    glVertex3f(x1, y1, z1)
    glVertex3f(x1, y2, z1)
    glVertex3f(x2, y2, z1)
    glVertex3f(x2, y1, z1)
    glEnd()
    # Back face
    glBegin(GL_LINE_LOOP)
    glColor3f(1, 0, 0) 
    glVertex3f(x1, y1, z2)
    glVertex3f(x1, y2, z2)
    glVertex3f(x2, y2, z2)
    glVertex3f(x2, y1, z2)
    glEnd()
    # Top face
    glBegin(GL_LINE_LOOP)
    glColor3f(1, 0,0)  
    glVertex3f(x1, y2, z1)
    glVertex3f(x1, y2, z2)
    glVertex3f(x2, y2, z2)
    glVertex3f(x2, y2, z1)
    glEnd()
    # Bottom face
    glBegin(GL_LINE_LOOP)
    glColor3f(1, 0,0) 
    glVertex3f(x1, y1, z1)
    glVertex3f(x1, y1, z2)
    glVertex3f(x2, y1, z2)
    glVertex3f(x2, y1, z1)

    glEnd()
    # Left face
    glBegin(GL_LINE_LOOP)
    glColor3f(1, 0, 0)  
    glVertex3f(x1, y1, z1)
    glVertex3f(x1, y2, z1)
    glVertex3f(x1, y2, z2)
    glVertex3f(x1, y1, z2)
    glEnd()    
    # Right face
    glBegin(GL_LINE_LOOP)
    glColor3f(1, 0, 0) 
    glVertex3f(x2, y1, z1)
    glVertex3f(x2, y2, z1)
    glVertex3f(x2, y2, z2)
    glVertex3f(x2, y1, z2)

    glEnd()
class Projectile:
    def __init__(self, x, y, scale):
        self.x = x
        self.y = y
        self.scale = scale
        self.hitbox=Circle(0.015*scale,x,y+0.03*scale)
    def draw_projectille(self):
        draw_filledcircle(0.015*self.scale,20,(1,0,0),self.x,self.y+0.03*self.scale)
        draw_elipse3(0.02*self.scale,20,(1,0,0),self.x,self.y)
    def move(self):
        self.y+=0.05
        self.hitbox.centery+=0.05
def draw_projectille(x,y,scale):
    draw_filledcircle(0.015*scale,20,(1,0,0),x,y+0.03*scale)
    draw_elipse3(0.02*scale,20,(1,0,0),x,y)
def draw_elipse3(raduis,num_segments,color,centerx,centery):
    glBegin(GL_POLYGON)
    rx=raduis
    ry=1.8*raduis
    for i in range (num_segments):
        angle =2*math.pi * i / num_segments
        x = rx * math.cos(angle)+centerx
        y = ry * math.sin(angle)+centery
        glColor4f(color[0],color[1],color[2],0.5)
        glVertex2f(x,y)
    glEnd()
def check_collision(circle1, circle2):
    distance_squared = (circle1.centerx - circle2.centerx) ** 2 + (circle1.centery - circle2.centery) ** 2
    radius_sum = circle1.radius + circle2.radius
    return distance_squared <= radius_sum ** 2
def load_texture(filename):
    texture_surface = pg.image.load(filename)
    texture_data = pg.image.tostring(texture_surface, "RGBA", True)
    width = texture_surface.get_width()
    height = texture_surface.get_height()

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    return texture
def draw(texture,x,y,scale):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    glBegin(GL_QUADS)
    glColor3f(1,1,1)
    glTexCoord2f(0, 0)
    glVertex3f(x-1*scale, y-1*scale, 0)
    glTexCoord2f(1, 0)
    glVertex3f(x+1*scale, y-1*scale, 0)
    glTexCoord2f(1, 1)
    glVertex3f(x+1*scale, y+1*scale, 0)
    glTexCoord2f(0, 1)
    glVertex3f(x-1*scale, y+1*scale, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)
class Spaceship:
    def __init__(self, x, y, scale,texture):
        self.x = x
        self.y = y
        self.scale = scale
        self.hitbox=Circle(scale,x,y)
        self.texture=texture
        self.targetable=True
    def draw(self):
        draw(self.texture,self.x, self.y, self.scale)
    def move(self, speedx):
        if -2.5<self.x+speedx<2.5:
            self.x += speedx
            self.hitbox.centerx += speedx
    def respawn(self):
        self.x=0
        self.y=-1.8
        self.hitbox.centerx=0
        self.hitbox.centery=-1.8
class Chicken:
    def __init__(self, x, y, scale):
        self.x = x
        self.y = y
        self.scale = scale
        self.hitbox=Circle(0.14*scale,x,y+0.04*scale)
        self.egg=None
    def draw_chicken(self):
        draw_chicken(self.x, self.y, self.scale)
    def spawn_egg(self):
        if self.egg==None:
            chance=random.randint(1,100)
            if chance<=2:
                self.egg=Egg(self.x,self.y-0.06*self.scale,2)
        else:
            self.egg.draw_egg()
            if self.egg.y<-2:
                self.egg=None
    def destroy_self(self,chickens):
        chickens.remove(self)  
        del self
class Circle:
    def __init__(self, radius,centerx, centery):
        self.radius = radius
        self.centerx = centerx
        self.centery = centery
class Egg:
    def __init__(self, x, y, scale):
        self.x = x
        self.y = y
        self.scale = scale
        self.hitbox=Circle(0.02*scale,x,y)
        self.speed=0.02
    def clone_init(self,egg):
        self.x = egg.x
        self.y = egg.y
        self.scale = egg.scale
        self.hitbox=Circle(0.02*egg.scale,egg.x,egg.y)
        self.speed=0.02
    def draw_egg(self):
        self.y=self.y-self.speed
        self.hitbox.centery=self.y
        draw_egg(self.x, self.y, self.scale)
def draw_egg(x,y,scale):
    draw_filledcircle(0.02*scale,20,(1,1,1),x,y)
    draw_circle(0.02*scale,20,(0,0,0),x,y)
def draw_chicken(x,y,scale):
    
    draw_chicken_wings(x,y,scale)
    draw_body(x,y,scale)
    draw_chicken_legs(x,y,scale)
    draw_chicken_head(x,y,scale)
def draw_body(x,y,scale):
    draw_filledcircle(0.085*scale,20,(1,1,1),x,y) #body
    draw_circle(0.085*scale,20,(0,0,0),x,y) # body outline
def draw_chicken_legs(x,y,scale):
    draw_filledcircle(0.02*scale,20,(1,165/255,0),x-0.03*scale,y-0.102*scale)
    draw_filledcircle(0.02*scale,20,(1,165/255,0),x+0.03*scale,y-0.102*scale)
def draw_heart(x, y, scale):
        draw_filledcircle(0.05*scale, 360, (1, 0, 0), x-0.05*scale, y)
        draw_filledcircle(0.05*scale, 360, (1, 0, 0), x+0.05*scale, y)
        draw_triangle(x-0.1*scale, y-0.016*scale, x+0.1*scale, y-0.016*scale, x, y-0.15*scale, (1, 0, 0))
def draw_chicken_wings(x,y,scale):
    draw_elipse2(0.03*scale,20,(1,1,1),x-0.07*scale,y+0.025*scale) #wing top
    draw_elipse2outline(0.03*scale,20,(0,0,0),x-0.07*scale,y+0.025*scale)
    draw_elipse2(0.025*scale,20,(1,1,1),x-0.05*scale,y-0.015*scale) #wing middle
    draw_elipse2outline(0.025*scale,20,(0,0,0),x-0.05*scale,y-0.015*scale)
    draw_elipse2(0.02*scale,20,(1,1,1),x-0.035*scale,y-0.05*scale) #wing bot
    draw_elipse2outline(0.02*scale,20,(0,0,0),x-0.035*scale,y-0.05*scale)
    draw_elipse2(0.03*scale,20,(1,1,1),x+0.07*scale,y+0.025*scale) #wing top
    draw_elipse2outline(0.03*scale,20,(0,0,0),x+0.07*scale,y+0.025*scale)
    draw_elipse2(0.025*scale,20,(1,1,1),x+0.05*scale,y-0.015*scale) #wing middle
    draw_elipse2outline(0.025*scale,20,(0,0,0),x+0.05*scale,y-0.015*scale)
    draw_elipse2(0.02*scale,20,(1,1,1),x+0.035*scale,y-0.05*scale) #wing bot
    draw_elipse2outline(0.02*scale,20,(0,0,0),x+0.035*scale,y-0.05*scale)
def draw_chicken_head(x,y,scale):
    draw_elipse(0.03*scale,20,(1,0,0),x,y+0.19*scale) #chin
    draw_filledcircle(0.08*scale,20,(1,1,1),x,y+0.1*scale) #head
    draw_circle(0.08*scale,20,(0,0,0),x,y+0.1*scale) #head outline
    draw_filledcircle(0.013*scale,20,(0,0,0),x-0.03*scale,y+0.12*scale) #eye 1
    draw_filledcircle(0.013*scale,20,(0,0,0),x+0.03*scale,y+0.12*scale) #eye 2
    draw_pyramid(x,y+0.085*scale,(1,165/255,0),0.3*scale) #beak
    draw_elipse(0.015*scale,20,(1,0,0),x,y+0.015*scale) #chin
def draw_elipse(raduis,num_segments,color,centerx,centery):
    glBegin(GL_POLYGON)
    rx=raduis
    ry=1.8*raduis
    for i in range (num_segments):
        angle =2*math.pi * i / num_segments
        x = rx * math.cos(angle)+centerx
        y = ry * math.sin(angle)+centery
        glColor3f(color[0],color[1],color[2])
        glVertex2f(x,y)
    glEnd()
def draw_elipse2(raduis,num_segments,color,centerx,centery):
    glBegin(GL_POLYGON)
    rx=raduis*4
    ry=raduis
    for i in range (num_segments):
        angle =2*math.pi * i / num_segments 
        x = rx * math.cos(angle)+centerx
        y = ry * math.sin(angle)+centery
        glColor3f(color[0],color[1],color[2])
        glVertex2f(x,y)
    glEnd()
def draw_elipse2outline(raduis,num_segments,color,centerx,centery):
    glBegin(GL_LINE_LOOP)
    rx=raduis*4
    ry=raduis
    for i in range (num_segments):
        angle =2*math.pi * i / num_segments 
        x = rx * math.cos(angle)+centerx
        y = ry * math.sin(angle)+centery
        glColor3f(color[0],color[1],color[2])
        glVertex2f(x,y)
    glEnd()
def draw_pyramid(x, y, color, scale):
    glBegin(GL_TRIANGLES)
    glColor3f(color[0], color[1], color[2])
    glVertex3f(x, y, 0.1)
    glVertex3f(x - 0.1*scale, y-0.1*scale, 0)
    glVertex3f(x + 0.1*scale, y-0.1*scale, 0)  # Vertex 2
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(color[0], color[1], color[2])
    glVertex3f(x, y, 0.1*scale)
    glVertex3f(x - 0.1*scale, y-0.1*scale, 0)
    glVertex3f(x , y + 0.1*scale, 0)  # Vertex 3
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(color[0], color[1], color[2])
    glVertex3f(x, y, 0.1)
    glVertex3f(x +0.1*scale, y - 0.1*scale, 0)
    glVertex3f(x, y+0.1*scale, 0)  # Vertex 4
    glEnd()
    glBegin(GL_LINES)
    glColor3f(0,0,0)
    glVertex3f(x, y, 0.1*scale)
    glVertex3f(x - 0.1*scale, y-0.1*scale, 0)
    glEnd()
    glBegin(GL_LINES)
    glColor3f(0,0,0)
    glVertex3f(x, y, 0.1*scale)
    glVertex3f(x + 0.1*scale, y-0.1*scale, 0)
    glEnd()
    glBegin(GL_LINES)
    glColor3f(0,0,0)
    glVertex3f(x, y, 0.1*scale)
    glVertex3f(x , y+0.1*scale, 0)
    glEnd()
def draw_circle(raduis,num_segments,color,centerx,centery):
    glBegin(GL_LINE_LOOP)
    for i in range (num_segments):
        angle =2*math.pi * i / num_segments
        x = raduis * math.cos(angle)+centerx
        y = raduis * math.sin(angle)+centery
        glColor3f(color[0],color[1],color[2])
        glVertex2f(x,y)
    glEnd()   
def draw_filledcircle(raduis,num_segments,color,centerx,centery):
    glBegin(GL_POLYGON)
    for i in range (num_segments):
        angle =2*math.pi * i / num_segments
        x = raduis * math.cos(angle)+centerx
        y = raduis * math.sin(angle)+centery
        glColor4f(color[0],color[1],color[2],1)
        glVertex2f(x,y)
    glEnd()            
def drawText(x, y, text, font):                                                
    textSurface = font.render(text, True, white, black)
    textSurface.set_colorkey((0,0,0))
    textData = pg.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
def draw_triangle(x1,y1,x2,y2,x3,y3,color):
    glBegin(GL_TRIANGLES)
    glColor3f(color[0],color[1],color[2])
    glVertex2f(x1,y1)
    glVertex2f(x2,y2)
    glVertex2f(x3,y3)
    glEnd() 
def draw_stars() :    
    num_stars = 50
    for _ in range(num_stars):
        x = random.uniform(-3,3)
        y = random.uniform(-3,3)
        r=random.uniform(0.001,0.005)
        draw_filledcircle(r,5,(1,1,1),x,y)
def main():
    currentlevel=1
    currentlives=3
    screen_width=800
    screen_height = 600
    Paused=False
    pg.init()
    pg.font.init()
    display = (screen_width,screen_height)
    screen=pg.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    font = pg.font.Font('PressStart2P-vaV7.ttf', 14)
    title_font = pg.font.Font('PressStart2P-vaV7.ttf', 24)
    title_font.set_bold(True)
    Running=True
    clock = pg.time.Clock()
    speedx=0
    time=0
    start_x=-2.2
    start_y=1.3
    level_started=False
    canShoot=True  
    GameOver=False
    Mainmenu=True
    texture = load_texture("spaceship.png")
    spaceship=Spaceship(0, -1.8,0.2,texture)
    music=pg.mixer.Sound("vibe.mp3")
    GameOver_music=pg.mixer.Sound("Game_Over_Sound.mp3")
    chicken_death=pg.mixer.Sound("chicken.mp3")
    MainMenu_Music=pg.mixer.Sound("mainmenu.mp3")
    timer=0
    stars_timer=0
    pg.mixer.Channel(0).play(MainMenu_Music,-1,0)
    isMusicPlaying=False
    Orphan_egg=[]
    projectiles=[]
    stars=[]
    stars.append(Stars())
    glPushMatrix()
    while Running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Running = False
            elif event.type== pg.KEYDOWN:
                if event.key == pg.K_p:
                    Paused = not Paused
                elif event.key == pg.K_a:
                    speedx=-0.1
                elif event.key == pg.K_d:
                    speedx=0.1
                if event.key == pg.K_SPACE and canShoot==True:
                    timer=1000
                    canShoot=False
                    projectiles.append(Projectile(spaceship.x,spaceship.y+0.05,1))
                elif event.key == pg.K_r and GameOver:
                    currentlevel=1
                    currentlives=3
                    GameOver=False
                    spaceship.respawn()
                    spaceship.targetable=True
                    pg.mixer.Channel(0).unpause()
                elif event.key==pg.K_RETURN and GameOver:
                    Mainmenu=True
                    currentlevel=1
                    currentlives=3
                    GameOver=False
                    spaceship.respawn()
                    spaceship.targetable=True
                    pg.mixer.Channel(0).play(MainMenu_Music,-1,0)
                elif event.key == pg.K_RETURN and Mainmenu:
                    Mainmenu=False
            elif event.type==pg.KEYUP:
                if event.key == pg.K_a or event.key == pg.K_d: 
                    speedx=0
                    
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if Mainmenu : 
            screen.fill(black)
            glPushMatrix()
            stars_timer+=clock.get_time()
            if stars_timer>=20000:
                stars_timer=0
                stars[0]=Stars()
            glTranslatef(0.0, 0.0, 4.6*stars_timer/20000)
            stars[0].draw()
            glPopMatrix()
            drawText(200,50,"Press Enter To Start The Game",font)
            drawText(210,400,"CHICKEN INVADERS",title_font)
            DrawCube(-0.5,-0.5,-0.5,0.5,0.5,0.5)
            draw_chicken(0,-0.1,1.8)
            """
            screen.fill(black)
            DrawCube(-1,-1,-1,1,1,1)
            if stars_timer==3000: 
                glPushMatrix()
            stars_timer-=clock.get_time()
            if(stars_timer<=0):
                stars_timer=3000
                stars[0]=Stars()
                glPopMatrix()
            glTranslatef(0.0, 0.0, 0.05)
            stars[0].draw()
            drawText(200,50,"Press Enter To Start The Game",font)
            drawText(210,350,"CHICKEN INVADERS",title_font)
            """
            
        elif GameOver:
            screen.fill(black)
            drawText(275,300,"Press R to restart",font)
            drawText(180,250,"Press Enter to return to Main Menu",font)
            drawText(275,350,"GAME OVER",title_font)
            pg.mixer.Channel(0).pause()
        elif Paused:
            screen.fill(black)
            clock.get_time()
        else:
            
            if not isMusicPlaying:
                glPopMatrix()
                isMusicPlaying=True
                pg.mixer.Channel(0).play(music,-1,0,3000)
            time+=clock.get_time()
            screen.fill(black)
            drawText(20,550,"Level "+str(currentlevel),font)
            drawText(640,550,"Lives "+str(currentlives),font)
            draw_stars()
            spaceship.move(speedx)
            if spaceship.targetable==False:
                respawn_timer-=clock.get_time()
                glPushMatrix()
                glRotatef(180*(1-respawn_timer/5000),0,0,1)
                glTranslatef(0,0,-20*(1-respawn_timer/5000))
                spaceship.draw()
                glPopMatrix()
                if respawn_timer<=0:
                    spaceship.targetable=True
                    spaceship.respawn()
            draw_heart(2.5,1.8,0.8)
            if canShoot==False:
                timer-=clock.get_time()
                if timer<=0:
                    canShoot=True
            
            if not level_started:
                num_chickens=10*currentlevel
                chickens=[]
                for i in range(num_chickens):
                    chickens.append(Chicken(start_x,start_y,1))
                    start_x+=0.5
                    if start_x>2.4:
                        start_x=-2.2
                        start_y-=0.5
                level_started=True               
            for chicken in chickens:
                chicken.draw_chicken()
                chicken.spawn_egg()
                if chicken.egg!=None and spaceship.targetable:
                    if check_collision(spaceship.hitbox,chicken.egg.hitbox):
                        currentlives-=1
                        chicken.egg=None
                        respawn_timer=5000
                        spaceship.targetable=False
                        if currentlives<0:
                            GameOver=True
                            pg.mixer.Channel(2).play(GameOver_music)
            for projectile in projectiles:
                projectile.move()
                for chicken in chickens:
                    if check_collision(projectile.hitbox,chicken.hitbox):
                        if chicken.egg!=None:
                            temp_egg=Egg(0,0,0)
                            temp_egg.clone_init(chicken.egg)
                            Orphan_egg.append(temp_egg) 
                        chicken.destroy_self(chickens)
                        num_chickens-=1
                        pg.mixer.Channel(1).play(chicken_death)
                        projectiles.remove(projectile)

                projectile.draw_projectille()
                if projectile.y>2:
                    projectiles.remove(projectile) 
            for egg in Orphan_egg:
                egg.draw_egg()
                if spaceship.targetable and check_collision(spaceship.hitbox,egg.hitbox):
                    currentlives-=1
                    Orphan_egg.remove(egg)
                    respawn_timer=5000
                    spaceship.targetable=False
                    if currentlives<0:
                        GameOver=True
                        pg.mixer.Channel(2).play(GameOver_music)
                elif egg.y<-2:
                    Orphan_egg.remove(egg)      
            if num_chickens==0:
                currentlevel+=1
                start_y=1.3
                level_started=False
                projectiles=[]
            if spaceship.targetable==True:
                spaceship.draw()
        pg.display.flip()
        clock.tick(20)
        
main()