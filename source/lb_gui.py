import pandas as pd
import random
import time

import kivy
from kivy.app import App
from kivy.app import App
from kivy.uix.button import Button
kivy.require('1.9.0')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.uix.widget import Widget

from lb_main import *


class BrainFlash(App):
    def build(self):  
        self._keyboard = None
        self.flag = None

        self.black = (0, 0, 0, 1)
        self.white = (1, 1, 1, 1)
        self.hide =  (1, 1, 1, 0)

        self.study_options  = ['Option1', 'Option2', 'Option3', 'Option4', 'Option5']
        self.selected_category = None
        self.common_mistake = None
        self.data_frame = None
        self.row = None
        self.result = None
        self.reveal_active = 0
        self.answer = None
        self.study_subset = []

        

        def gui_home(instance):
            

            # setting  main window features
            home = FloatLayout()

            #create central line
            center_line = Label(text='____________________________________________',
                                font_size ='18sp', size_hint=(0.2, 0.2),
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})
            center_line.color = (1,1,1,1)

            study_btn = Button(text='Study Cards', 
                        background_color=(1, 1, 1, 0),
                        color=self.white,
                        size_hint=(0.4, 0.07),
                        pos_hint={'center_x': 0.5, 'center_y': 0.54},
                        font_name='Allura_Regular',
                        font_size=45)
            
            manage_btn = Button(text='Manage Cards', 
                        background_color=(1, 1, 1, 0),
                        color=self.white,
                        size_hint=(0.4, 0.07),
                        pos_hint={'center_x': 0.5, 'center_y': 0.45},
                        font_name='Allura_Regular',
                        font_size=20)
            
            address = '../images/1cards.png'
            img_bg1 = AsyncImage(source=address, pos_hint={'center_x': 0.5, 'center_y': 0.62}, size_hint=(0.08, 0.08), allow_stretch=False, keep_ratio=False)
            home.add_widget(img_bg1)
            img_bg1.opacity = 1

            #BrainFlash
            
            # setting a popup window on top for home page and buttons
            study_btn.bind(on_press= gui_category)
            
            home.add_widget(center_line)
            home.add_widget(study_btn)
            home.add_widget(manage_btn)
            popup.title = 'BrainFlash - 2023-05 - v0.0.1'
            popup.content = home
            popup.open()
        
        def gui_category(instance):
            self.study_options, self.data_frame  = mainMapReduce()
            category = FloatLayout()



            address = '../images/1paper_2.png'
            img_bg3 = AsyncImage(source=address, pos_hint={'center_x': 0.6, 'center_y': 0.5}, size_hint=(1, 1), allow_stretch=False, keep_ratio=False)
            category.add_widget(img_bg3)
            img_bg3.opacity = 0.4

            address = '../images/1paper_2.png'
            img_bg3 = AsyncImage(source=address, pos_hint={'center_x': 0.55, 'center_y': 0.5}, size_hint=(1, 1), allow_stretch=False, keep_ratio=False)
            category.add_widget(img_bg3)
            img_bg3.opacity = 0.6

            address = '../images/1paper_2.png'
            img_bg3 = AsyncImage(source=address, pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(1, 1), allow_stretch=False, keep_ratio=False)
            category.add_widget(img_bg3)


            # setting a popup window on top for the page and buttons
            # create a grid of all topics and let user choose
            # create a grid of buttons for each option
            #‍‍‍‍self.study_options  = ['Option1', 'Option2', 'Option3', 'Option4', 'Option5', 'Option1', 'Option2', 'Option3', 'Option4', 'Option5']
            len_option = len(self.study_options)
            if len_option > 10 : len_option = 10
            btn = [0]*len_option
            btn_columns = 4
            btn_size = 0.15 
            res = len_option % btn_columns  

            for i in range(len_option):
                option = ">" + self.study_options[i] + "<"
                row = i // btn_columns
                col = i % btn_columns
                btn[i] = Button(text=option,
                             background_color=(1,1,1,0.0), 
                             size_hint = (btn_size, btn_size),
                             color=self.black,
                             font_name='Allura_Regular',
                             font_size=35)   
                
                xpos = 0.4 - btn_size*4/2.  + col*(btn_size+0.05)-0.05/2.*(btn_columns-1) + random.uniform(-0.03, 0.03)
                if i >= (len_option - res): xpos = (0.5-(res*btn_size/2))+(i-len_option+res)*(btn_size+0.05) + random.uniform(-0.03, 0.03)  

                btn[i].pos_hint = {'x': xpos, 'y': 0.4 + (len_option//(btn_columns*2) - row) * (btn_size + 0.05) + random.uniform(-0.04, 0.04) }

                btn[i].bind (on_press=select_category)
                category.add_widget(btn[i])

            btn_return = Button(text='- Return -', 
                                background_color=self.hide,
                                color=self.black,
                                size_hint=(0.4, 0.1),
                                pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                font_name='Allura_Regular',
                                font_size=30)
            
            if len(self.study_options) == 0 : 
                btn_return.text = '                Right now, \n there is no material available,\n                 to study \n\n   - Please check your material -'
                btn_return.size_hint=(0.6, 0.6)                   
                btn_return.pos_hint={'center_x': 0.5, 'center_y': 0.5}
                btn_return.font_size=35
            
            btn_return.bind(on_press=gui_home)
            category.add_widget(btn_return)           

            popup.content = category
            popup.title = 'Available Categories:'

        def select_category(instance):
            if instance.text != ' ': 
                # getting the text of a button and remove extra symbols
                self.selected_category = (str(instance.text))[1:-1]
                gui_study_type()

        def gui_study_type():
            self.study_subset = []

            study_type = FloatLayout()

            address = '../images/1paper_1.png'
            img_bg4 = AsyncImage(source=address, pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(1, 1), allow_stretch=False, keep_ratio=False)
            study_type.add_widget(img_bg4)
            img_bg4.opacity = 0.6

            center_line = Label(text='____________________________________________',
                                font_size ='18sp', size_hint=(0.2, 0.2),
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})
            center_line.color = self.black

            btn_Study = Button(text='Start Review', 
                                background_color=self.hide,
                                color=self.black,
                                size_hint=(0.4, 0.07),
                                pos_hint={'center_x': 0.5, 'center_y': 0.525},
                                font_name='Allura_Regular',
                                font_size=45)
            
            btn_common_mistakes = Button(text='Common Mistakes', 
                                background_color=self.hide,
                                color=self.black,
                                size_hint=(0.4, 0.07),
                                pos_hint={'center_x': 0.5, 'center_y': 0.45},
                                font_name='Allura_Regular',
                                font_size=25)
            
            btn_home = Button(text='- Home -', 
                                background_color=self.hide,
                                color=self.white,
                                size_hint=(0.4, 0.1),
                                pos_hint={'center_x': 0.4, 'center_y': 0.1},
                                font_name='Allura_Regular',
                                font_size=25)

            btn_return = Button(text='- Return -', 
                                background_color=self.hide,
                                color=self.white,
                                size_hint=(0.4, 0.1),
                                pos_hint={'center_x': 0.6, 'center_y': 0.1},
                                font_name='Allura_Regular',
                                font_size=25)
            
            study_type.add_widget(center_line)
            
            btn_Study.bind(on_press=gui_normal_study)
            study_type.add_widget(btn_Study)  

            btn_common_mistakes.bind(on_press=gui_common_mistakes)
            study_type.add_widget(btn_common_mistakes) 

            btn_home.bind(on_press=gui_home)
            study_type.add_widget(btn_home) 

            btn_return.bind(on_press=gui_category)
            study_type.add_widget(btn_return)          

            popup.content = study_type
            popup.title = ' '

        def gui_normal_study(instance):
            self.common_mistake = 0
            df = self.data_frame
            if len(self.study_subset) == 0 :
                self.study_subset = df[(df['Category'] == self.selected_category) & (df['TimeNextREV'] < int(time.time() / 60.)) ]
            else:
                gui_read_card()            

        def gui_common_mistakes(instance):
            self.common_mistake = 1
            df = self.data_frame
            if len(self.study_subset) == 0 :
                self.study_subset = df[(df['Category'] == self.selected_category) & (df['MistakeNo'] > 2) & (df['TimeNextREV'] < int(time.time() / 60.)) ]
            else:               
                gui_read_card()   

        def gui_record():
            text0 = ''
            boxlist = [0, 1, 3, 7, 15, 30, 60, 120]
            for boxID in boxlist:
                status = self.data_frame[(self.data_frame['BoxNo'] == boxID) & (self.data_frame['Category'] == self.selected_category)]
                text0 += '[' + str(boxID) + '] '+ str(len(status)) + '  |' 
            



            record = 'B-' + str(int((self.row['BoxNo'].values)[0])) + ' |' + text0
            return record
            

        def gui_read_card():

            gui_read_card.flag = 0
            #read a random row
            # show the card on gui and run the question and apply lietner data
            self.study_subset = self.study_subset[(self.study_subset['TimeNextREV'] < int(time.time() / 60.)) ]
            print(len(self.study_subset))
            print(self.study_subset)

            if len(self.study_subset) > 0: 
                self.row = self.study_subset.sample()
                #self.study_subset.drop(self.row)
                

            sideA = (self.row['SideA'].values)[0]
            sideB = (self.row['SideB'].values)[0]
            source = str(self.selected_category) + ' --> '

            if (self.row['ActiveSide'].values)[0] == 1 : 
                sideA = (self.row['SideB'].values)[0]
                sideB = (self.row['SideA'].values)[0]
                source = '--> ' + str(self.selected_category)

            MistakeN = int((self.row['MistakeNo'].values)[0])

            if MistakeN <= 1: difficulty = 'Easy'
            if MistakeN > 1:  difficulty = 'Normal'
            if MistakeN > 4:  difficulty = 'High'


            record = gui_record()


            record = source + '?    -    Difficulty:   ' + difficulty + '\n-------------------------------------------------------------------------------\n' + record

            

            read_card = FloatLayout()

            address = '../images/1paper_1.png'
            img_bg5 = AsyncImage(source=address, pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(1, 1), allow_stretch=False, keep_ratio=False)
            read_card.add_widget(img_bg5)
            img_bg5.opacity = 1

            btn_card = Button(text= sideA, 
                                background_color=self.hide,
                                color=self.black,
                                size_hint=(0.4, 0.2),
                                pos_hint={'center_x': 0.5, 'center_y': 0.65},
                                
                                font_size=30)
            
            btn_answer = Button(text= sideB,
                                background_color=self.black,
                                color = self.white,
                                opacity = 0.0,
                                size_hint=(0.4, 0.2),
                                pos_hint={'center_x': 0.5, 'center_y': 0.50},
                                font_size=30)
            
            
            btn_record = Button(text= record, 
                                background_color=self.hide,
                                color=self.black,
                                size_hint=(0.7, 0.07),
                                pos_hint={'center_x': 0.5, 'center_y': 0.31},
                                font_name='Allura_Regular',
                                font_size=17)
            
            btn_home = Button(text= '- Home -', 
                                background_color=self.hide,
                                color=self.white,
                                size_hint=(0.4, 0.1),
                                pos_hint={'center_x': 0.4, 'center_y': 0.1},
                                font_name='Allura_Regular',
                                font_size=25)

            btn_return = Button(text='- Return -', 
                                background_color=self.hide,
                                color=self.white,
                                size_hint=(0.4, 0.1),
                                pos_hint={'center_x': 0.6, 'center_y': 0.1},
                                font_name='Allura_Regular',
                                font_size=25)
            
            btn_yes = Button(text= '< Yes >', 
                                background_color=self.hide,
                                color=self.hide,
                                size_hint=(0.1, 0.1),
                                pos_hint={'center_x': 0.8, 'center_y': 0.55},
                                font_name='Allura_Regular',
                                font_size=20)
            
            btn_no = Button(text= '< No >', 
                                background_color=self.hide,
                                color=self.hide,
                                size_hint=(0.1, 0.1),
                                pos_hint={'center_x': 0.8, 'center_y': 0.45},
                                font_name='Allura_Regular',
                                font_size=20)
            

            def _keyboard_closed(self):
                self._keyboard.unbind(on_key_down=_on_keyboard_down)
                self._keyboard = None

            def _on_keyboard_down(self, keyboard, keycode, text):
                reader = gui_read_card
                #print(keycode)

                if keycode == ' ' and reader.flag == 1:
                    reader.flag = 2
                    gui_reveal_card(1)

                if keycode == 'p' and reader.flag == 2:
                    reader.flag = 0
                    gui_yes(1)

                if keycode == 'm' and reader.flag == 2:
                    reader.flag = 0
                    gui_no(1)
                # Return True to accept the key. Otherwise, it will be used by
                # the system.
                return True
            
            if self._keyboard == None :
                self._keyboard = Window.request_keyboard(_keyboard_closed, self, 'text')

                
            def gui_reveal_card(instance):
                btn_answer.opacity = 0.8
                btn_yes.color = self.white
                btn_no.color = self.white
                btn_yes.background_color=self.black
                btn_no.background_color=self.black
                btn_card.bind(on_press=gui_pass)

            def gui_yes(instance):
                btn_answer.opacity = 0
                btn_card.text = ' '
                self.answer = 1
                btn_yes.color = self.hide
                btn_no.color = self.hide 
                self.result = mainLietner(self.row, 1)
                self.study_subset.update(self.result)
                self.data_frame.update(self.result)
                mainDataWriter(self.data_frame)
                if len(self.study_subset) > 1: 
                    gui_read_card()
                else:
                    b_return(0)
                


            def gui_no(instance):
                btn_answer.opacity = 0
                btn_card.text = ' '
                self.answer = 0
                btn_yes.color = self.hide
                btn_no.color = self.hide 
                self.result = mainLietner(self.row, 0)
                self.study_subset.update(self.result)
                self.data_frame.update(self.result)
                mainDataWriter(self.data_frame)
                if len(self.study_subset) > 1: 
                    gui_read_card()
                else:
                    b_return(0)

            def gui_pass(instance):
                pass


            def b_home(instance):
                mainDataWriter(self.data_frame)
                gui_read_card.flag = 0
                gui_home(0)

            def b_return(instance):
                mainDataWriter(self.data_frame)
                gui_read_card.flag = 0
                gui_category(0)

            
            read_card.add_widget(btn_answer)
            read_card.add_widget(btn_record) 
            
            btn_card.bind(on_press=gui_reveal_card)
            read_card.add_widget(btn_card)  

            btn_home.bind(on_press=b_home)
            read_card.add_widget(btn_home) 

            btn_return.bind(on_press=b_return)
            read_card.add_widget(btn_return)  

            btn_yes.bind(on_press=gui_yes)
            read_card.add_widget(btn_yes)

            btn_no.bind(on_press=gui_no)
            read_card.add_widget(btn_no)  

            

            popup.content = read_card
            popup.title = 'Hint:   <Space> -> Reveal the card    ||    <P> -> yes!    ||    <M> -> No! '

            self._keyboard.bind(on_key_down=_on_keyboard_down)
            gui_read_card.flag = 1
            
            return

        
        



        # build GUI background page
        layout = FloatLayout(size=(1200, 1600), size_hint=(1, 1))

        bg = FloatLayout(size_hint=(1, 1))
        address = '../images/image'+str(random.randint(1, 18))+'.jpg'
        img_bg = AsyncImage(source=address, pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(1, 1), allow_stretch=False, keep_ratio=False)
        bg.add_widget(img_bg)
        popup_bg = Popup(title=' ', content=bg, auto_dismiss=False, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        popup_bg.open()

        popup = Popup(title=' ', content=layout, auto_dismiss=False, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        # create funtion to change color based on hour of day
        color_pop = ((35 / 255.) + 0.5, (110 / 255.) + 0.5, (150 / 255.) + 0.5, 0.5)
        popup.background_color = color_pop


        gui_home(1)
        return layout

if __name__ == '__main__':
    BrainFlash().run()
    # here buid is automatically will run