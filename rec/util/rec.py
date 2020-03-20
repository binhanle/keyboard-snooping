import sys
import queue
import numpy as np
import soundfile as sf
import sounddevice as sd


class myrecording(object):

    def __init__(self, filename, samplerate=44100, blocksize=0, channels=2):
        self.filename = filename
        self.rate = samplerate
        self.block = blocksize
        self.channels = channels

        self.outdata = queue.Queue()
        self.outfile = sf.SoundFile(
            self.filename, mode="x", samplerate=self.rate, channels=self.channels
        )


        print("Current devices:\n")
        print(sd.query_devices())
        print("")

        self.i_device = int(input("Choose mic (index):  "))
        self.stream = sd.InputStream(
            samplerate=self.rate,
            blocksize=self.block,
            device=self.i_device,
            channels=self.channels,
            callback=self.callback,
        )

    def callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)

        self.outdata.put(indata.copy())
        self.outfile.write( self.outdata.get() )

    def start_record(self):

        self.stream.start()


    def stop_record(self):
        
        try:
            self.stream.stop()
            self.outfile.flush()
            self.outfile.close()
        except RuntimeError as e:
            print( e )





