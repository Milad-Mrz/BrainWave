from gtts import gTTS
import vlc
import time

def tts_en(text, play=1):

    main_list = []
    with open('dl-voices-en/list.txt', 'r') as data0:
        for line0 in data0:
            main_list.append(line0.strip())
        # print(main_list)

    if text in main_list:
        id0 = [main_list.index(text)]
        file_name = 'dl-voices-en/' + str(id0[0]) + '.mp3'
        if play == 1:
            p0 = vlc.MediaPlayer(file_name)
            p0.play()
    else:
        with open('dl-voices-en/list.txt', 'a') as data0:
            # language = 'en-gb'
            language = 'en-au'
            my_obj = gTTS(text=text, lang=language, slow=False)
            time.sleep(1)
            id0 = len(main_list)
            data0.write(text + '\n')
            file_name = 'dl-voices-en/' + str(id0) + '.mp3'

            my_obj.save(file_name)
            if play == 1:
                p0 = vlc.MediaPlayer(file_name)
                p0.play()
            main_list.append(text)



mode0_temp = 'vp1'
enw_0 = []

with open('word_source/'+mode0_temp+'_en.txt', 'r') as enw:
    for temp0 in enw:
        enw_0.append(temp0.strip())

idx = 0
idt = len(enw_0)
for text0 in enw_0:
    idx += 1
    tts_en(text0, play=0)
    print(round(idx/idt*100,2))
