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



class Float_Layout(App):
    def build(self):
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



