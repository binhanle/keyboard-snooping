import argparse, sys, os, csv, wave, time, math, shutil
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.signal import hilbert, find_peaks

from scipy.integrate import cumtrapz
import all2earth

key2coord = {
    '0': [0,0],
    '1': [-1,1],
    '2': [0,1],
    '3': [1,1],
    '4': [-1,2],
    '5': [0,2],
    '6': [1,2],
    '7': [-1,3],
    '8': [0,3],
    '9': [1,3]
}

def keypair2class(keypair):
    fst = keypair[0:1]
    snd = keypair[1:2]
    fst_coord = key2coord[fst]
    snd_coord = key2coord[snd]
    coord = [snd_coord[0]-fst_coord[0],snd_coord[1]-fst_coord[1]]
    return coord

def clear(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)

def clearPath(path_name):
    if os.path.exists(path_name):
        shutil.rmtree(path_name)
        
def createDirectory(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

def parseWav(wav_file_name): 
    sampling_rate, data = wavfile.read(wav_file_name)
    df = pd.DataFrame(data)
    df['value'] = abs(df[list(df.columns)].sum(axis=1))
    return sampling_rate, df

def peakWav(file_prefix, peak_range, plot_sync):
    # file name
    audio_file_name = file_prefix+'.wav'
    audio_csv_file_name = file_prefix+'.wave.csv'
    # parsing and reading
    sampling_rate, wav_df = parseWav(audio_file_name)
    print("\nSampling Rate\t\t\t{0} Hz".format(sampling_rate))
    # head and peak
    head_wav_df = wav_df[:int(sampling_rate*peak_range)]
    peak_index = head_wav_df['value'].idxmax()
    peak_value = head_wav_df.at[peak_index, 'value']
    print("Peak Index:\t\t\t{0} ({1:.3f} seconds)".format(peak_index, peak_index/sampling_rate))
    print("Peak Value:\t\t\t{0}".format(peak_value))
    sync_wav_df = wav_df[peak_index:].reset_index(drop=True)
    sync_wav_df.to_csv(audio_csv_file_name,header=False,columns=[0])
    # plot synchronization
    if plot_sync:
        # visualize head 
        head_wav_df_plot = head_wav_df.plot(y=1,color='red')
        head_wav_df_fig = head_wav_df_plot.get_figure()
        head_wav_df_fig.savefig(file_prefix+'.wave.head.png')
        # visualize sync head 
        sync_wav_df_plot = sync_wav_df[:int(sampling_rate*peak_range)].reset_index().plot(y=1,color='red')
        sync_wav_df_fig = sync_wav_df_plot.get_figure()
        sync_wav_df_fig.savefig(file_prefix+'.wave.sync.png')
    return sampling_rate, sync_wav_df

def peakEarth(file_prefix, peak_range_earth, plot_sync):
    # file names
    # all_file_name = file_prefix+'.all.csv'
    earth_file_name = file_prefix+".earth.csv"
    # parsing and reading 
    # all2earth.convert(all_file_name, file_prefix)
    # all2earth.convert2(all_file_name, file_prefix)time,gFx,gFy,gFz,TgF
    earth_df = pd.read_csv(earth_file_name, dtype={'time': 'float64', 'gFx': 'float64', 'gFy': 'float64', 'gFz': 'float64'})
    earth_df = earth_df.rename(columns={"time": "ts", "gFx": "x", "gFy": "y", "gFz": "z"}, errors="raise")
    earth_df = earth_df.drop(columns=['TgF'])
    earth_df['ts'] = earth_df['ts']*1000
    earth_df['ts'] = earth_df['ts'].astype('int64')
    peak_range_end = int(earth_df['ts'][0])+int(peak_range_earth*1000)
    head_earth_df = earth_df[earth_df['ts']<peak_range_end].reset_index(drop=True)
    peak_index = head_earth_df['z'].abs().idxmax()
    starting_ts = earth_df['ts'][0]
    peak_ts = int(head_earth_df.at[peak_index, 'ts'])
    peak_value = head_earth_df.at[peak_index, 'z']
    print("\nStarting TimeStamp:\t\t{0} ms".format(starting_ts))
    print("Peak TimeStamp:\t\t\t{0} ms ({1:.3f} seconds)".format(peak_ts, (peak_ts-starting_ts)/1000))
    print("Peak Value:\t\t\t{0}".format(peak_value))
    sync_earth_df = earth_df[earth_df['ts']>=peak_ts].reset_index(drop=True)
    sync_earth_df['ts']=sync_earth_df['ts']-peak_ts
    # plot synchronization
    if plot_sync:
        # visualize head 
        head_earth_df_plot = head_earth_df.plot(x='ts',y='z',color='red')
        head_earth_df_fig = head_earth_df_plot.get_figure()
        head_earth_df_fig.savefig(file_prefix+'.earth.head.png')
        # visualize sync head 
        sync_earth_df_plot = sync_earth_df[:head_earth_df.shape[0]].plot(x='ts',y='z',color='red')
        sync_earth_df_fig = sync_earth_df_plot.get_figure()
        sync_earth_df_fig.savefig(file_prefix+'.earth.sync.png')
    return sync_earth_df

def createFolders(file_prefix):
    keylog_file_name = file_prefix+".csv"
    keylog_df =  pd.read_csv(keylog_file_name, names=['start', 'end', 'content'])
    keylog_data = []
    #get keylog data
    with open(keylog_file_name, mode='r') as keylog_file:
        keylog_file_reader = csv.reader(keylog_file)
        keylog_data = list(keylog_file_reader)
    num = 0
    print(" ")
    pbar = tqdm(total=len(keylog_data), desc='CREATING', unit='folders')
    for i, keylog in enumerate(keylog_data):
        index = f'{i:04d}'              
        content = keylog[2]
        clearPath(file_prefix+"."+index+"/")
        createDirectory(file_prefix+"."+index+"/")
        # earth_output_name = file_prefix+"."+index+"/"+content+".earth.csv"
        # rota_output_name = file_prefix+"."+index+"/"+content+".rota.txt"
        # wave_output_name = file_prefix+"."+index+"/"+content+".wave.csv"
        # clear(earth_output_name)
        # clear(rota_output_name)
        # clear(wave_output_name)
        num += 1
        pbar.update(1)
    pbar.close()
    print("Created Folders:\t\tFROM {0}.0000/ TO {1}.{2:04d}/".format(file_prefix, file_prefix, num-1))
    print("Number of Folders:\t\t{0}".format(num))
    return keylog_df, keylog_data

def cutWave(file_prefix, sampling_rate, sync_wav_df, keylog_data, stereo):
    # print(sync_wav_df)
    # print(hilbert(sync_wav_df[100000:200000]['value']))
    # return
    print(" ")
    # envelope = np.abs(hilbert(sync_wav_df[0]))
    failures = []
    peak_dict = {}
    pbar = tqdm(total=len(keylog_data), desc='CUTTING ', unit='samples')
    for i, keylog in enumerate(keylog_data):
        index = f'{i:04d}'
        content = keylog[2]
        starting_ts = int(keylog[0])
        ending_ts = int(keylog[1])
        starting_index = int((starting_ts*sampling_rate)/1000000000)
        ending_index = int((ending_ts*sampling_rate)/1000000000)
        wave_output_name = file_prefix+"."+index+"/"+content+".wave.csv"
        # finding 6 peak
        # peak_thresh = 10000
        peak_thresh = 31000
        peak_sep_sec = 0.15

        part_wav_df = sync_wav_df[starting_index:ending_index]
        # print(part_wav_df[0])
        # envelope = np.abs(hilbert(part_wav_df[0]))
        distance = peak_sep_sec * sampling_rate
        peaks, _ = find_peaks(part_wav_df['value'], height=peak_thresh, distance=distance)
        if len(peaks) == 6: 
            peaks = peaks+starting_index
            peak_dict[i] = peaks  
            if stereo:
                part_wav_df.to_csv(wave_output_name,header=False,columns=[0,1])
            else:
                part_wav_df.to_csv(wave_output_name,header=False,columns=[0])
        else:
            failures.append(index)
        pbar.update(1)
    pbar.close()
    if len(failures)>0:
        for failure in failures:
            path = file_prefix+"."+failure+"/"
            clearPath(path)
        print("Could not find 6 peaks:\t\t{0}, removed these folders".format(failures))
    return peak_dict

def cutEarth(file_prefix, sync_earth_df, keylog_data, peak_dict, sampling_rate):
    print(" ")
    pbar = tqdm(total=len(keylog_data), desc='CUTTING', unit='samples')
    for i, keylog in enumerate(keylog_data):
        index = f'{i:04d}'
        content = keylog[2]
        # earth_output_name = file_prefix+"."+index+"/"+content+".lnac.csv"
        earth_output_name = file_prefix+"."+index+"/"+content+".acce.csv"
        # if peak_dict.get(i) != None:
        if i in peak_dict.keys():
            peak = peak_dict.get(i)
            peak_ts = peak*(1000/sampling_rate)
            from_ts = peak_ts[0]
            to_ts = peak_ts[5]
            # finding shift
            corrected_from_ts_idx = sync_earth_df[ (sync_earth_df['ts']>=(from_ts-100)) & (sync_earth_df['ts']<(from_ts+100))]['z'].idxmax()
            corrected_from_ts = sync_earth_df['ts'][corrected_from_ts_idx]
            corrected_to_ts_idx = sync_earth_df[ (sync_earth_df['ts']>=(to_ts-100)) & (sync_earth_df['ts']<(to_ts+100))]['z'].idxmax()
            corrected_to_ts = sync_earth_df['ts'][corrected_to_ts_idx]
            shift = corrected_from_ts - from_ts
            part_earth_df = sync_earth_df[ (sync_earth_df['ts']>=corrected_from_ts) & (sync_earth_df['ts']<corrected_to_ts)]
            part_earth_df.to_csv(earth_output_name,header=False,columns=['ts','x','y','z'],index=False)

            # part_earth_df = sync_earth_df[ (sync_earth_df['ts']>=from_ts) & (sync_earth_df['ts']<to_ts)]
            # part_earth_df.to_csv(earth_output_name,header=False,columns=['ts','x','y','z'],index=False)
     
            angle5 = []
            for j in range(5):
                keypair = content[j:j+2]
                coord = keypair2class(keypair)
                starting_ts = peak_ts[j]
                ending_ts = peak_ts[j+1]
                corrected_starting_ts_idx = sync_earth_df[ (sync_earth_df['ts']>=(starting_ts-100)) & (sync_earth_df['ts']<(starting_ts+100))]['z'].idxmax()
                corrected_starting_ts = sync_earth_df['ts'][corrected_starting_ts_idx]
                corrected_ending_ts_idx = sync_earth_df[ (sync_earth_df['ts']>=(ending_ts-100)) & (sync_earth_df['ts']<(ending_ts+100))]['z'].idxmax()
                corrected_ending_ts = sync_earth_df['ts'][corrected_ending_ts_idx]
                move_df = sync_earth_df[ (sync_earth_df['ts']>=corrected_starting_ts) & (sync_earth_df['ts']<corrected_ending_ts)].copy()
                move_df['ts'] = move_df['ts'].astype('int64')
                move_df['ts'] = move_df['ts'] - int(corrected_starting_ts)
                # move_output_name = file_prefix+"."+index+"/"+str(j)+"."+str(keypair)+"."+str(coord[0])+"."+str(coord[1])+".lnac.csv"
                move_output_name = file_prefix+"."+index+"/"+str(j)+"."+str(keypair)+"."+str(coord[0])+"."+str(coord[1])+".acce.csv"
                move_df.to_csv(move_output_name,header=False,columns=['ts','x','y','z'],index=False)
                

                # vx = cumtrapz(move_df['x'], x=move_df['ts'], initial=0)
                # vy = cumtrapz(move_df['y'], x=move_df['ts'], initial=0)
                # # x = cumtrapz(vx, x=move_df['ts'], initial=0)
                # # y = cumtrapz(vy, x=move_df['ts'], initial=0)
                # # dx = x[-1]-x[0]
                # # dy = y[-1]-y[0]

                # vx_mid = vx[int(vx.size/2)]
                # vy_mid = vy[int(vx.size/2)]

                # angle = math.atan2(vy_mid, vx_mid)
                # angle5.append(angle)
            # rotation4 = []
            # for k in range(4):
            #     angle1 = angle5[k]
            #     angle2 = angle5[k+1]
            #     rotation = angle2-angle1
            #     while rotation<(math.pi*(-1)):
            #         rotation += math.pi*2
            #     while rotation>(math.pi):
            #         rotation -= math.pi*2
            #     rotation4.append(rotation)
            #     with open(rota_output_name, 'w') as rota_output_file:
            #         for rotation in rotation4:
            #             rota_output_file.write("{0:.6f}\n".format(rotation))
        pbar.update(1)
    pbar.close()
        

if __name__ == '__main__':

    # plt styles
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams["figure.figsize"] = (80,40)

    #parsing arguments
    parser = argparse.ArgumentParser(description="python synclipper3.py")
    parser.add_argument("fileprefix", help="Prefix of Data Files")
    parser.add_argument("-s", "--stereo", help = "Two Different Channels?", required=False, action='store_true')
    parser.add_argument("-o", "--onlyaudio", help = "Only Audio? ", required=False, action='store_true')
    parser.add_argument("-p", "--plotsync", help = "Plot the Synchronization? ", required=False, action='store_true')
    parser.add_argument("-a", "--audiopeakrange", help = "[int] seconds for audio peak range, defaut:5", required=False, type=float, default=5.0)
    parser.add_argument("-e", "--earthpeakrange", help = "[int] seconds for earth peak range, defaut:5", required=False, type=float, default=5.0)

    args = parser.parse_args()
    
    #argument variables
    print("\n░░░░ Arguments")
    file_prefix = args.fileprefix
    stereo = args.stereo
    audio_only = args.onlyaudio
    plot_sync = args.plotsync
    peak_range_audio = args.audiopeakrange
    peak_range_earth = args.earthpeakrange
    print("\nPrefix of Data Files:\t\t{0}".format(file_prefix))
    print("Two Different Channels?\t\t{0}".format(stereo))
    print("Audio Only?\t\t\t{0}".format(audio_only))
    print("Peak Range of Audio: \t\t0:0 - 0:{0}".format(peak_range_audio))
    print("Peak Range of Sensors: \t\t0:0 - 0:{0}".format(peak_range_earth))

    sync_earth_df = None 
    # peak: earth 
    if audio_only == False:
        print("\n░░░░ Earth Peak")
        sync_earth_df = peakEarth(file_prefix, peak_range_earth, plot_sync)
    
    # peak: audio 
    print("\n░░░░ Audio Peak")
    sampling_rate, sync_wav_df = peakWav(file_prefix, peak_range_audio, plot_sync)

    # create folders
    print("\n░░░░ Creating Folders")
    keylog_df, keylog_data = createFolders(file_prefix)

    # cut: audio
    print("\n░░░░ Cutting Audio")
    peak_dict = cutWave(file_prefix, sampling_rate, sync_wav_df, keylog_data, stereo)

    # cut: earth
    if audio_only == False:
        print("\n░░░░ Cutting Earth")
        cutEarth(file_prefix, sync_earth_df, keylog_data, peak_dict, sampling_rate)



    
