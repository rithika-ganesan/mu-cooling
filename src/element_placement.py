### Simple loop to understand placement of solenoids and detectors in the solenoid design

period = 2000

for i in range(10):
    bmaxd = period * i + period*0/4

    bminf = period * i + period*1/4 #minimum virtual detectors at same location as the fofo
    fofof = period * i + period*1/4

    bmaxf = period * i + period*1/2 #max detectors in the middle

    bmind = period * i + period*3/4
    fofod = period * i + period*3/4

    print(bmaxd, bminf, fofof, bmaxf, fofod, bmind)

