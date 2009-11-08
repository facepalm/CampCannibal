# this is improved version of animatedsprite which can be found here:
# http://swiftcoder.wordpress.com/2009/04/17/enhanced-animation-code-for-pyglet/

import pyglet

class AnimatedSprite(pyglet.sprite.Sprite):
    ''' Sprite subclass providing advanced
            playback controls for animated sprites '''

    def __init__(self,
                         img, x=0, y=0,
                         blend_src=pyglet.gl.GL_SRC_ALPHA,
                         blend_dest=pyglet.gl.GL_ONE_MINUS_SRC_ALPHA,
                         batch=None,
                         group=None,
                         usage='dynamic',
                         file_names=None):
        pyglet.sprite.Sprite.__init__(self, img, x, y, blend_src, blend_dest, batch, group, usage)

        self._paused = False
        self._range = (0, 1)
        self._frame_lookup = [ range(0, len(self._animation.frames)) ]
        self._current_lookup_index = 0
        self.look_up_map = {}
        if file_names is not None:
            print "Filenames"
            #Map the picture list to file name 
            self.file_names = file_names
            print [f for f in self.file_names]
            i = 0 # There is a nicer way of doing this  with list compres -htormey
            for n in self.file_names:
                self.look_up_map[n] = i
                i += 1
            print self.look_up_map

    def _animate(self, dt):
        self._frame_index += 1
        if self._frame_index >= self.range[1]:
            self._frame_index = self.range[0]
            self.dispatch_event('on_animation_end')

        # use frame lookup table
        frame = self._animation.frames[ self._frame_lookup[self._current_lookup_index][self._frame_index]]
        self._set_texture(frame.image.get_texture())

        if frame.duration != None:
            pyglet.clock.schedule_once(self._animate, frame.duration)
        else:
            self.dispatch_event('on_animation_end')

    def set_frame(self, i):
        ''' Seek to the specified frame '''
        self._frame_index = max(self.range[0], min(self.range[1], i))
        frame = self._animation.frames[self._frame_index]

        pyglet.clock.unschedule(self._animate)
        self._animate(0.0)

    def set_loop(self, begin, end):
        ''' Loop between the begin and end frames '''
        print "set look up"
        self.range = (begin, end)

        if self._frame_index < begin:
            self._frame_index = begin-1

        pyglet.clock.unschedule(self._animate)
        self._animate(0.0)

    def pause(self):
        ''' pause animation playback '''
        if not self._paused:
            frame = self._animation.frames[self._frame_index]
            self._animate(frame.duration)
            pyglet.clock.unschedule(self._animate)
            self._paused = True

    def play(self):
        ''' resume animation playback '''
        if self._paused:
            frame = self._animation.frames[self._frame_index]
            self._animate(frame.duration)
            self._paused = False

    def set_active_lookup(self, index):
        if index >= 0 or index < len(self._frame_lookup):
            self._current_lookup_index = index
            self._frame_index = 0

    def add_pic_name_look_up(self, translate_list):
        list = []
        #Translate image names into their index
        for l in translate_list:
            if l in self.look_up_map:
                list.append(self.look_up_map[l])
        print list, " <- list"
        if len(list) > 0:
            self._frame_lookup.append(list)
            self.set_loop(0, len(list))
        else:
            return false

    def add_lookup(self, list):
        self._frame_lookup.append(list)
        self.set_loop(0, len(list))
