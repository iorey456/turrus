#import modules
import time
from machine import Pin
from dfplayer import DFPlayer


class Music:
    
    def __init__(self):
        self.current_music = 0
        self.music_playing = False
        self.button = Pin(15, Pin.IN,Pin.PULL_UP)
        self.changing_button = Pin(22, Pin.IN,Pin.PULL_UP)
        self.df = DFPlayer(uart_id=1,tx_pin_id=4,rx_pin_id=5)
        time.sleep(1)
        self.numbers_of_music = self.df.get_files_in_folder(1) - 3
        print(self.numbers_of_music)
        #self.df.play(4,self.numbers_of_music - 1)
        time.sleep(1)
        self.df.volume(30)
        
    def boot_sound(self):
        self.df.play(3,2)
        
    def play_music(self):
        self.df.volume(27)
        self.df.play(1,self.current_music)
       
    def play_announce(self):
        self.df.volume(30)
        time.sleep(2)
        self.df.play(2,1)
    
    def playing_button_state(self):
        return self.button.value() == False
    
    def is_playing(self):
        try:
            return self.df.is_playing()
        except IndexError:
            return False
        
    def playing_button_observer(self):
        if self.playing_button_state() == True and self.is_playing() == False:
            print('button pressed!')
            self.play_music()
            self.music_playing = True
        if self.playing_button_state() == False and self.music_playing == True and self.is_playing() == True:
            self.music_playing = False
            self.df.stop()
            self.play_announce()
            
    def changing_button_observer(self):
        if self.changing_button.value() == False:
            self.current_music += 1
            if self.current_music > self.numbers_of_music:
                self.current_music = 0
            #self.df.play(3,1)
            self.df.play(4,self.current_music)
            print("music =", self.current_music)
            
    def main(self):
        time.sleep(1)
        while True:
            time.sleep(0.5)
            self.changing_button_observer()
            self.playing_button_observer()
            
            
#main program
music = Music()
music.boot_sound()
music.main()








