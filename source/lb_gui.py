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


        
        def gui_home():
            # setting  main window features

            study_options  = mainMapReduce()
            self.study_options = study_options

            # setting a popup window on top for home page and buttons

            study_btn.bind(on_press= gui_Category())
            manage_btn.bind(on_press= gui_manage())


        
        def gui_category():
            # close last pop 
            # setting a popup window on top for the page and buttons
            # create a grid of all topics and let user choose


            self.study_options #input list
            self.chosen_category = chosen_category # output
            gui_study_type()

            btn_return.bind(on_press= gui_home(self.study_options))



        def gui_study_type():
            # close last pop 
            # setting a popup window on top for the page and buttons

            # Create a button that sets the parameter to "Hello"
            btn_Study = Button(text="Study", command=lambda: mainStudy(self.chosen_category, 0) )

            # Create a button that sets the parameter to "World"
            btn_common_mistakes = Button(text="Common Mistakes", command=lambda: mainStudy(self.chosen_category, 1) )


            btn_return.bind(on_press= gui_category())
            btn_home.bind(on_press= gui_home(self.study_options))

            pop_study_type.add_widget(btn_nxt)




        def gui_normal_study():
            # close last pop 
            # setting parameters



            btn_return.bind(on_press= gui_study_type())
            btn_home.bind(on_press= gui_home(self.study_options))
            
            mainStudy(self.chosen_category, 1)            


        def gui_common_mistakes():
            # close last pop 
            # setting parameters
            btn_return.bind(on_press= gui_study_type())
            btn_home.bind(on_press= gui_home(self.study_options))
            
            mainStudy(self.chosen_category, 1)
            gui_read_card()

        def gui_read_card():
            # close last pop 
            # setting a popup window on top for the page and buttons
            card_btn.bind(on_press= gui_revealed_card())
            btn_return.bind(on_press= gui_study_type())
            btn_home.bind(on_press= gui_home(self.study_options))

        # if mistake == 1 : 
            
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
        layout = FloatLayout(size=(600, 800), size_hint=(1, 1))

        img_bg = AsyncImage(source='../images/1.jpg', pos_hint={'left': 1, 'top': 1}, size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        layout.add_widget(img_bg)

        bsh_x = 0.95
        bsh_y = 0.9

        x_pos = 0.5
        y_pos = 0.5

        

        btn = Button(text='____________________________________________',
                     
                     background_color=(0.4, 0.4, 0.4, 0.93),
                     color=(1, 1, 1, 0.9),
                     size_hint=(bsh_x, bsh_y),
                     pos_hint={'center_x': x_pos, 'center_y': y_pos})
                    

        btn.bind(on_press=button_empty)

        layout.add_widget(btn)

        return layout

if __name__ == '__main__':
    BladeLearner2049().run()
    # here buid is automatically will run



