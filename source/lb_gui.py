import pandas as pd
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
            self.study_options, self.data_frame  = mainMapReduce()
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
                             background_color=self.hide, 
                             size_hint = (btn_size, btn_size),
                             color=self.white,
                             font_name='Allura_Regular',
                             font_size=35)               
                btn[i].pos_hint = {'x':  0.5 - btn_size*4/2.  + col*(btn_size+0.05)-0.05/2.*(btn_columns-1), 'y': 0.5 + int(len_option/8.)*btn_size - row*0.15 }
                btn[i].bind (on_press=select_category)
                category.add_widget(btn[i])

            btn_return = Button(text='- Return -', 
                                background_color=self.hide,
                                color=self.white,
                                size_hint=(0.4, 0.1),
                                pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                font_name='Allura_Regular',
                                font_size=25)
            btn_return.bind(on_press=gui_home)
            category.add_widget(btn_return)           

            popup.content = category
            popup.title = 'Available Categories:'

        def select_category(instance):
            if instance.text != ' ':
                # getting the text of a button
                self.selected_category = str(instance.text)
                #print(self.selected_category)
                gui_study_type()

        def gui_study_type():
            study_type = FloatLayout()

            center_line = Label(text='____________________________________________',
                                font_size ='18sp', size_hint=(0.2, 0.2),
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})
            center_line.color = (1,1,1,1)

            btn_Study = Button(text='Start Review', 
                                background_color=self.hide,
                                color=self.white,
                                size_hint=(0.4, 0.07),
                                pos_hint={'center_x': 0.5, 'center_y': 0.525},
                                font_name='Allura_Regular',
                                font_size=45)
            
            btn_common_mistakes = Button(text='Common Mistakes', 
                                background_color=self.hide,
                                color=self.white,
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
                if len(self.study_subset) == 0 :
                    #exit and write
                    mainDataWriter(self.data_frame) 
            else:
                gui_read_card(0)            


        def gui_common_mistakes(instance):
            self.common_mistake = 1
            df = self.data_frame
            if len(self.study_subset) == 0 :
                self.study_subset = df[(df['Category'] == self.selected_category) & (df['MistakeNo'] > 2) & (df['TimeNextREV'] < int(time.time() / 60.)) ]
                if len(self.study_subset) == 0 :
                    #exit and write
                    mainDataWriter(self.data_frame) 
            else:               
                gui_read_card(0)            
                

        def gui_read_card(instance):
            #read a random row
            # show the card on gui and run the question and apply lietner data
            self.row = self.study_subset.sample()
            # update the row in main df and remove the row from subset 

            sideA = (self.row['SideA'].values)[0]
            sideB = (self.row['SideB'].values)[0]
            #print(sideA,sideB)
            if (self.row['ActiveSide'].values)[0] == 1 : 
                sideA = (self.row['SideB'].values)[0]
                sideB = (self.row['SideA'].values)[0]

            record = '[ Box - ' + str((self.row['BoxNo'].values)[0]) + ' ]'

            read_card = FloatLayout()

            center_line = Label(text= '____________________________________________',
                                font_size ='18sp', size_hint=(0.2, 0.2),
                                pos_hint={'center_x': 0.5, 'center_y': 0.75})
            center_line.color = (1,1,1,1)

            center_line2 = Label(text= '____________________________________________',
                                font_size ='18sp', size_hint=(0.2, 0.2),
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})
            center_line.color = (1,1,1,1)

            btn_card = Button(text= sideA, 
                                background_color=self.hide,
                                color=self.white,
                                size_hint=(0.4, 0.1),
                                pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                font_name='Allura_Regular',
                                font_size=45)
            
            btn_record = Button(text= record, 
                                background_color=self.hide,
                                color=self.white,
                                size_hint=(0.4, 0.07),
                                pos_hint={'center_x': 0.5, 'center_y': 0.3},
                                font_name='Allura_Regular',
                                font_size=20)
            
            btn_home = Button(text= '- Home -', 
                                background_color=self.hide,
                                color=self.white,
                                size_hint=(0.4, 0.1),
                                pos_hint={'center_x': 0.4, 'center_y': 0.1},
                                font_name='Allura_Regular',
                                font_size=25)

            btn_return = Button(text= '- Return -', 
                                background_color=self.hide,
                                color=self.white,
                                size_hint=(0.4, 0.1),
                                pos_hint={'center_x': 0.6, 'center_y': 0.1},
                                font_name='Allura_Regular',
                                font_size=25)
            
            
            btn_yes = Button(text= '< Yes >', 
                                background_color=self.hide,
                                color=self.hide,
                                size_hint=(0.4, 0.1),
                                pos_hint={'center_x': 0.7, 'center_y': 0.65},
                                font_name='Allura_Regular',
                                font_size=25)
            
            btn_no = Button(text= '< No >', 
                                background_color=self.hide,
                                color=self.hide,
                                size_hint=(0.4, 0.1),
                                pos_hint={'center_x': 0.7, 'center_y': 0.55},
                                font_name='Allura_Regular',
                                font_size=25)
                
            def gui_reveal_card(instance):
                btn_card.text = sideB
                btn_yes.color = self.white
                btn_no.color = self.white
                btn_card.bind(on_press=gui_pass)

            def gui_yes(instance):
                self.answer = 1
                btn_yes.color = self.hide
                btn_no.color = self.hide 
                self.result = mainLietner(self.row, 1)
                self.data_frame.update(self.result)
                mainDataWriter(self.data_frame)
                if self.common_mistake == 1:
                    gui_common_mistakes()         
                else:
                    gui_normal_study()


            def gui_no(instance):
                self.answer = 0
                btn_yes.color = self.hide
                btn_no.color = self.hide 
                self.result = mainLietner(self.row, 0)
                self.data_frame.update(self.result)
                mainDataWriter(self.data_frame)
                if self.common_mistake == 1:
                    gui_common_mistakes()         
                else:
                    gui_normal_study()

            def gui_pass(instance):
                pass


            def b_home(instance):
                mainDataWriter(self.data_frame)
                gui_home()

            def b_return(instance):
                mainDataWriter(self.data_frame)
                gui_category()


            read_card.add_widget(center_line)
            read_card.add_widget(center_line2)
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
            popup.title = ' '

            return


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



