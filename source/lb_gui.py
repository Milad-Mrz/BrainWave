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

            self.study_options #input list
            self.chosen_category = chosen_category # output
            gui_study_type()
            btn_return.bind(on_press= gui_home(self.study_options))



        def gui_study_type():
            # close last pop 
            # setting a popup window on top for the page and buttons

            btn2.bind(on_press= gui_normal_study)
            btn3.bind(on_press= gui_common_mistakes())

            btn_return.bind(on_press= gui_category())
            btn_home.bind(on_press= gui_home(self.study_options))




        def gui_normal_study():
            # setting parameters
            btn_return.bind(on_press= gui_study_type())
            btn_home.bind(on_press= gui_home(self.study_options))
            
            mainStudy(self.chosen_category, 1)            
            gui_read_card()


        def gui_common_mistakes():
            # setting parameters
            btn_return.bind(on_press= gui_study_type())
            btn_home.bind(on_press= gui_home(self.study_options))
            
            mainStudy(self.chosen_category, 1)
            gui_read_card()

        def gui_read_card():
            
            card_btn.bind(on_press= gui_revealed_card())
            btn_return.bind(on_press= gui_study_type())
            btn_home.bind(on_press= gui_home(self.study_options))

        # if mistake == 1 : 
            
        def gui_revealed_card():
            yes_btn.bind(on_press= gui_yes())
            no_btn.bind(on_press= gui_no())


        def gui_yes():
            self.answer = 1

        def gui_no():
            self.answer = 0


        # fake buttons bid func. for other buttons which act as label with back ground , ...
        def button_fake(instance):
            fake_value = 0  # --------------------------------------

        layout = FloatLayout(size=(450, 850), size_hint=(1, 1))

        address0 = 'BG/1.jpg'
        img_bg = AsyncImage(source=address0, pos_hint={'left': 1, 'top': 1}, size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        layout.add_widget(img_bg)

        bsh_x = 0.5
        bsh_y = 0.3

        x_pos = 0.5
        y_pos = 0.5

        btn = Button(text=' ',
                     background_color=(0.4, 0.4, 0.4, 0.93),
                     color=(1, 0, 0, 0.9),
                     size_hint=(bsh_x, bsh_y),
                     pos_hint={'center_x': x_pos, 'center_y': y_pos})

        btn.bind(on_press=button_fake)

        layout.add_widget(btn)
        return layout

if __name__ == '__main__':
    Float_Layout().run()


df, df_temp = select_course("data.csv")
data_rev, len_mis, len_rev, len_new, len_001, len_003, len_007, len_015, len_030, len_060, len_120 = data_monitor(df)
df = study(df, data_rev)
data_writer(df, df_temp)



