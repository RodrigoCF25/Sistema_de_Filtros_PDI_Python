# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 18:02:50 2022

@author: rodri
"""

import time
import tkinter as tk
from tkinter import Button, ttk, OptionMenu, StringVar, filedialog as fd
import os
import cv2 as cv
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import shutil
import math

def prSetTxt(pTxt, pVal):
    pTxt.delete(0, len(pTxt.get()))
    pTxt.insert(0, pVal)



class WindowFilterSystem:
    def __init__(self):
        self.__route_to_save = "D:/Procesamiento de imagenes/Prueba.png"
        self.__window = tk.Tk()
        self.__window.title("Filter System")
        self.__window.geometry("2000x2000+0+0")
        self.__imageName = ""
        self.__height, self.__width = (0,0)

        self.__list_tk_images = [] #Lista de imagenes para Tk
        self.__list_cv_images = [] #Lista de imagenes para cv. Con ellas haremos las transformaciones


        self.__aCurr_final_image = 0 #Es un contador que nos posicionara en la imagen que debemos mostrar en la derecga

        self.__initial_image_tk = "" #Imagen de la izquierda en el Tk
        self.__final_image_tk = "" #Imagen de la derecha en el Tk

        self.__initial_image_cv = "" #Imagen de la izquierda en cv
        self.__final_image_cv = "" #Imagen de la derecha en cv
        self.__color_model = "" #Solo puede ser RGB o gray

        self.__initial_image_label = tk.Label(self.__window,text = "Initial",font = ("Arial",13),width = 5,height=1)
        self.__initial_image_label.place(x=0,y=0)

        self.__final_image_label = tk.Label(self.__window,text = "Final",font = ("Arial",13),width=5,height=1)
        self.__final_image_label.place(x=1450,y=0)

        self.__initial_image_portrait = ""
        self.__final_image_portrait = ""
        
        self.__label_effect_info = tk.Label(self.__window,text = "",font = ("Arial",9),width=40,height=1)
        self.__label_effect_info.place(x = 40,y = 700)
        
        self.__label_info = tk.Label(self.__window,text = "Effect's info: ",font = ("Arial",9),width=12,height=1)
        self.__label_info.place(x = 10,y = 700)
        
        
        
        self.__label_to_save = tk.Label(self.__window, text = "path =")
        self.__label_to_save.place(x = 575, y = 2)
        self.__entry_route = tk.Entry(self.__window, width = 32)
        prSetTxt(self.__entry_route,"D:/Quinto semestre/Procesamiento de imagenes")
        self.__entry_route.place(x = 625, y = 2)
        
                

        self.__parameter1_label = tk.Label(self.__window) #Para transformación exponencial (alfa), Binary (umbral), Gamma (gamma)
        self.__parameter1_label.place(x=0,y=10000)
        self.__parameter1_entry = tk.Entry(self.__window) #Para transformación exponencial (alfa), Binary (umbral), Gamma (gamma)
        self.__parameter1_entry.place(x=0,y=10000)

        self.__parameter2_label = tk.Label(self.__window) #Para sigma de Gauss
        self.__parameter2_label.place(x=0,y=10000)
        self.__parameter2_entry = tk.Entry(self.__window) #Para sigma de Gauss
        self.__parameter2_entry.place(x=0,y=10000)
        
        
        self.__combo = ttk.Combobox(self.__window,state="readonly", width = 5)
        self.__combo["values"] = ["1:2","1:3"]
        self.__combo.set("1:2")
        self.__combo.place(x=0,y=10000)
        

        
        self.__help_label = tk.Label(self.__window,text = "To start editing an image browse an image",font = ("Arial",10))
        self.__help_label.place(x= 10, y = 680)
        
        self.__help_label1_camera = tk.Label(self.__window, text = "A = Adaptive Binary Mean C, a = Adaptive Binary Inv Mean C, B = Binary, b = Binary Inv, C = CMY, c = Contour, d = Detail, E = Emboss, e = exponential dark, F = Find Edges, G = Gaussian Blur, g = GRAY, i = HSI, l = exponential light,  M = MinFilter, m = median Blur",font = ("Arial",9))
        self.__help_label1_camera.place(x = 10, y = 720)
                
        self.__help_label2_camera = tk.Label(self.__window, text = "n = gray negative, O = Binary OTSU, o = Binary OTSU Inv, q = QUIT, r = RGB, S = Sharpened Image, s = sharpened filter2D, v = HSV, y = YCrCb, z = BGR",font = ("Arial",9))
        self.__help_label2_camera.place(x = 10, y = 740)

        

        self.__kernel = [] #kernel 
        self.__label_kernel = ""
        self.__my_labels_for_kernel = [] #pensado para ser kernel de 3x3
        self.__my_entry = ""
        self.__my_entries_for_kernel = [] 
        self.__list_of_kernels_for_sharpened = ["1", "2", "3", "4", "5", "6" , "Free"] 



        self.__selected_option_for_sharpened = StringVar()
        self.__selected_option_for_sharpened.set(self.__list_of_kernels_for_sharpened[0])
        self.__selection_for_kernel_sharpened = OptionMenu(self.__window,self.__selected_option_for_sharpened,*self.__list_of_kernels_for_sharpened, command = self.Select_kernel_for_sharpened_button_click)
        self.__selection_for_kernel_sharpened.place(x=0,y=10000)




        #self.__se = []
        #self.__label_se = ""
        #self.__my_labels_for_se = []
        #self.__my_entry_se = ""
        #self.__my_entries_for_se = []
   
        self.__list_of_cv_se = ["RECT", "CROSS", "ELLIPSE"] 

        self.__selected_option_for_cv_se = StringVar()
        self.__selected_option_for_cv_se.set(self.__list_of_cv_se[0])
        self.__selection_for_cv_se = OptionMenu(self.__window,self.__selected_option_for_cv_se,*self.__list_of_cv_se, command = self.Select_cv_se_click)
        self.__selection_for_cv_se.place(x=0,y=10000)




        #Buttons
        
        self.__buttonCamera = Button(self.__window,text="Camera",command=self.Turn_on_Camera_click, cursor = "hand1")
        self.__buttonCamera.place(x = 710, y = 150)
        
        self.__buttonExplore = Button(self.__window,text = "Browse Image", command = self.BrowseImage_click, cursor = "hand1")
        self.__buttonExplore.place(x= 690, y = 35)
    

        self.__buttonReset = Button(self.__window,text = "Reset", width = 13, command = self.Reset_click,cursor = "hand1")
        self.__buttonReset.place(x= 690, y = 120)


        self.__buttonUndo = Button(self.__window,text = "Undo", width = 5,command = self.Undo_click,cursor = "hand1")
        self.__buttonUndo.place(x= 690, y =90)


        self.__buttonRedo = Button(self.__window,text = "Redo", width = 5,command = self.Redo_click,cursor = "hand1")
        self.__buttonRedo.place(x= 740, y = 90)

        self.__buttonSave = Button(self.__window,text = "Just Save", width = 6,command = self.Save_click,cursor = "hand1") #Guarda la imagen que se ve en final
        self.__buttonSave.place(x= 670, y = 180)
        
        
        self.__buttonSave_and_Change = Button(self.__window,text = "Save&Change", width = 10,command = self.Save_and_Change_click, cursor = "hand1") #Guarda la imagen que se ve en final
        self.__buttonSave_and_Change.place(x= 750, y = 180)



        self.__list_of_options = ["Negative","Logarithmic","Exponential LIGHT","Exponential DARK","Gamma","EqualizeHist HSV", "EqualizeHist YCrCb","EqualizeHist HLS", "EqualizeHist YUV", 
        "Blur", "Median Blur", "Gaussian Blur", "Smooth_Image", "Smooth_More_Image", "Sharpened" , "Laplacian", "Sharpened_Image", #Falta hacer sharpened
        "MinFilter","CONTOUR", "DETAIL", "EDGE_ENHANCE", "EDGE_ENHANCE_MORE", "EMBOSS", "FIND_EDGES", "Canny",
        "GRAY" ,"BGR", "CMY","HSV","HLS", "YCrCb","BINARY","BINARY OTSU", "BINARY MEAN C", "Erode", "Dilate", "Open", "Close", "Hit or Miss"] #Añadir Erosion, Dilatación, Apertura, Cierre, Hit or Miss 

       



        self.__selected_option = StringVar()
        self.__selected_option.set(self.__list_of_options[0])
        self.__selection_menu = OptionMenu(self.__window,self.__selected_option,*self.__list_of_options, command = self.Select_button_click)
        self.__selection_menu.place(x=690,y=60)


        self.__buttonApplyEffect = Button(self.__window,text = "Apply Effect", width = 13, command = self.ApplyEffect_click)
        self.__buttonApplyEffect.place(x=690,y=220)

        self.__matrix_size_confirm_button = Button(self.__window,text = "Send",width = 5, command = self.Matrix_size_confirm_size_click)
        self.__matrix_size_confirm_button.place(x = 0, y = 10000)


        self.__clean_kernel_button = Button(self.__window,text = "Clean", width = 5, command = self.clean_kernel_button_click)
        self.__clean_kernel_button.place(x = 0, y = 10000)

        self.__window.mainloop()




    def Know_Color_Model(self):
        try:
            if ((len(self.__final_image_cv.shape) == 2 and len(np.unique(self.__final_image_cv))>2) or (len(self.__final_image_cv.shape) == 3 and ((self.__final_image_cv[:,:,0].all()== self.__final_image_cv[:,:,1]).all() and ((self.__final_image_cv[:,:,0].all()==self.__final_image_cv[:,:,2]).all())))):
                self.__color_model = "GRAY"
            elif(len(self.__final_image_cv.shape) == 3):
                self.__color_model = "RGB"
            else:
                self.__color_model = "BIN"
        except TypeError:
            self.__color_model = "BIN"

        
        
    def Turn_on_Camera_click(self):
        font = cv.FONT_ITALIC
        color = (0,0,255)
        cap = cv.VideoCapture(0)
        chars = ["A","a","B","b","C","c","E","e","F","d","G","g","i","l","m","M","n","o","O","r","S","s","v","y","z"]
        chars = [ord(ch) for ch in chars]
        wanted_effect = ord("r")
        while(True):
            _,frame = cap.read() #frame es nuestra imagen
            key = cv.waitKey(1)
            if key != -1:
                wanted_effect = key
                color = (0,0,255)
                if(wanted_effect in [97,98]):
                    color = (255,255,255)
                elif(wanted_effect in [65,66]):
                    color = (0,0,0)

            if wanted_effect in chars:
                frame = self.__Apply_Effect_on_Camera(frame,wanted_effect)
            
            """ 
            num_frames = 12
            # Start time
            start = time.time()
             
            # Grab a few frames
            for i in range(0, num_frames) :
                cap.read()
                
             
            # End time
            end = time.time()
             
            # Time elapsed
            seconds = end - start
            #print ("Time taken : {0} seconds".format(seconds))
             
            # Calculate frames per second
            fps  = num_frames / seconds
            #print("Estimated frames per second : {0}".format(fps))
            
            
            cv.putText(frame,"{}FPS".format(int(fps)),(5,25),font,1,color,1,cv.LINE_AA)            

            """ 

            if key == ord("q"):
                break
            
            
            cv.imshow("Camera",frame)

            
        cap.release()
        cv.destroyAllWindows()



    def __Apply_Effect_on_Camera(self, frame,effect):
        if effect == ord("C"): #CMY
            return np.max(frame) - frame
        
        elif effect == ord("n"):
            frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
            return np.max(frame) - frame

        elif effect == ord("r"): #RGB
            return frame

        elif effect == ord("A"): #Adaptive Binary 
            frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
            return cv.adaptiveThreshold(frame,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,11,7)


        elif effect == ord("a"): #Adaptive Binary Inv
            frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
            return cv.adaptiveThreshold(frame,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY_INV,11,7)

        elif effect == ord("B"): #Binary 
            frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
            return cv.threshold(frame,np.mean(frame),255,cv.THRESH_BINARY)[1]

        elif effect == ord("b"): #Binary Inv
            frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
            return cv.threshold(frame,np.mean(frame),255,cv.THRESH_BINARY_INV)[1]
        
        elif effect == ord("O"): #Binary Otsu 
            frame =  cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
            return cv.threshold(frame,0,255,cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
        
        elif effect == ord("o"): #Binary Otsu INV
            frame =  cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
            return cv.threshold(frame,0,255,cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
        
        elif effect == ord("c"): #CONTOUR
            frame = Image.fromarray(frame,mode = "RGB")
            frame = frame.filter(ImageFilter.CONTOUR())
            return np.array(frame)

        elif effect == ord("d"): #detail
            frame = Image.fromarray(frame, mode = "RGB")
            frame = frame.filter(ImageFilter.DETAIL()) 
            return np.array(frame)

        elif effect == ord("z"): #BGR
            return cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        
        elif effect == ord("G"): #GaussianBlur
            return cv.GaussianBlur(frame,(11,11),5)
        
        elif effect == ord("g"): #gray
            return cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        
        elif effect == ord("v"): #hsv
            return cv.cvtColor(frame,cv.COLOR_BGR2HSV)
        
        elif effect == ord("i"): #hls or hsi
            return cv.cvtColor(frame,cv.COLOR_BGR2HLS)

        elif effect == ord("S"): #Sharpened_Image
            frame = Image.fromarray(frame, mode = "RGB")
            frame = frame.filter(ImageFilter.SHARPEN())
            return np.array(frame)
        
        elif effect == ord("s"): #Sharpened_filter2D
            return cv.filter2D(frame,-1,np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]]))
        
        elif effect == ord("m"): #medianBlur
            return cv.medianBlur(frame,11)
        

        elif effect == ord("M"): #MinFilter esta retrasado porque le toma tiempo la operacion
            frame = Image.fromarray(frame, mode = "RGB")
            image = frame.filter(ImageFilter.MinFilter(3)) 
            return np.array(image)

        elif effect == ord("E"): #EMBOSS
            frame = Image.fromarray(frame, mode = "RGB")
            image = frame.filter(ImageFilter.EMBOSS()) 
            return np.array(image)
        
        elif effect == ord("F"): #FIND_EDGES
            frame = Image.fromarray(frame, mode = "RGB")
            image = frame.filter(ImageFilter.FIND_EDGES()) 
            return np.array(image)

        elif effect == ord("y"): #YCrCb
            return cv.cvtColor(frame,cv.COLOR_BGR2YCrCb)
        
        elif effect == ord("e"): #Exponential DARK
            maximum = np.max(frame)
            alfa = 2
            A = maximum/(np.exp(alfa)-1)
            frame =  A * (np.exp((alfa*frame.astype("float64"))/maximum)-1)
            return frame.astype("uint8")

        elif effect == ord("l"): #Logarithm pero que va a ser expresado por Exponential Light por rapidez
            maximum = np.max(frame)
            alfa = 2
            A = maximum/(1-np.exp(-alfa))
            image_exponential_light = A * (1-np.exp((-alfa*frame)/maximum))
            return image_exponential_light.astype("uint8")
        


        
        


    def BrowseImage_click(self):
        self.__imageName = ""
        try:
            self.__imageName = tk.filedialog.askopenfilename(initialdir = "/", 
                                            title = "Select a File",
                                        filetypes=[("image", ".jpeg"),("image", ".png"), ("image", ".jpg")]) #El usuario puede escoger su imagen
            if(self.__imageName != ""):
                
                self.__list_tk_images = []
                self.__list_cv_images = []
                self.__list_name_effects = []
                image = cv.imread(self.__imageName)
                try:
                    if ((len(image.shape) == 2 and len(np.unique(image))>2) or (len(image) == 3 and ((image[:,:,0].all()== image[:,:,1]).all() and ((image[:,:,0].all()== image[:,:,2]).all())))):
                        self.__color_model = "GRAY"
                    elif(len(image.shape) == 3):
                        self.__color_model = "RGB"
                    else:
                        self.__color_model = "BIN"
                except TypeError:
                    self.__color_model = "BIN"
                            
                

                old_height,old_width = image.shape[0], image.shape[1]
                self.__height, self.__width = old_height, old_width
                if(old_width > old_height):
                    hypotenuse = 650
                else:
                    hypotenuse = 750
                theta = math.atan2(old_height,old_width)
                new_height = int(hypotenuse*math.sin(theta))
                new_width = int(hypotenuse*math.cos(theta))
                image = cv.resize(image,(new_width,new_height))
                cv.imwrite(self.__route_to_save,image)
                
    
                image_tk_photoimage = tk.PhotoImage(file = self.__route_to_save)
                self.__list_tk_images.append(image_tk_photoimage)
                self.__list_tk_images.append(image_tk_photoimage)
                
                image = cv.imread(self.__route_to_save)
    
                if (len(image.shape)==3):
                    self.__list_cv_images.append(image[:,:,::-1])
                    self.__list_cv_images.append(image[:,:,::-1])
                else:
                    self.__list_cv_images.append(image)
                    self.__list_cv_images.append(image)
    

                self.__aCurr_final_image = 1
                
                self.__initial_image_tk = self.__list_tk_images[0]
                self.__initial_image_cv = self.__list_cv_images[0]
    
                self.__final_image_tk = self.__list_tk_images[self.__aCurr_final_image]
                self.__final_image_cv = self.__list_cv_images[self.__aCurr_final_image]
    
                self.__initial_image_portrait = tk.Label(self.__window,image = self.__initial_image_tk)
                self.__initial_image_portrait.place(x = 0,y = 20)
    
                self.__final_image_portrait = tk.Label(self.__window,image = self.__final_image_tk)
                self.__final_image_portrait.place(x = 1500 - new_width, y=20)
    
                
        
        except AttributeError:
            pass

    
    def Reset_click(self):
        while(len(self.__list_tk_images)>2):
            self.__list_tk_images.pop(-1)
            self.__list_cv_images.pop(-1)

        self.__aCurr_final_image = 1
        

        self.__final_image_tk = self.__list_tk_images[self.__aCurr_final_image]
        self.__final_image_cv = self.__list_cv_images[self.__aCurr_final_image]

        self.__final_image_portrait.configure(image  = self.__final_image_tk)


        self.Know_Color_Model()

    def Undo_click(self):
        if(self.__aCurr_final_image>1):
            self.__aCurr_final_image -= 1
        

        self.__final_image_tk = self.__list_tk_images[self.__aCurr_final_image]
        self.__final_image_cv = self.__list_cv_images[self.__aCurr_final_image]

 
        self.__final_image_portrait.configure(image = self.__final_image_tk)

              

        self.Know_Color_Model()


    def Redo_click(self):
            
        if(self.__aCurr_final_image < len(self.__list_tk_images)-1):
            self.__aCurr_final_image += 1
        

        self.__final_image_tk = self.__list_tk_images[self.__aCurr_final_image]
        self.__final_image_cv = self.__list_cv_images[self.__aCurr_final_image]

        self.__initial_image_portrait.configure(image = self.__initial_image_tk)
        self.__final_image_portrait.configure(image = self.__final_image_tk)

        
        self.Know_Color_Model()

    def Save_click(self):
        route = self.__entry_route.get()
        if route not in ["", " "]:
            image = cv.resize(self.__final_image_cv,(self.__width,self.__height))
            if(self.__color_model == "RGB"):
                image = image[:,:,::-1]
            cv.imwrite(r"{}".format(route),image)
        
    
    def Save_and_Change_click(self):
        route = self.__entry_route.get()
        if route not in ["", " "]:
            image = cv.resize(self.__final_image_cv,(self.__width,self.__height))
            if(self.__color_model == "RGB"):
                image = image[:,:,::-1]
            cv.imwrite(r"{}".format(route),image)

            while(len(self.__list_tk_images)>0):
                self.__list_tk_images.pop(0)
                self.__list_cv_images.pop(0)

            self.__list_cv_images.append(self.__final_image_cv)
            self.__list_cv_images.append(self.__final_image_cv)
            
            self.__list_tk_images.append(self.__final_image_tk)
            self.__list_tk_images.append(self.__final_image_tk)

            self.__aCurr_final_image = 1
            
            self.__initial_image_cv = self.__list_tk_images[0]

            self.__initial_image_tk = self.__list_tk_images[0]
            self.__final_image_tk = self.__list_tk_images[self.__aCurr_final_image]
            self.__final_image_cv = self.__list_cv_images[self.__aCurr_final_image]

            self.__initial_image_portrait.configure(image = self.__initial_image_tk)
            self.__final_image_portrait.configure(image = self.__final_image_tk)


            self.Know_Color_Model()

    def Select_button_click(self,trash_parameter = 0):
        if(self.__color_model != "RGB" and self.__color_model != "GRAY" and self.__color_model != "BIN"): #Las imagenes a las que si podemos hacer transformaciones son RGB, GRAY y BINARIA
            self.__list_cv_images.pop(-1)
            self.__list_tk_images.pop(-1)    
            self.Undo_click()
 
        self.__parameter1_label.place(x=0,y=10000)
        self.__parameter1_entry.place(x=0,y=10000)

        self.__parameter2_label.place(x=0,y=10000)
        self.__parameter2_entry.place(x=0,y=10000)
        
        self.__combo.place(x= 0, y = 10000)


        self.__selection_for_kernel_sharpened.place(x = 0, y =10000)
        self.__matrix_size_confirm_button.place(x=0,y=10000)
        self.__clean_kernel_button.place(x=0,y=10000)

        self.__selection_for_cv_se.place(x = 0, y = 10000)

        for i in self.__my_labels_for_kernel:
            i.after(0,i.destroy())

        self.__my_labels_for_kernel = []
        
        for i in range(0, len(self.__my_entries_for_kernel)):
            for j in range(0,len(self.__my_entries_for_kernel[0])):
                self.__my_entries_for_kernel[i][j].after(0,self.__my_entries_for_kernel[i][j].destroy())

        self.__my_entries_for_kernel = []


        
        wanted_effect = self.__selected_option.get()
        if (wanted_effect == "Negative"):
            self.__help_label.configure(text = "Your image can be in RGB, GRAY or BINARY")
            self.__label_effect_info.place(x = 40,y = 700)
            self.__label_effect_info.configure(text = "Inverts the intensisty of pixels")
        elif (wanted_effect == "Logarithmic"):
            self.__help_label.configure(text = "Your image can be in RGB or GRAY")
            self.__label_effect_info.place(x=5,y=700)
            self.__label_effect_info.configure(text = "light your image")
        
        elif (wanted_effect in ["BINARY OTSU", "BINARY MEAN C"]):
            self.__help_label.configure(text = "Your image can be in RGB or GRAY")
            if wanted_effect == "BINARY OTSU":
                self.__label_effect_info.place(x = 30,y = 700)
                self.__label_effect_info.configure(text = "Best general binarization")
            else:
                self.__label_effect_info.place(x = 55,y = 700)
                self.__label_effect_info.configure(text = "Particular binarization for each pixel")
        
        elif(wanted_effect == "Exponential LIGHT" or wanted_effect == "Exponential DARK"):
            self.__help_label.configure(text = "Your image can be in RGB or GRAY")
            self.__parameter1_label.configure(text = "Alfa = ")
            self.__parameter1_label.place(x=690,y=250)
            self.__parameter1_entry.place(x=740,y=250)
            self.__parameter1_entry.configure(width = 8)
            prSetTxt(self.__parameter1_entry, "1")
            if(wanted_effect == "Exponential LIGHT"):
                self.__label_effect_info.place(x = 45,y = 700)
                self.__label_effect_info.configure(text = "light your image by a variable")
            else:
                self.__label_effect_info.place(x = 45,y = 700)
                self.__label_effect_info.configure(text = "dark your image by a variable")
                
        elif(wanted_effect  == "BINARY"):
            self.__help_label.configure(text = "Your image can be in RGB or GRAY")
            self.__parameter1_label.configure(text = "Umbral = ")
            self.__parameter1_label.place(x=690,y=250)
            self.__parameter1_entry.place(x=740,y=250)
            self.__parameter1_entry.configure(width = 8)
            prSetTxt(self.__parameter1_entry, str((np.mean(self.__final_image_cv))))
            self.__label_effect_info.place(x = 60,y = 700)
            self.__label_effect_info.configure(text = "General binarization proposed by you")
        
        elif (wanted_effect == "Gamma"):
            self.__help_label.configure(text = "Your image can be in RGB or GRAY")
            self.__parameter1_label.configure(text = "Gamma = ")
            self.__parameter1_label.place(x=690,y=250)
            self.__parameter1_entry.place(x=740,y=250)
            self.__parameter1_entry.configure(width = 8)
            prSetTxt(self.__parameter1_entry, "1")
            self.__label_effect_info.place(x=60,y=700)
            self.__label_effect_info.configure(text = "light when gamma < 1; dark gamma > 1")        
            
        
        elif (wanted_effect in ["EqualizeHist HSV", "EqualizeHist YCrCb","EqualizeHist HLS", "EqualizeHist YUV"]):
            self.__label_effect_info.place(x=60,y=700)
            self.__label_effect_info.configure(text = "Best distribution of intensity in pixels")        
            self.__help_label.configure(text = "Your image can be in RGB or GRAY")
        
        
        elif (wanted_effect in ["CMY","BGR","HSV","HLS","YCrCb"]):
            if(wanted_effect == "CMY"):
                self.__label_effect_info.place(x=60,y=700)
                self.__label_effect_info.configure(text = "Inverts the intensity of pixels")  
            elif wanted_effect == "BGR":
                self.__label_effect_info.place(x=70,y=700)
                self.__label_effect_info.configure(text = "Red channel in usual blue channel position")
            
            elif(wanted_effect == "HSV"):
                self.__label_effect_info.place(x=30,y=700)
                self.__label_effect_info.configure(text = "No linear color model")        
                
            elif(wanted_effect == "HLS"):
                self.__label_effect_info.place(x=30,y=700)
                self.__label_effect_info.configure(text = "No linear color model")  
            
            elif(wanted_effect == "YCrCb"):
                self.__label_effect_info.place(x=70,y=700)
                self.__label_effect_info.configure(text = "Linear color model that uses chrominance")  
                
            self.__help_label.configure(text = "Your image must be in RGB")
        
        elif (wanted_effect in  ["Blur","Median Blur", "Gaussian Blur"]):
            self.__help_label.configure(text = "Your image can be in RGB or GRAY")
            self.__parameter1_label.configure(text = "Size = ")
            self.__parameter1_label.place(x=690,y=250)
            self.__parameter1_entry.place(x=740,y=250)
            self.__parameter1_entry.configure(width = 8)
            prSetTxt(self.__parameter1_entry, "3")
            if(wanted_effect == "Blur"):
                self.__label_effect_info.place(x=40,y=700)
                self.__label_effect_info.configure(text = "Makes your image blurred") 
            
            if(wanted_effect == "Median Blur"):
                self.__label_effect_info.place(x=60,y=700)
                self.__label_effect_info.configure(text = "Remove white and black noise")
            

            if(wanted_effect == "Gaussian Blur"):
                self.__parameter2_label.configure(text = "Sigma = ")
                self.__parameter2_label.place(x=690,y=280)
                self.__parameter2_entry.place(x=740,y=280)
                self.__parameter2_entry.configure(width = 8)
                prSetTxt(self.__parameter2_entry, "1")
                self.__label_effect_info.place(x=70,y=700)
                self.__label_effect_info.configure(text = "Makes your image blurred more natural")

        elif (wanted_effect == "Laplacian"):
            self.__help_label.configure(text = "Your image can be in RGB or GRAY")
            self.__parameter1_label.configure(text = "Size = ")
            self.__parameter1_label.place(x=690,y=250)
            self.__parameter1_entry.place(x=740,y=250)
            self.__parameter1_entry.configure(width = 8)
            prSetTxt(self.__parameter1_entry, "3")
            self.__label_effect_info.place(x=30,y=700)
            self.__label_effect_info.configure(text = "Detects edges")

        elif (wanted_effect == "MinFilter"):
            self.__help_label.configure(text = "Your image can be in RGB or GRAY")
            self.__parameter1_label.configure(text = "Size = ")
            self.__parameter1_label.place(x=690,y=250)
            self.__parameter1_entry.place(x=740,y=250)
            self.__parameter1_entry.configure(width = 8)
            prSetTxt(self.__parameter1_entry, "1")
            self.__label_effect_info.place(x=45,y=700)
            self.__label_effect_info.configure(text = "Contours increase in thickness")
        
        elif (wanted_effect == "Sharpened"):
            self.__help_label.configure(text = "Your image can be in RGB or GRAY")
            self.__selection_for_kernel_sharpened.place(x = 800, y = 80)
            self.__label_effect_info.place(x=30,y=700)
            self.__label_effect_info.configure(text = "Highlight color changes")
            self.Select_kernel_for_sharpened_button_click()
            
        elif (wanted_effect == "Canny"):
            self.__help_label.configure(text = "Your image can be in RGB or GRAY")
            self.__label_effect_info.place(x=30,y=700)
            self.__label_effect_info.configure(text = "Find contours")
            
            
            self.__parameter1_label.configure(text = "Size = ") #Tamaño de la matriz para el blur
            self.__parameter1_label.place(x=690,y=250)
            self.__parameter1_entry.place(x=740,y=250)
            self.__parameter1_entry.configure(width = 8)
            prSetTxt(self.__parameter1_entry,"3")
            
            self.__parameter2_label.configure(text = "Value = ") #Valor
            self.__parameter2_label.place(x=690,y=280)
            self.__parameter2_entry.place(x=740,y=280)
            self.__parameter2_entry.configure(width = 8)
            prSetTxt(self.__parameter2_entry,"50")
            
            self.__combo.place(x=740, y =310)
           
        
        elif (wanted_effect == "GRAY"):
            self.__label_effect_info.place(x=45,y=700)
            self.__label_effect_info.configure(text = "Your image in gray scale")
        
        elif (wanted_effect == "CONTOUR"):
            self.__label_effect_info.place(x=30,y=700)
            self.__label_effect_info.configure(text = "Find contours")
        
        elif (wanted_effect == "DETAIL"):
            self.__label_effect_info.place(x=50,y=700)
            self.__label_effect_info.configure(text = "Improve the details of an image")
            
        elif (wanted_effect == "Smooth_Image"):
            self.__label_effect_info.place(x=40,y=700)
            self.__label_effect_info.configure(text = "Blurs your image a little")
            
        elif (wanted_effect == "Smooth_Image_More"):
            self.__label_effect_info.place(x=40,y=700)
            self.__label_effect_info.configure(text = "Blurs your image a little more")
        
        elif (wanted_effect == "EDGE_ENHANCE"):
            self.__label_effect_info.place(x=40,y=700)
            self.__label_effect_info.configure(text = "Improve the edges in the image")
            
        elif (wanted_effect == "EDGE_ENHANCE_MORE"):
            self.__label_effect_info.place(x=73,y=700)
            self.__label_effect_info.configure(text = "Improve a little bit more the edges in the image")
        
        elif (wanted_effect == "FIND_EDGES"):
            self.__label_effect_info.place(x=40,y=700)
            self.__label_effect_info.configure(text = "Finds the edges of an image")
        
        elif (wanted_effect == "EMBOSS"):
            self.__label_effect_info.place(x=65,y=700)
            self.__label_effect_info.configure(text = "Give a visual effect of high relief")
        

        elif (wanted_effect in ["Erode", "Dilate", "Close", "Open"]):
            self.__help_label.configure(text = "Your image must be in BINARY")
            self.__selection_for_cv_se.place(x = 690, y = 250)

            self.__parameter1_label.configure(text = "Size: ")
            self.__parameter1_label.place(x=770, y = 250)
            self.__parameter1_entry.place(x = 805, y = 250)
            self.__parameter1_entry.configure(width = 3)
            prSetTxt(self.__parameter1_entry,"3")

            self.__parameter2_label.configure(text = "Iterations: ")
            self.__parameter2_label.place(x=690, y = 290)
            self.__parameter2_entry.configure(width = 3)
            self.__parameter2_entry.place(x = 760, y = 290)
            prSetTxt(self.__parameter2_entry,"1")
            
            if(wanted_effect == "Erode"):
                self.__label_effect_info.place(x=30,y=700)
                self.__label_effect_info.configure(text = "Background info increases")
            elif(wanted_effect == "Dilate"):
                self.__label_effect_info.place(x=30,y=700)
                self.__label_effect_info.configure(text = "Background info decreases")
            elif(wanted_effect == "Close"):
                self.__label_effect_info.place(x=30,y=700)
                self.__label_effect_info.configure(text = "Dilate + Erode")
            else:
                self.__label_effect_info.place(x=30,y=700)
                self.__label_effect_info.configure(text = "Erode + Dilate")
            
        elif (wanted_effect == "Hit or Miss"):
            self.__help_label.configure(text = "Your image must be in BINARY")
            self.__label_kernel = ""
            self.__parameter1_label.place(x = 690, y = 270)
            self.__parameter1_label.configure(text = "Size: ")
            self.__parameter1_entry.configure(width = 3)
            self.__parameter1_entry.place(x = 725, y = 270)
            self.__matrix_size_confirm_button.place(x = 0, y = 10000)
            prSetTxt(self.__parameter1_entry,"3")
            self.__matrix_size_confirm_button.place(x = 770, y = 270)
            self.__label_effect_info.place(x=40,y=700)
            self.__label_effect_info.configure(text = "Find patterns or shapes")
            
            self.__clean_kernel_button.place(x = 820, y = 270)



            y = 310
            for i in range(0,3):
                row = []
                x = 650
                for j in range(0,3):
                    x += 50
                    self.__my_entry = tk.Entry(self.__window,width = 2)
                    self.__my_entry.place(x = x, y = y)
                    row.append(self.__my_entry)
                self.__my_entries_for_kernel.append(row)
                y += 50
            
    



            
    def Matrix_size_confirm_size_click(self): #Este lo puede compartir sharpened con Hit or Miss
        old_size = len(self.__my_entries_for_kernel)
        new_size = int(self.__parameter1_entry.get())

        if (new_size > 9):
            new_size = 9
        elif (new_size  < 3):
            new_size = 3

        if(new_size % 2 == 0):
            new_size += 1

        prSetTxt(self.__parameter1_entry,str(new_size))
        values = []

        for i in range(0, old_size):
            row = []
            for j in range(0,old_size):
                row.append(self.__my_entries_for_kernel[i][j].get())
            values.append(row)

        for i in range(0, old_size):
            for j in range(0,old_size):
                self.__my_entries_for_kernel[0][0].after(0,self.__my_entries_for_kernel[0][0].destroy())
                self.__my_entries_for_kernel[0].pop(0)
            self.__my_entries_for_kernel.pop(0)
        
        self.__my_entries_for_kernel = []

        y = 310
        if(new_size == 3):
            x_temp = 650
        elif(new_size == 5):
            x_temp = 600
        elif(new_size == 7):
            x_temp = 540
        else:
            x_temp = 500
            y = 350


        
        for i in range(0, new_size):
            row = []
            x = x_temp
            for j in range(0, new_size):
                x += 50
                if((i < old_size) and (j < old_size)):
                    self.__my_entry = tk.Entry(self.__window,width = 2)
                    self.__my_entry.place(x = x, y = y)
                    prSetTxt(self.__my_entry,values[i][j])
                    row.append(self.__my_entry)
                else:
                    self.__my_entry = tk.Entry(self.__window,width = 2)
                    self.__my_entry.place(x = x, y = y)
                    row.append(self.__my_entry)
            self.__my_entries_for_kernel.append(row)
            y += 50




 
    def Select_kernel_for_sharpened_button_click(self, trash_parameter = ""):
        wanted_kernel = self.__selected_option_for_sharpened.get()
        self.__label_kernel = ""
        self.__parameter1_label.place(x = 0, y = 10000)
        self.__parameter1_entry.place(x = 0, y = 10000)
        self.__matrix_size_confirm_button.place(x = 0, y = 10000)
        self.__clean_kernel_button.place(x = 0, y = 10000)

        for i in self.__my_labels_for_kernel:
            i.after(0,i.destroy())

        self.__my_labels_for_kernel = []
        
        for i in range(0, len(self.__my_entries_for_kernel)):
            for j in range(0,len(self.__my_entries_for_kernel)):
                self.__my_entries_for_kernel[i][j].after(0,self.__my_entries_for_kernel[i][j].destroy())

        self.__my_entries_for_kernel = []

        if(wanted_kernel == "1"):

            kernel = [["0","1","0"],["1","-4","1"],["0","1","0"]]
            self.__kernel = np.array([[0,1,0],[1,-4,1],[0,1,0]])
            y = 270
            for i in range(0,3):
                x = 650    
                for j in range(0,3):
                    x += 50
                    self.__label_kernel = tk.Label(text = kernel[i][j])
                    self.__label_kernel.place(x = x,y = y)
                    self.__my_labels_for_kernel.append(self.__label_kernel)

                y += 50
        
        elif(wanted_kernel == "2"):
            kernel = [["0","-1","0"],["-1","4","-1"],["0","-1","0"]]
            self.__kernel = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]])
            y = 270
            for i in range(0,3):
                x = 650    
                for j in range(0,3):
                    x += 50
                    self.__label_kernel = tk.Label(text = kernel[i][j])
                    self.__label_kernel.place(x = x,y = y)
                    self.__my_labels_for_kernel.append(self.__label_kernel)

                y += 50

        elif(wanted_kernel == "3"):
            kernel = [["1","1","1"],["1","-8","1"],["1","1","1"]]
            self.__kernel = np.array([[1,1,1],[1,-8,1],[1,-1,1]])
            y = 270
            for i in range(0,3):
                x = 650    
                for j in range(0,3):
                    x += 50
                    self.__label_kernel = tk.Label(text = kernel[i][j])
                    self.__label_kernel.place(x = x,y = y)
                    self.__my_labels_for_kernel.append(self.__label_kernel)

                y += 50

        elif(wanted_kernel == "4"):
            kernel = [["-1","-1","-1"],["-1","8","-1"],["-1","-1","-1"]]
            self.__kernel = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
            y = 270
            for i in range(0,3):
                x = 650    
                for j in range(0,3):
                    x += 50
                    self.__label_kernel = tk.Label(text = kernel[i][j])
                    self.__label_kernel.place(x = x,y = y)
                    self.__my_labels_for_kernel.append(self.__label_kernel)

                y += 50
        elif(wanted_kernel == "5"):
            kernel = [["-1","-1","-1"],["-1","9","-1"],["-1","-1","-1"]]
            self.__kernel = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
            y = 270
            for i in range(0,3):
                x = 650    
                for j in range(0,3):
                    x += 50
                    self.__label_kernel = tk.Label(text = kernel[i][j])
                    self.__label_kernel.place(x = x,y = y)
                    self.__my_labels_for_kernel.append(self.__label_kernel)

                y += 50

        elif(wanted_kernel == "6"):
            kernel = [["1","1","1"],["1","-9","1"],["1","1","1"]]
            self.__kernel = np.array([[1,1,1],[1,9,1],[1,1,1]])
            y = 270
            for i in range(0,3):
                x = 650    
                for j in range(0,3):
                    x += 50
                    self.__label_kernel = tk.Label(text = kernel[i][j])
                    self.__label_kernel.place(x = x,y = y)
                    self.__my_labels_for_kernel.append(self.__label_kernel)

                y += 50
            
        elif(wanted_kernel == "Free"):
            self.__parameter1_label.configure(text = "Size =")
            self.__parameter1_label.place(x= 700, y = 270)
            self.__parameter1_entry.configure(width = 2)
            prSetTxt(self.__parameter1_entry,"3")
            self.__parameter1_entry.place(x = 740, y = 270)
            self.__matrix_size_confirm_button.place(x = 770, y = 270)
            self.__clean_kernel_button.place(x = 830, y = 270)
            y = 300
            for i in range(0,3):
                x = 650    
                row = []
                for j in range(0,3):
                    x += 50
                    self.__my_entry = tk.Entry(self.__window,width = 2)
                    self.__my_entry.place(x = x,y = y)
                    row.append(self.__my_entry)
                self.__my_entries_for_kernel.append(row)
                y += 50
            
    
    def Select_cv_se_click(self,trash_parameter = ""):
        pass

    def clean_kernel_button_click(self):
        for i in range(0,len(self.__my_entries_for_kernel)):
            for j in range(0, len(self.__my_entries_for_kernel[0])):
                prSetTxt(self.__my_entries_for_kernel[i][j],"")
        

    
    def ApplyEffect_click(self):
        while(self.__aCurr_final_image < len(self.__list_cv_images)-1):
            self.__list_cv_images.pop(-1)
            self.__list_tk_images.pop(-1) 
   

        wanted_effect = self.__selected_option.get()
        
        if(wanted_effect == "Negative"):
            image = np.max(self.__final_image_cv) - self.__final_image_cv
            self.__InnerSave(image)
 
        elif (wanted_effect == "Logarithmic"):
            if(self.__color_model == "RGB"):
                image_hsv = cv.cvtColor(self.__final_image_cv,cv.COLOR_RGB2HSV)
                brightness = image_hsv[:,:,2]
                c = 255/np.log(1+np.max(brightness))
                for row in range(image_hsv.shape[0]):
                    for column in range(image_hsv.shape[1]):
                        if(brightness[row][column]>0):
                            brightness[row][column] = c * np.log(brightness[row][column])
                        else:
                             brightness[row][column] = c * np.log(1 + brightness[row][column])

                img_log_hsv = cv.merge((image_hsv[:,:,0],image_hsv[:,:,1],brightness))
                img_log_rgb = cv.cvtColor(img_log_hsv,cv.COLOR_HSV2RGB)
                self.__InnerSave(img_log_rgb)
            elif (self.__color_model == "GRAY"):
                image_log = self.__final_image_cv
                c = 255/np.log(1+np.max(image_log))
                for row in range(image_log.shape[0]):
                    for column in range(image_log.shape[1]):
                        if(image_log[row][column]>0):
                            image_log[row][column] = c * np.log(image_log[row][column])
                        else:
                             image_log[row][column] = c * np.log(1 + image_log[row][column])

                self.__InnerSave(image_log)
            


        elif (wanted_effect == "Exponential LIGHT"):
            if(self.__color_model == "RGB" or self.__color_model == "GRAY"):
                try:
                    alfa = float(self.__parameter1_entry.get().strip())
                except :
                    alfa = 1
                
                maximum = np.max(self.__final_image_cv)

                if(alfa>np.max(self.__final_image_cv)):
                    alfa = maximum
                    prSetTxt(self.__parameter1_entry, "1")
                elif(alfa<=0):
                    alfa = 1
                    prSetTxt(self.__parameter1_entry, "1")
                
                A = maximum/(1-np.exp(-alfa))


                image_exponential_light = A * (1-np.exp((-alfa*self.__final_image_cv)/maximum))
                image_exponential_light = image_exponential_light.astype("uint8")

                self.__InnerSave(image_exponential_light)

        elif (wanted_effect == "Exponential DARK"):
            if(self.__color_model == "RGB" or self.__color_model == "GRAY"):
                
                try:
                    alfa = float(self.__parameter1_entry.get().strip())
                except ValueError:
                    alfa = 1
                
                maximum = np.max(self.__final_image_cv)

                if(alfa<=0):
                    alfa = 1
                    prSetTxt(self.__parameter1_entry, "1")
                
                A = maximum/(np.exp(alfa)-1)

                image_exponential_dark = A * (np.exp((alfa*self.__final_image_cv.astype("float64"))/maximum)-1)
                image_exponential_dark = image_exponential_dark.astype("uint8")

                self.__InnerSave(image_exponential_dark)
        
        elif (wanted_effect == "Gamma"):
            if(self.__color_model == "RGB" or self.__color_model == "GRAY"):
                try:
                    gamma = float(self.__parameter1_entry.get().strip())
                    if (gamma < 0.04):
                        gamma = 0.04
                        prSetTxt(self.__parameter1_entry, "0.04")
                    elif (gamma > 25):
                        gamma = 25
                        prSetTxt(self.__parameter1_entry, "25")
                except ValueError:
                    gamma = 1
                    prSetTxt(self.__parameter1_entry, "1")
                
                image_gamma =  (255/(np.max(self.__final_image_cv)**gamma)) * (self.__final_image_cv ** gamma)
                
                self.__InnerSave(image_gamma)
                
                
        elif(wanted_effect == "EqualizeHist HSV"):
            if(self.__color_model == "RGB"):
                hsv = cv.cvtColor(self.__final_image_cv,cv.COLOR_RGB2HSV)
                brightness = hsv[:,:,2]
                brightness_eq = cv.equalizeHist(brightness)
                hsv[:,:,2] = brightness_eq
                rgb_eq = cv.cvtColor(hsv,cv.COLOR_HSV2RGB)
                self.__InnerSave(rgb_eq)
                
                
            elif(self.__color_model == "GRAY"):
                image_equalized = cv.equalizeHist(self.__final_image_cv)
                self.__InnerSave(image_equalized)

                
        elif(wanted_effect == "EqualizeHist YCrCb"):
            if(self.__color_model == "RGB"):
                YCrCb = cv.cvtColor(self.__final_image_cv,cv.COLOR_RGB2YCrCb)
                Y = YCrCb[:,:,0]
                Y_eq = cv.equalizeHist(Y)
                YCrCb[:,:,0] = Y_eq
                rgb_eq = cv.cvtColor(YCrCb,cv.COLOR_YCrCb2RGB)
                self.__InnerSave(rgb_eq)
                
                
            elif(self.__color_model == "GRAY"):
                image_equalized = cv.equalizeHist(self.__final_image_cv)
                self.__InnerSave(image_equalized)
                
        elif(wanted_effect == "EqualizeHist HLS"):
            if(self.__color_model == "RGB"):
                hls = cv.cvtColor(self.__final_image_cv,cv.COLOR_RGB2HLS)
                lightness = hls[:,:,1]
                lightness_eq = cv.equalizeHist(lightness)
                hls[:,:,1] = lightness_eq
                rgb_eq = cv.cvtColor(hls,cv.COLOR_HLS2RGB)

                self.__InnerSave(rgb_eq)
                
                
            elif(self.__color_model == "GRAY"):
                image_equalized = cv.equalizeHist(self.__final_image_cv)
                self.__InnerSave(image_equalized)
        
        elif(wanted_effect == "EqualizeHist YUV"):
            if(self.__color_model == "RGB"):
                YUV = cv.cvtColor(self.__final_image_cv,cv.COLOR_RGB2YUV)
                Y = YUV[:,:,0]
                Y_eq = cv.equalizeHist(Y)
                YUV[:,:,0] = Y_eq
                rgb_eq = cv.cvtColor(YUV,cv.COLOR_YUV2RGB)
                self.__InnerSave(rgb_eq)

            elif(self.__color_model == "GRAY"):
                image_equalized = cv.equalizeHist(self.__final_image_cv)
                self.__InnerSave(image_equalized)

                
        elif (wanted_effect == "Blur"):
            if(self.__color_model != "BIN"):
                matriz_size = int(self.__parameter1_entry.get())
                if (matriz_size % 2 == 0):
                    matriz_size += 1
                    prSetTxt(self.__parameter1_entry,str(matriz_size))
                kernel = np.ones((matriz_size,matriz_size),dtype = "float64") / (matriz_size ** 2)
                image = cv.filter2D(self.__final_image_cv,-1,kernel)
                self.__InnerSave(image)

        elif (wanted_effect == "Median Blur"):
            if(self.__color_model != "BIN"):
                matriz_size = int(self.__parameter1_entry.get())
                if (matriz_size % 2 == 0):
                    matriz_size += 1
                    prSetTxt(self.__parameter1_entry,str(matriz_size))
                image = cv.medianBlur(self.__final_image_cv,matriz_size)
                self.__InnerSave(image)
        
        elif (wanted_effect == "Gaussian Blur"):
            if(self.__color_model != "BIN"):
                matriz_size = int(self.__parameter1_entry.get())
                if (matriz_size % 2 == 0):
                    matriz_size += 1
                    prSetTxt(self.__parameter1_entry,str(matriz_size))
                sigma = int(self.__parameter2_entry.get())
                image = cv.GaussianBlur(self.__final_image_cv,(matriz_size,matriz_size),sigma)
                self.__InnerSave(image)

        elif (wanted_effect == "Smooth_Image"):
            if(self.__color_model != "BIN"):

                if(self.__color_model == "RGB"):
                    image = Image.fromarray(self.__final_image_cv, mode = "RGB")  
                else:
                    image =  image = Image.fromarray(self.__final_image_cv, mode = "L")
                image = image.filter(ImageFilter.SMOOTH())
                image = np.array(image)
                self.__InnerSave(image)
        
        elif (wanted_effect == "Smooth_More_Image"):
            if(self.__color_model != "BIN"):
                if(self.__color_model == "RGB"):
                    image = Image.fromarray(self.__final_image_cv, mode = "RGB")  
                else:
                    image =  image = Image.fromarray(self.__final_image_cv, mode = "L")
                image = image.filter(ImageFilter.SMOOTH_MORE())
                image = np.array(image)
                self.__InnerSave(image)

        elif (wanted_effect == "Laplacian"):
            if(self.__color_model != "BIN"):
                matriz_size = int(self.__parameter1_entry.get())
                if (matriz_size % 2 == 0):
                    matriz_size += 1
                    prSetTxt(self.__parameter1_entry,str(matriz_size))
                image = cv.Laplacian(self.__final_image_cv,-1,matriz_size)
                self.__InnerSave(image)

        elif(wanted_effect == "Sharpened"):
            if(self.__color_model != "BIN"):
                if(self.__selected_option_for_sharpened.get() != "Free"):
                    image = cv.filter2D(self.__final_image_cv,-1,self.__kernel)
                else:
                    size = len(self.__my_entries_for_kernel)
                    self.__kernel = []
                    for i in range(0,size):
                        for j in range(0,size):
                            value = self.__my_entries_for_kernel[i][j].get()
                            try:
                                self.__kernel.append(int(value))
                            except ValueError:
                                if(value in ["", " "]):
                                    self.__kernel.append(0)
                                else:
                                    self.__kernel.append(-1)
                    self.__kernel = np.array(self.__kernel).reshape(size,size)
                    image = cv.filter2D(self.__final_image_cv,-1,self.__kernel)
                    

                self.__InnerSave(image)
        
        elif (wanted_effect == "Sharpened_Image"):
            if(self.__color_model != "BIN"):
                if(self.__color_model == "RGB"):
                    image = Image.fromarray(self.__final_image_cv, mode = "RGB")  
                else:
                    image = Image.fromarray(self.__final_image_cv, mode = "L")
                image = image.filter(ImageFilter.SHARPEN())
                image = np.array(image)
                self.__InnerSave(image)
        
        elif (wanted_effect == "MinFilter"):
            if(self.__color_model != "BIN"):
                if(self.__color_model == "RGB"):
                    image = Image.fromarray(self.__final_image_cv, mode = "RGB")  
                else:
                    image = Image.fromarray(self.__final_image_cv, mode = "L")
                size = int(self.__parameter1_entry.get())
                if (size % 2 == 0):
                    size += 1
                    prSetTxt(self.__parameter1_entry,str(size))
                image = image.filter(ImageFilter.MinFilter(size))
                image = np.array(image)
                self.__InnerSave(image)

        elif (wanted_effect == "CONTOUR"):
            if(self.__color_model != "BIN"):
                if(self.__color_model == "RGB"):
                    image = Image.fromarray(self.__final_image_cv, mode = "RGB")  
                else:
                    image =  image = Image.fromarray(self.__final_image_cv, mode = "L")
                image = image.filter(ImageFilter.CONTOUR())
                image = np.array(image)
                self.__InnerSave(image)
                
        elif (wanted_effect == "Canny"):
            if(self.__color_model != "BIN"):
                size = int(self.__parameter1_entry.get().strip())
                if(size % 2 == 0):
                    size += 1
                    prSetTxt(self.__parameter1_entry, str(size))
                value = self.__parameter2_entry.get().strip()
                value = int(float(value))
                prSetTxt(self.__parameter2_entry, str(value))
                ratio = int(self.__combo.get()[-1])
                if(self.__color_model == "RGB"):
                    image = cv.cvtColor(self.__final_image_cv, cv.COLOR_RGB2GRAY)
                else:
                    if(len(image.shape[-1])==3):
                        image = cv.cvtColor(self.__final_image_cv, cv.COLOR_RGB2GRAY)
                
                image = cv.blur(image,(size,size))
                image = cv.Canny(image,value,value * ratio)
                self.__InnerSave(image)
                    
                    
        

        elif (wanted_effect == "DETAIL"):
            if(self.__color_model != "BIN"):
                if(self.__color_model == "RGB"):
                    image = Image.fromarray(self.__final_image_cv, mode = "RGB")  
                else:
                    image =  image = Image.fromarray(self.__final_image_cv, mode = "L")
                image = image.filter(ImageFilter.DETAIL())
                image = np.array(image)
                self.__InnerSave(image)

        elif (wanted_effect == "EDGE_ENHANCE"):
            if(self.__color_model != "BIN"):
                if(self.__color_model == "RGB"):
                    image = Image.fromarray(self.__final_image_cv, mode = "RGB")  
                else:
                    image =  image = Image.fromarray(self.__final_image_cv, mode = "L")
                image = image.filter(ImageFilter.EDGE_ENHANCE())
                image = np.array(image)
                self.__InnerSave(image)

        elif (wanted_effect == "EDGE_ENHANCE_MORE"):
            if(self.__color_model != "BIN"):
                if(self.__color_model == "RGB"):
                    image = Image.fromarray(self.__final_image_cv, mode = "RGB")  
                else:
                    image =  image = Image.fromarray(self.__final_image_cv, mode = "L")
                image = image.filter(ImageFilter.EDGE_ENHANCE_MORE())
                image = np.array(image)
                self.__InnerSave(image)

        elif (wanted_effect == "EMBOSS"):
            if(self.__color_model != "BIN"):
                if(self.__color_model == "RGB"):
                    image = Image.fromarray(self.__final_image_cv, mode = "RGB")  
                else:
                    image =  image = Image.fromarray(self.__final_image_cv, mode = "L")
                image = image.filter(ImageFilter.EMBOSS())
                image = np.array(image)
                self.__InnerSave(image)
        
        elif (wanted_effect == "FIND_EDGES"):
            if(self.__color_model != "BIN"):
                if(self.__color_model == "RGB"):
                    image = Image.fromarray(self.__final_image_cv, mode = "RGB") 
                else:
                    image =  image = Image.fromarray(self.__final_image_cv, mode = "L")
                image = image.filter(ImageFilter.FIND_EDGES())
                image = np.array(image)
                self.__InnerSave(image)



        elif (wanted_effect == "GRAY"):
            if(self.__color_model == "RGB"):
                image = cv.cvtColor(self.__final_image_cv,cv.COLOR_RGB2GRAY)
                self.__InnerSave(image)
        
        elif(wanted_effect == "BGR"):
            if(self.__color_model == "RGB"):
                image = self.__final_image_cv[:,:,::-1]
                self.__InnerSave(image)
                self.__color_model = "BGR"

        elif (wanted_effect == "CMY"):
            if(self.__color_model == "RGB"):
                image = 255 - self.__final_image_cv
                self.__InnerSave(image)
                self.__color_model = "CMY"
        
        elif (wanted_effect == "HSV"):
            if(self.__color_model == "RGB"):
                image = cv.cvtColor(self.__final_image_cv,cv.COLOR_RGB2HSV)
                self.__InnerSave(image)
                self.__color_model = "HSV"
        
        elif (wanted_effect == "HLS"):
            if(self.__color_model == "RGB"):
                image = cv.cvtColor(self.__final_image_cv,cv.COLOR_RGB2HLS)
                self.__InnerSave(image)
                self.__color_model = "HLS"
        
        elif (wanted_effect == "YCrCb"):
            if(self.__color_model == "RGB"):
                image = cv.cvtColor(self.__final_image_cv,cv.COLOR_RGB2YCrCb)
                self.__InnerSave(image)
                self.__color_model = "YCrCb"

        elif (wanted_effect == "BINARY"):
            if(self.__color_model == "RGB"):
                try:
                    umbral = float(self.__parameter1_entry.get().strip())
                    if(umbral>255 or umbral < 0):
                        umbral = np.mean(self.__final_image_cv)
                except ValueError:
                    umbral = np.mean(self.__final_image_cv)
                
                image_gray = cv.cvtColor(self.__final_image_cv.astype("uint8"),cv.COLOR_RGB2GRAY)
                image_bin = cv.threshold(image_gray,umbral,255,cv.THRESH_BINARY)[1]
                self.__InnerSave(image_bin)
            elif(self.__color_model == "GRAY"):
                try:
                    umbral = int(self.__parameter1_entry.get().strip())
                    if(umbral>255 or umbral < 0):
                        umbral = np.mean(self.__final_image_cv)
                except ValueError:
                    umbral = np.mean(self.__final_image_cv)
                if(len(self.__final_image_cv.shape) == 3):
                    image_gray = cv.cvtColor(self.__final_image_cv,cv.COLOR_RGB2GRAY)
                else:
                    image_gray = self.__final_image_cv
                image_bin = cv.threshold(image_gray,umbral,255,cv.THRESH_BINARY)[1]
                self.__InnerSave(image_bin)
        
        elif (wanted_effect == "BINARY MEAN C"):
            if(self.__color_model == "RGB"):
                image_gray = cv.cvtColor(self.__final_image_cv,cv.COLOR_RGB2GRAY)
                image_bin = cv.adaptiveThreshold(image_gray,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,11,7)
                self.__InnerSave(image_bin)
            elif(self.__color_model == "GRAY"):
                image_bin = cv.adaptiveThreshold(self.__final_image_cv,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,11,7)
                self.__InnerSave(image_bin)

        elif (wanted_effect == "BINARY OTSU"):
            if(self.__color_model == "RGB"):
                image_gray = cv.cvtColor(self.__final_image_cv,cv.COLOR_RGB2GRAY)
                image_bin = cv.threshold(image_gray,0,255,cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
                self.__InnerSave(image_bin)
            elif(self.__color_model == "GRAY"):
                if(len(self.__final_image_cv.shape) == 3):
                    image_gray = cv.cvtColor(self.__final_image_cv,cv.COLOR_RGB2GRAY)
                else:
                    image_gray = self.__final_image_cv
                image_bin = cv.threshold(image_gray,0,255,cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
                self.__InnerSave(image_bin)

        elif (wanted_effect == "Erode"):
            if(self.__color_model == "BIN"):
                se_type = self.__selected_option_for_cv_se.get()
                size = int(self.__parameter1_entry.get())
                if(size % 2 == 0):
                    size += 1

                iterations = int(self.__parameter2_entry.get())
                if(se_type == "RECT"):
                    se = cv.getStructuringElement(cv.MORPH_RECT,(size,size))
                elif(se_type == "CROSS"):
                    se = cv.getStructuringElement(cv.MORPH_CROSS,(size,size))
                elif (se_type == "ELLIPSE"):
                    se = cv.getStructuringElement(cv.MORPH_ELLIPSE,(size,size))
                
                erosionada = cv.erode(self.__final_image_cv,kernel = se, iterations=iterations)
                self.__InnerSave(erosionada)
        
        elif (wanted_effect == "Dilate"):
            if(self.__color_model == "BIN"):
                se_type = self.__selected_option_for_cv_se.get()
                size = int(self.__parameter1_entry.get())
                if(size % 2 == 0):
                    size += 1
                    prSetTxt(self.__parameter1_entry,str(size))
                iterations = int(self.__parameter2_entry.get())
                if(se_type == "RECT"):
                    se = cv.getStructuringElement(cv.MORPH_RECT,(size,size))
                elif(se_type == "CROSS"):
                    se = cv.getStructuringElement(cv.MORPH_CROSS,(size,size))
                elif (se_type == "ELLIPSE"):
                    se = cv.getStructuringElement(cv.MORPH_ELLIPSE,(size,size))
                
                erosionada = cv.dilate(self.__final_image_cv,kernel = se, iterations=iterations)
                self.__InnerSave(erosionada)

        elif (wanted_effect == "Open"):
            if(self.__color_model == "BIN"):
                se_type = self.__selected_option_for_cv_se.get()
                size = int(self.__parameter1_entry.get())
                if(size % 2 == 0):
                    size += 1
                    prSetTxt(self.__parameter1_entry,str(size))
                iterations = int(self.__parameter2_entry.get())
                if(se_type == "RECT"):
                    se = cv.getStructuringElement(cv.MORPH_RECT,(size,size))
                elif(se_type == "CROSS"):
                    se = cv.getStructuringElement(cv.MORPH_CROSS,(size,size))
                elif (se_type == "ELLIPSE"):
                    se = cv.getStructuringElement(cv.MORPH_ELLIPSE,(size,size))
                
                img_open = cv.morphologyEx(self.__final_image_cv,cv.MORPH_OPEN,kernel = se,iterations= iterations)
                self.__InnerSave(img_open)
        
        elif (wanted_effect == "Close"):
            if(self.__color_model == "BIN"):
                se_type = self.__selected_option_for_cv_se.get()
                size = int(self.__parameter1_entry.get())
                if(size % 2 == 0):
                    size += 1
                    prSetTxt(self.__parameter1_entry,str(size))
                iterations = int(self.__parameter2_entry.get())
                if(se_type == "RECT"):
                    se = cv.getStructuringElement(cv.MORPH_RECT,(size,size))
                elif(se_type == "CROSS"):
                    se = cv.getStructuringElement(cv.MORPH_CROSS,(size,size))
                elif (se_type == "ELLIPSE"):
                    se = cv.getStructuringElement(cv.MORPH_ELLIPSE,(size,size))
                
                img_close = cv.morphologyEx(self.__final_image_cv,cv.MORPH_CLOSE,kernel = se,iterations= iterations)
                self.__InnerSave(img_close)
        
        elif (wanted_effect == "Hit or Miss"):
            if(self.__color_model == "BIN"):
                kernel = []
                for i in range(0,len(self.__my_entries_for_kernel)):
                    row = []
                    for j in range(0, len(self.__my_entries_for_kernel[0])):
                        value = self.__my_entries_for_kernel[i][j].get()
                        try:
                            row.append(int(value))
                        except ValueError:
                            if(value in  ["", " "]):
                                row.append(0)
                            elif value == "-":
                                row.append(-1)
                    kernel.append(row)

                kernel = np.array(kernel,dtype="int64")
                
                htm = cv.morphologyEx(self.__final_image_cv,cv.MORPH_HITMISS, kernel = kernel)

                self.__InnerSave(htm)


    def __InnerSave(self,image):
        try:
            if ((len(image.shape) == 2 and len(np.unique(image))>2) or (len(image) == 3 and ((image[:,:,0].all()== image[:,:,1]).all() and ((image[:,:,0].all()== image[:,:,2]).all())))):
                self.__color_model = "GRAY"
            elif(len(image.shape) == 3):
                self.__color_model = "RGB"
            else:
                self.__color_model = "BIN"
        except TypeError:
            self.__color_model = "BIN"

        self.__list_cv_images.append(image)
        
        if(self.__color_model == "RGB"):
            image = image[:,:,::-1]
        
        cv.imwrite(self.__route_to_save,image)


        image_tk = tk.PhotoImage(file = self.__route_to_save)
        self.__list_tk_images.append(image_tk)  

        self.__aCurr_final_image += 1

        self.__final_image_cv = self.__list_cv_images[self.__aCurr_final_image]
    
        self.__final_image_tk = self.__list_tk_images[self.__aCurr_final_image]
        
        

        self.__final_image_portrait.configure(image = self.__final_image_tk)


        

FilterSystem = WindowFilterSystem()