import os
from pocketsphinx import LiveSpeech, get_model_path
import time
#import RPi.GPIO as GPIOpi
from gpiozero import PWMOutputDevice

class Motor_Control():
    def initialize(self):
        self.rightf = PWMOutputDevice(12, True, 0, 1000)
        self.rightr = PWMOutputDevice(13, True, 0, 1000)
        self.leftf = PWMOutputDevice(14, True, 0, 1000)
        self.leftr = PWMOutputDevice(15, True, 0, 1000)
        self.speedr = 0
        self.speedl = 0
        self.offsetr = 0
        self.offsetl = 0
        self.speedmax = 1
        print("start motor")

    def right(self):
        if self.speedr == 0:
            self.speedr = self.speedr*1.2
        else:
            self.speedr = 0.10
            self.speedl = -0.10
        self.go()

    def left(self):
        if self.speedl == 0:
            self.speedr = self.speedl*1.2
        else:
            self.speedr = 0.10
            self.speedl = -0.10
        self.go()
    
    def forward(self):
        if self.speedl == 0 and self.speedr == 0:
            self.speedr = self.speedmax
            self.speedl = self.speedmax
            self.go()
        elif self.speedl < self.speedr and self.speedl > 0 and self.speedr > 0:
            self.speedl = self.speedr
            self.go()
        elif self.speedl > self.speedr and self.speedl > 0 and self.speedr > 0:
            self.speedr = self.speedl
            self.go()
        else:
            self.stop()
    
    def backward(self):
        if self.speedl == 0 and self.speedr == 0:
            self.speedr = -self.speedmax
            self.speedl = -self.speedmax
            self.go()
        elif self.speedl > self.speedr and self.speedl < 0 and self.speedr < 0:
            self.speedl = self.speedr
            self.go()
        elif self.speedl < self.speedr and self.speedl < 0 and self.speedr < 0:
            self.speedr = self.speedl
            self.go()
        else:
            self.stop()

    def faster(self):
        self.speedr = self.speedr*1.5
        self.speedl = self.speedl*1.5
        self.go()

    def slower(self):
        self.speedr = self.speedr*0.5
        self.speedl = self.speedl*0.5
        self.go()

    def stop(self):
        self.speedl = 0
        self.speedr = 0
        self.go()

    def go(self):
        if self.speedr > self.speedmax:
            self.speedr = self.speedmax
        if self.speedl > self.speedmax:
            self.speedl = self.speedmax
        if self.speedr >= 0:
            self.rightf.value = self.speedr
        if self.speedr <= 0:
            self.rightr.value = self.speedr
        if self.speedl >= 0:
            self.leftf.value = self.speedl
        if self.speedl <= 0:
            self.leftr.value = self.speedl
        print("speedr "+self.speedr+" speedl "+self.speedl)

# = get_model_path()
model_path = "/usr/local/share/pocketsphinx/model/de/"
print("model_path: "+model_path)

#print(str(Motor_Control.stop))

speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    #hmm=os.path.join(model_path, 'en-us'),
    #lm=os.path.join(model_path, 'en-us.lm.bin'),
    #dic=os.path.join(model_path, 'cmudict-en-us.dict')
    hmm=os.path.join(model_path, 'de'),
    lm=os.path.join(model_path, 'de.lm'),
    dic=os.path.join('/home/andreas/rc-car-control/', 'car.dict')
)
for phrase in speech:
    print("pharse: ("+str(phrase)+")")
    if str(phrase) == "stopp":
        #print("stopp")
        print(Motor_Control.stop)
    elif str(phrase) == "vorwärts":
        #print("forward")
        print(Motor_Control.forward)
    elif str(phrase) == "rückwärts":
        #print("backward")
        print(Motor_Control.backward)
    elif str(phrase) == "schneller":
        #print("faster")
        print(Motor_Control.faster)
    elif str(phrase) == "langsamer":
        #print("slower")
        print(Motor_Control.slower)
    elif str(phrase) == "links":
        #print("left")
        print(Motor_Control.left)
    elif str(phrase) == "rechts":
        #print("right")
        print(Motor_Control.right)
    elif str(phrase) == "halt":
        #print("halt")
        print(Motor_Control.stop)
