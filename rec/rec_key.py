import os
import glob
import time
import keyboard
import datetime
import random
from util.rec import *

def writeKeyLog( ofile, lines, t_bias ):

    with open(ofile, "w") as f:
        for line in lines:
            end_time = (line[-1].time - t_bias) * 1e9
            start_time = (line[0].time - t_bias) * 1e9

            string = "".join([c.name for c in line[1:-1]])

            f.write("%d,%d,%s\n" % (start_time, end_time, string))



if __name__ == '__main__':

    line  = []
    lines = []

    t_bias  = 0
    out_dir = 'records'

    began = False

    filename = datetime.datetime.now().strftime('%m%d%H%M%S')

    wavFile = '%s/%s.wav' % (out_dir, filename )
    logFile = '%s/%s.csv' % (out_dir, filename )

    os.makedirs( out_dir, exist_ok=True )
    
    rec = myrecording(filename=wavFile) 

    print('Recording parameters set.')
    print('Started microphone . . .')

    rec.start_record()
    time.sleep(0.5)

    print('Please start actual recording by pressing [SPACE] . . .\n' )

    num = 0
    while True:
        key = keyboard.read_event()

        if key.event_type == 'down':

            if key.name == 'space':
                if not began:
                    t_bias = key.time
                    print('Start actual recording:\n' )
                    

                    line.append(key)
                    began = True
                else:
                    print('Stop recording.\n')
                    rec.stop_record()
                    break

            else:
                line.append(key)

                if key.name == 'enter':

                    randominput = ''.join(["{}".format(random.randint(0, 9)) for digits in range(0, 6)])

                    lines.append(line)
                    num += 1
                    print(" [LINE] "+str(num))
                    print(" [NEXT] "+randominput)
                    
                    # print(' '.join([k.name for k in line]))
                    line = [key]


    print('Writing key logs to %s . . . ' % (logFile) )
    writeKeyLog( logFile, lines, t_bias )

