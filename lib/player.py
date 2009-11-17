class Creature(object):
    creature_batch = pyglet.graphics.Batch()
    #States that a bug can be in
    STOPPED     = 0 
    MOVING      = 1
 
    def __init__(self, tile, game_data, centerx=0, centery=0, width=32, height=32):
            self.game                           = game_data["game"]
            self.game_data                      = game_data
            sequence_names                      = [ name for name in self.game_data['data']['agents']['Monster01']['animations']]
            sequence                            = [self.game_data['data']['agents']['Monster01']['animations'][i] for i in self.game_data['data']['agents']['Monster01']['animations']]
            animation                           = pyglet.image.Animation.from_image_sequence(sequence, 0.3, True )
            self.sprite                         = animatedsprite.AnimatedSprite(animation, 0, 0, batch=self.creature_batch, file_names=sequence_names)
            #This needs to be fixed
            #Left Sprite set
            self.sprite.add_pic_name_look_up(["Monster_Left1.png", "Monster_Left2.png"])
            #Right sprite set
            self.sprite.add_pic_name_look_up(["Monster_Right1.png","Monster_Right2.png"])
            #Up sprite set
            self.sprite.add_pic_name_look_up(["Monster_Up1.png", "Monster_Up2.png"])
            #Down sprite set
            self.sprite.add_pic_name_look_up(["Monster_Down1.png", "Monster_Down2.png"])
            self.sprite.set_active_lookup(4)
            self.tile                           = tile 
            self.width                          = self.sprite.width
            self.height                         = self.sprite.height
            x, y                                = self.tile.position
            if centerx: 
                self.centerx                    = centerx
            else: 
                self.centerx                    = (x+0.5)*self.tile.return_tile_size()
            if centery: 
                self.centery                    = centery 
            else: 
                self.centery                    = (y+0.5)*self.tile.return_tile_size() 
            self.sprite.x                       = self.left
            self.sprite.y                       = self.bottom
            self.move_x=0
            self.move_y=0
            self.speed = 4
            self.state          = self.STOPPED
            self.beginingx     = None
            self.beginingy     = None
            self.destinationx  = None
            self.destinationy  = None
            self.time           = 0

            self.game.add_handler(self)

    @property
    def left(self):
        return self.centerx - (self.width // 2)

    @property
    def right(self):
        return self.centerx +  (self.width // 2)
        
    @property
    def top(self):
        return self.centery + (self.height // 2)

    @property
    def bottom(self):
        return self.centery -  (self.height // 2)

    def on_key_press(self, *args):
        symbol, mods = args
        if not (mods & pyglet.window.key.MOD_SHIFT):
            if symbol == key.MOTION_DOWN:
                print "down"
                self.move_y=-1
                self.sprite.set_active_lookup(4)
            elif symbol == key.MOTION_UP:
                print "Up"
                self.move_y=1
                self.sprite.set_active_lookup(3)
            elif symbol == key.MOTION_LEFT:
                print "Left"
                self.move_x=-1
                self.sprite.set_active_lookup(1)
            elif symbol == key.MOTION_RIGHT:
                print "Right"
                self.move_x=1
                self.sprite.set_active_lookup(2)
        if self.move_y !=0 or self.move_x != 0:
            self.beginingx      = self.centerx
            self.destinationx   = self.centerx + (self.move_x * 20)
            self.beginingy      =  self.centery
            self.destinationy   = self.centery + (self.move_y * 20)
            self.time           = 0
            self.state          = self.MOVING

    def on_key_release(self, *args):   
        symbol, mods = args
        if self.move_y==1 and symbol == pyglet.window.key.MOTION_UP:
            self.move_y=0
        if self.move_y==-1 and symbol == pyglet.window.key.MOTION_DOWN:
            self.move_y=0
        if self.move_x==-1 and symbol == pyglet.window.key.MOTION_LEFT:
            self.move_x=0
        if self.move_x==1 and symbol == pyglet.window.key.MOTION_RIGHT:
            self.move_x=0         

    def on_update(self, dt):   
        '''Update sprites postion/state'''
        if self.state == self.MOVING:
            print self.move_y, self.move_x
            self.time += 1
            changex             = self.destinationx - self.beginingx
            changey             = self.destinationy - self.beginingy
            duration    = math.sqrt( (changex * changex) + (changey * changey))//self.speed
            if not (self.time > duration):
                self.centerx            = self.linear_tween(self.time, duration, changex, self.beginingx)
                self.centery            = self.linear_tween(self.time, duration, changey, self.beginingy)
                self.sprite.x           = self.centerx#right
                self.sprite.y           = self.centery#top
            else:
                self.state              = self.STOPPED

    def move_to_pt(self,dest):
        self.destinationx = dest[0]
        self.destinationy = dest[1]
        self.beginingx    = self.centerx
        self.beginingy    = self.centery
        self.time = 0
        self.state = self.MOVING   

    def linear_tween(self, t, d, c, b):
        '''
        function used to make movement of bugs look smooth
        t = time, d = duration, c = changes in position, b = begin position
        '''
        return c*t//d + b


