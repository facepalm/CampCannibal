import pyglet
from pyglet import clock

'''

Ok, so the Tween stuff has been fixed.
What I need to figure out now is how to make Frank moving around look good.
I feel like I need to read the chapter again
Why does frank move around in a jerky fasion? I want a smooth move between points
'''

def ease_in_out_quad (t, b, c, d):
    t = t / (d/2)
    if (t < 1):
        return c/2*t*t + b
    t -= 1
    return -c/2 * (t*(t-2) - 1) + b

def ease_in_quad(t, b, c, d):
    td = t / d
    return c*(td)*td + b

def ease_none (t, b, c, d):
    return c*t/d + b

class Motion(pyglet.event.EventDispatcher):
    def __init__(self, obj, prop, begin, duration, use_seconds, looping, name):
        self.obj            = obj
        self.prop           = prop
        self.begin          = begin
        self.position       = begin
        self.duration       = duration
        self.use_seconds    = use_seconds
        self.name           = name
        self.debug_time     = debug_time
        self.time           = 1
        self.prev_position  = None
        self.prev_time      = None
        self.looping        = False 
        self.clock          = clock.Clock()
        self.register_events()

    def register_events(self):
        self.register_event_type('on_motion_started')
        self.register_event_type('on_motion_stopped')
        self.register_event_type('on_motion_resumed')
        self.register_event_type('on_motion_looped')
        self.register_event_type('on_motion_finished')
        self.register_event_type('on_motion_changed')

    def on_motion_started(self, obj):
            print "Got on_motion_started event for ", obj.name

    def on_motion_stopped(self, obj):
            print "Got on_motion_stopped event for ", obj.name

    def on_motion_resumed(self, obj):
            print "Got on_motion_resumed event for ", obj.name

    def next_frame(self, dt):
        if self.use_seconds:
            #self.set_time
            self.set_time(self.time + dt)
        else:
            #Not sure what I want to do for frames
            pass

    def prev_frame(self):
        pass

    def update(self):
        self.set_position(self.get_position(self.time))

    def set_time(self, t):
        self.prev_time = self.time
        if (t > self.duration):
            if(self.looping):
                self.rewind(t - self.duration)
                self.dispatch_event('on_motion_looped', self)
            else:
                self.stop()
                self.dispatch_event('on_motion_finished', self)
        elif(t < 0):
            self.rewind()
        else:
            self.time = t
        self.update()

    #Probably want to change this to self.set_time
    def on_update(self, dt):
        if self.time < self.duration:
            print "Tick for object", self.name, "current time ", dt
        else:
            print "Finished for", self.name
            self.clock.unschedule(self.on_update)

        self.time += dt

    def start(self):
        #For now just assume that we are using seconds.
        self.rewind()
        pyglet.clock.schedule_interval(self.clock.tick, 1.0/60)
        #self.clock.schedule_interval(self.on_update, 1.0)
        self.clock.schedule_interval(self.next_frame, 1.0/60)
        self.dispatch_event('on_motion_started', self)

    def rewind(self, t=1):
        self.time = t
        self.fix_time()

    def fix_time(self):
        pass

    def stop(self):
        #Perhaps changes this to set_time
        self.clock.unschedule(self.next_frame)
        self.dispatch_event('on_motion_stopped', self)

    def resume(self):
        self.fix_time()
        self.clock.schedule_interval(self.next_frame, 1.0)
        self.dispatch_event('on_motion_resumed', self)

    def fforward(self):
        pass

    def get_time(self):
        return self.time

    def to_string(self):
        return "[motion prop= ", self.prop,  " t= ", self.time, " pos= ", self.position, " ]" 

    def get_position(self, t):
        pass

    def set_position(self, p):
        self.prev_position = self.position 
        self.position      = p
        setattr(self.obj, self.prop, self.position)
        self.dispatch_event('on_motion_changed', self)

    def get_prev_pos(self):
        pass

    def set_begin(self, b):
        pass

    def get_begin(self):
        return self.begin

    def set_duration(self, d):
        if d is None or d <= 0:
            self.duration = -1
        else:
            self.duration = d

    def set_looping(self, b):
        pass

    def get_looping(self):
        pass

    def set_obj(self, obj):
        self.obj = obj

    def get_obj(self):
        return self.obj

    def set_prop(self, p):
        self.prop   = p

    def get_prop(self):
        return self.prop

    def set_use_seconds(self, use_secs):
        self.use_seconds = use_secs

    def get_use_seconds(self):
        return self.use_seconds

#def __init__(self, obj, prop, begin, duration, use_seconds, looping, name):
class Tween(Motion):
    def __init__(self, obj, prop, func, begin, finish, duration, use_seconds, looping=False, name=None):
        #super(Motion, self).__init__(*args, **kwargs)
        self.obj            = obj
        self.func           = func
        self.prop           = prop
        self.begin          = begin
        self.finish         = finish
        self.duration       = duration
        self.position       = begin
        self.prev_position  = None
        self.change         = None
        self.use_seconds    = use_seconds
        self.name           = name
        self.start_time     = None
        self.time           = None # May remove this later
        self.looping        = looping #Might need to change this
        self.clock          = clock.Clock()
        self.register_events()
        self.set_func(func)
        self.set_finish(finish)

    def get_position(self, t=None):
        if(t == None):
            t = self.time
        position = self.func(t, self.begin, self.change, self.duration)
        return position

    def set_func(self, f):
        self.func = f

    def get_func(self):
        return self.func

    def set_change(self, c):
        self.change = c

    def get_change(self):
        return self.change

    def set_finish(self, f):
        self.change = f - self.begin

    def get_finish(self):
        return self.begin + self.change


#window = pyglet.window.Window(width=800,height=600, resizable=True, visible=False)
#window.clear()
#window.set_visible(True)
#m = Motion(window, "something", 0, 12, 3, True, "Test1") 
#m1 = Motion(window, "something", 0, 6, 0.5, False, "Test4") 
#game_data = game.init()
#pyglet.sprite.Sprite(self.game_data['data']['map']['elements']['House01']['Wall6.png'], 0, 0, batch=self.object_batch)
#sprite = pyglet.sprite.Sprite(game_data['data']['agents']['Monster01']['animations']['Monster_Up1.png'], 0, 0)

#def on_draw(self):
#    print "Draw"
#clock.schedule_interval(printPoo, 1.0)
#pyglet.app.run()
