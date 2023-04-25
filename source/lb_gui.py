import pandas as pd
import os
import time
import random

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
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.image import AsyncImage
from lb_main import *



class BladeLearner2049(App):
    def build(self):  
        self.white = (1, 1, 1, 1)
        self.study_options  = ['Option1', 'Option2', 'Option3', 'Option4', 'Option5']
        self.selected_category = None
        self.selected_study_type = None

        def gui_home(instance):
            self.study_options  = mainMapReduce()
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
            
            # setting a popup window on top for home page and buttons
            study_btn.bind(on_press= gui_category)
            #manage_btn.bind(on_press= gui_manage)
            
            home.add_widget(center_line)
            home.add_widget(study_btn)
            home.add_widget(manage_btn)
            popup.title = ' '
            popup.content = home
            popup.open()
        

        def gui_category(instance):
            category = FloatLayout()

            # setting a popup window on top for the page and buttons
            # create a grid of all topics and let user choose
            # create a grid of buttons for each option
            len_option = len(self.study_options)
            if len_option > 20 : len_option = 20
            btn = [0]*len_option
            btn_columns = 4
            btn_size = 0.15
            for i in range(len_option):
                option = self.study_options[i]
                row = i // btn_columns
                col = i % btn_columns
                btn[i] = Button(text=option,
                             background_color=(1, 1, 1, 0.0), 
                             size_hint = (btn_size, btn_size),
                             color=self.white,
                             font_name='Allura_Regular',
                             font_size=35)               
                btn[i].pos_hint = {'x':  0.5 - btn_size*4/2.  + col*(btn_size+0.05)-0.05/2.*(btn_columns-1), 'y': 0.5 + int(len_option/8.)*btn_size - row*0.15 }
                btn[i].bind (on_press=select_category)
                category.add_widget(btn[i])

            return_btn = Button(text='- Return -', 
                                background_color=(1, 1, 1, 0),
                                color=self.white,
                                size_hint=(0.4, 0.1),
                                pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                font_name='Allura_Regular',
                                font_size=25)
            return_btn.bind(on_press=gui_home)
            category.add_widget(return_btn)           

            popup.content = category
            popup.title = 'Available Categories:'

        def select_category(instance):
            if instance.text != ' ':
                # getting the text of a button
                self.selected_category = str(instance.text)
                print(self.selected_category)
                gui_study_type()

        def gui_study_type():
            study_type = FloatLayout()

            center_line = Label(text='____________________________________________',
                                font_size ='18sp', size_hint=(0.2, 0.2),
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})
            center_line.color = (1,1,1,1)

            btn_Study = Button(text='Start Review', 
                                background_color=(1, 1, 1, 0),
                                color=self.white,
                                size_hint=(0.4, 0.07),
                                pos_hint={'center_x': 0.5, 'center_y': 0.525},
                                font_name='Allura_Regular',
                                font_size=45)
            
            btn_common_mistakes = Button(text='Common Mistakes', 
                                background_color=(1, 1, 1, 0),
                                color=self.white,
                                size_hint=(0.4, 0.07),
                                pos_hint={'center_x': 0.5, 'center_y': 0.45},
                                font_name='Allura_Regular',
                                font_size=25)
            
            btn_home = Button(text='- Home -', 
                                background_color=(1, 1, 1, 0),
                                color=self.white,
                                size_hint=(0.4, 0.1),
                                pos_hint={'center_x': 0.4, 'center_y': 0.1},
                                font_name='Allura_Regular',
                                font_size=25)

            return_btn = Button(text='- Return -', 
                                background_color=(1, 1, 1, 0),
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

            return_btn.bind(on_press=gui_category)
            study_type.add_widget(return_btn)          

            popup.content = study_type
            popup.title = ' '

        def gui_normal_study(instance):
            mainStudy(self.selected_category, 0)
            print('0') 
                    

        def gui_common_mistakes(instance):
            mainStudy(self.selected_category, 1)
            print('1') 
            

        def gui_read_card(row):
            study_type = FloatLayout()

            center_line = Label(text='____________________________________________',
                                font_size ='18sp', size_hint=(0.2, 0.2),
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})
            center_line.color = (1,1,1,1)

            btn_Study = Button(text='Start Review', 
                                background_color=(1, 1, 1, 0),
                                color=self.white,
                                size_hint=(0.4, 0.07),
                                pos_hint={'center_x': 0.5, 'center_y': 0.525},
                                font_name='Allura_Regular',
                                font_size=45)
            
            btn_common_mistakes = Button(text='Common Mistakes', 
                                background_color=(1, 1, 1, 0),
                                color=self.white,
                                size_hint=(0.4, 0.07),
                                pos_hint={'center_x': 0.5, 'center_y': 0.45},
                                font_name='Allura_Regular',
                                font_size=25)
            
            btn_home = Button(text='- Home -', 
                                background_color=(1, 1, 1, 0),
                                color=self.white,
                                size_hint=(0.4, 0.1),
                                pos_hint={'center_x': 0.4, 'center_y': 0.1},
                                font_name='Allura_Regular',
                                font_size=25)

            return_btn = Button(text='- Return -', 
                                background_color=(1, 1, 1, 0),
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

            return_btn.bind(on_press=gui_category)
            study_type.add_widget(return_btn)          

            popup.content = study_type
            popup.title = ' '
            #Setting a popup window on top for the page and buttons
            card_btn.bind(on_press= gui_revealed_card())
            btn_return.bind(on_press= gui_study_type())
            btn_home.bind(on_press= gui_home(self.study_options))
            
        def gui_revealed_card():
            # update last pop 
            # setting a popup window on top for the page and buttons

            # Create a button that sets the parameter to "Hello"
            btn_yes = Button(root, text="Yes", command=lambda: mainStudy(self.chosen_category, 1) )
            btn_yes.pack()

            # Create a button that sets the parameter to "World"
            btn_no = Button(root, text="No", command=lambda: mainStudy(self.chosen_category, 1) )
            btn_no.pack()

            yes_btn.bind(on_press= gui_yes())
            no_btn.bind(on_press= gui_no())


        def gui_yes():
            self.answer = 1

        def gui_no():
            self.answer = 0


        def button_empty(instance):
            # fake buttons bid func. for other buttons which act as label with back ground , ...
            value = 0




        

        # build GUI background page
        layout = FloatLayout(size=(1200, 1600), size_hint=(1, 1))

        bg = FloatLayout(size_hint=(1, 1))
        address = '../images/image'+str(random.randint(1, 18))+'.jpg'
        img_bg = AsyncImage(source=address, pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        bg.add_widget(img_bg)
        popup_bg = Popup(title=' ', content=bg, auto_dismiss=False, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        popup_bg.open()

        popup = Popup(title=' ', content=layout, auto_dismiss=False, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        # create funtion to change color based on hour of day
        color_pop = ((35 / 255.) + 0.5, (110 / 255.) + 0.5, (150 / 255.) + 0.5, 0.5)
        popup.background_color = color_pop


        gui_home('1')
        return layout


        
        '''
        btn = Button(text='____________________________________________',
                    
                    background_color=(0.4, 0.4, 0.4, 0.93),
                    color=(1, 1, 1, 0.9),
                    size_hint=(bsh_x, bsh_y),
                    pos_hint={'center_x': x_pos, 'center_y': y_pos})
                    

        btn.bind(on_press=button_empty)

        layout.add_widget(btn)
        '''
        return layout

if __name__ == '__main__':
    BladeLearner2049().run()
    # here buid is automatically will run



