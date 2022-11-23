from Signdetection.yolov5.detect import loadModel, detect
import tkinter as tk
from tkinter import messagebox
from Lanedetection.main import process_image, process_video, process_webcam
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfile
import os


# sorce = 'D:/ds-project/DS3-TarzonTheWonderCar/combining/test/00005.png'
# # source = "D:/ds-project/DS3-TarzonTheWonderCar/vid1.mp4"
# # source = 'D:/ds-project/DS3-TarzonTheWonderCar/Lanedetection/videos/v1.mp4'
# # source = 'D:/ds-project/DS3-TarzonTheWonderCar/2.png'
# # img = custom_run(weights, source, datafile)
# # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# # img = detect_lane(img)
# # plt.imshow(img)
# # plt.show()
# # process_video(source,'testOutput.mp4')


class Platform():

    def __init__(self) -> None:
        self.weights = 'Signdetection/last.pt'
        self.datafile = 'Signdetection/custom_dataset.yaml'
        self.hel20 = "Helvetica 15 bold"
        self.hel14 = "Helvetica 10"
        self.aril8 = "Arial 8"
        self.hel5 = "Helvetica 5"
        self.file_dir = None

        self.taskbar = None
        self.mode = None
        self.source = None
        self.start = None

        self.root = tk.Tk()
        self.root.title("road helper model")

        self.radio_var = tk.IntVar()
        self.taskbar_text = tk.StringVar()

        self.modeType = 0
        self.modeLoaded = False

        self.save_dir = 'Output'
        if not (os.path.exists(self.save_dir)):
            os.mkdir(self.save_dir)
    # frames

    def create_button_frame1(self, ):
        buttons_frame = tk.Frame(self.root, border=2, relief=tk.GROOVE)

        # button frame
        tk.Label(buttons_frame, text='Load options', font=self.hel14, anchor='w').pack(anchor='w', padx=30, pady=2,
                                                                                       side='top')
        tk.Button(buttons_frame, text='Load file', font=self.hel20, width=20, command=self.open_file).pack(anchor='w',
                                                                                                           padx=30,
                                                                                                           pady=2)
        tk.Button(buttons_frame, text='webcam ', font=self.hel20, width=20, command=self.webcam).pack(anchor='w',
                                                                                                      padx=30, pady=2)
        tk.Label(buttons_frame, text='*webcam cannot process both lane and sign detection together', font=self.hel5,
                 anchor='w', foreground='red').pack(anchor='nw', padx=30, pady=2, side='top')

        buttons_frame.pack(padx=10, pady=10, fill='x')
        return buttons_frame

    def create_save_frame(self, ):
        buttons_frame = tk.Frame(self.root, border=2, relief=tk.GROOVE)

        # button farme
        tk.Button(buttons_frame, text='save file', font=self.hel20, width=20).pack(anchor='w', padx=30, pady=2)
        buttons_frame.pack(padx=10, pady=10, fill='x')
        return buttons_frame

    def create_radio_frame(self, mode=1):
        radio_frame = tk.Frame(self.root, border=2, relief=tk.GROOVE)
        # radio button frame
        self.radio_var.set(1)
        tk.Label(radio_frame, text='Select Mode', font=self.hel14, anchor='w').pack(anchor='nw', side='top')
        if mode == 1:

            tk.Radiobutton(radio_frame, text="Sign detection", variable=self.radio_var, value=1).pack(anchor='w',
                                                                                                      padx=30, pady=2)
            tk.Radiobutton(radio_frame, text="lane detection", variable=self.radio_var, value=2).pack(anchor='w',
                                                                                                      padx=30, pady=2)
            tk.Radiobutton(radio_frame, text="both", variable=self.radio_var, value=3).pack(anchor='w', padx=30, pady=2)
        else:
            tk.Radiobutton(radio_frame, text="Sign detection", variable=self.radio_var, value=1).pack(anchor='w',
                                                                                                      padx=30, pady=2)
            tk.Radiobutton(radio_frame, text="lane detection", variable=self.radio_var, value=2).pack(anchor='w',
                                                                                                      padx=30, pady=2)

        radio_frame.pack(padx=10, pady=10, fill='x')
        return radio_frame

    def create_start_frame(self, ):
        start_frame = tk.Frame(self.root, border=2, relief=tk.GROOVE)

        # start frame
        tk.Button(start_frame, text='Start', font=self.hel20, width=20, command=self.proceed).pack(anchor='w', padx=30,
                                                                                                   pady=2)

        start_frame.pack(padx=10, pady=10, fill='x')
        return start_frame

    def create_taskbar_frame(self, ):
        taskbar_frame = tk.Frame(self.root, border=2, relief='groove', bg='white')

        # task bar frame1111
        lambel = tk.Label(taskbar_frame, textvariable=self.taskbar_text, font=self.aril8, bg='white')
        lambel.pack(fill='x', anchor='w', side='left')

        taskbar_frame.pack(padx=10, pady=10, fill='x')
        return taskbar_frame

    # button funcs
    def open_file(self):
        self.modeType = 1
        file = askopenfile(mode='r', filetypes=[('Video', ['*.mov', '*.avi', '*.mkv', '*.mp4', ]), ('Image', ['*.png', '*.jpg', '*.jpeg'])])
        self.file_dir = str(file.name)
        if self.file_dir is not None:
            self.taskbar_text.set(f'file loaded : {self.file_dir.split(sep="/")[-1]}')
            self.makeGUI(1)

    def webcam(self):
        self.modeType = 0
        self.taskbar_text.set(f'Webcam selected')
        self.makeGUI(2)

    def destroyall(self):
        if self.taskbar is not None:
            self.taskbar.destroy()
            self.taskbar = None
        if self.mode is not None:
            self.mode.destroy()
            self.mode = None
        if self.source is not None:
            self.source.destroy()
            self.source = None
        if self.start is not None:
            self.start.destroy()
            self.start = None

    def makeGUI(self, i):
        self.destroyall()
        if i == 0:
            self.source = self.create_button_frame1()
            self.taskbar = self.create_taskbar_frame()
        elif 1 == i:
            self.source = self.create_button_frame1()
            self.mode = self.create_radio_frame(1)
            self.start = self.create_start_frame()
            self.taskbar = self.create_taskbar_frame()
        elif i == 2:
            self.source = self.create_button_frame1()
            self.mode = self.create_radio_frame(0)
            self.start = self.create_start_frame()
            self.taskbar = self.create_taskbar_frame()

    def proceed(self):
        if ((self.radio_var.get() == 1 or self.radio_var.get() == 3 )):
            if(self.modeLoaded == False):
                self.taskbar_text.set('Please wait Loading Model...')
                self.taskbar.update()
                loadModel(self.weights, self.datafile)
                self.modeLoaded = True
                self.taskbar_text.set('Model Loaded')
                self.taskbar.update()
        if(self.modeType == 0):
            if(self.radio_var.get() == 1):
                detect(0, project=self.save_dir)
            else:
                process_webcam()

        if(self.modeType == 1):
            is_video = True in [(i in self.file_dir) for i in ['.mov', '.avi', '.mkv', '.mp4', ]]
            savdir=self.save_dir + '/exp' +( (str(len(os.listdir(self.save_dir)))+'/') if len(os.listdir(self.save_dir)) >0 else '/')
            self.taskbar_text.set("Processing File! please Wait...")
            self.taskbar.update()
            if(self.radio_var.get() == 1):
                detect(self.file_dir, project=self.save_dir)
            elif(self.radio_var.get() == 2):  
                os.mkdir(savdir)
                if(is_video):
                    process_video(self.file_dir, savdir + self.file_dir.split('/')[-1] )
                else:
                    process_image(self.file_dir, savdir + self.file_dir.split('/')[-1])
            else:
                
                detect(self.file_dir, project=self.save_dir)
                os.rename(savdir+self.file_dir.split('/')[-1], savdir+ 'tmp' +self.file_dir.split('/')[-1])
                if(is_video):
                    process_video(savdir+'tmp'+self.file_dir.split('/')[-1], savdir +self.file_dir.split('/')[-1])
                else:
                     process_image(savdir+'tmp'+self.file_dir.split('/')[-1], savdir +self.file_dir.split('/')[-1])
                os.remove(savdir+ 'tmp' +self.file_dir.split('/')[-1])

            self.taskbar_text.set("file processed and saved")
            self.taskbar.update()
            messagebox.showinfo("Process Completed", f'given file is processed and saved at {savdir} ')


        

    def mainloop(self):
        self.taskbar_text.set(f'welcome')
        self.makeGUI(0)
        self.root.mainloop()

    # label.grid(row=0, column=0, padx = 2, pady=2)
    # load_img_button.grid(row=0+1, column=0, padx = 2, pady=2)
    # save_img_button.grid(row=1+1, column=0, padx = 2, pady=2)
    # webcam_button.grid(row=2+1, column=0, padx = 2, pady=2)


platform = Platform()
platform.mainloop()
