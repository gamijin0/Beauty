import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm
import numpy
import time
import moviepy.editor as mpy
import images2gif

class MyFigure:

    #==========================================
    dirName = "" #主文件夹名
    imgDirName="img" #用于保存图片
    gifDirName="gif" #用于保存gif
    figure = plt.figure()
    mand = numpy.array([0])
    extent = []
    radius =0
    evolveRate=0.85
    #==========================================

    # 创建主文件夹及img,gif文件夹 #
    def __init__(self,dirName):
        self.dirName = dirName
        import os
        if(os.path.isdir(self.dirName)==False):# if NOT exists
            print("["+dirName+"] has been created.")
            os.mkdir(dirName)
        if(os.path.isdir(self.dirName+"/"+self.imgDirName)==False):# if NOT exists
            print("["+self.dirName+"/"+self.imgDirName+"] has been created.")
            os.mkdir(self.dirName+"/"+self.imgDirName)
        if(os.path.isdir(self.dirName+"/"+self.gifDirName)==False):# if NOT exists
            print("["+self.dirName+"/"+self.gifDirName+"] has been created.")
            os.mkdir(self.dirName+"/"+self.gifDirName)
        # else:# if exists
        #     import shutil
        #     shutil.rmtree(dirName)  # 删除
        #     os.mkdir(dirName)
        #     print("["+dirName+"] has been deleted and created.")
        self.figure = plt.figure(1,(16,16))
        plt.gca().set_axis_off()  # 不显示坐标
        plt.rcParams['toolbar'] = 'None' #不显示工具栏
        pass

    # 迭代判断
    def iter_point(self,c):
        import math
        z = c
        for i in range(1, 100):  # 最多迭代100次
            if abs(z) > 100: break  # 半径大于2则认为逃逸:
            z = z*z+c


            # +math.sin(abs(z))-math.sin(abs(z))
        return i  # 返回迭代次数

    # 产生Mandelbort集合 #
    def GetMandelbort(self,cx, cy, d,border_length):
        # 绘制点(cx, cy)附近正负d的范围的Mandelbrot
        self.radius = d
        x0, x1, y0, y1 = cx - d, cx + d, cy - d, cy + d
        y, x = numpy.ogrid[y0:y1:(border_length)*1j, x0:x1:(border_length)*1j]
        c = x + y * 1j
        start = time.clock()
        mandelbrot = numpy.frompyfunc(self.iter_point,1, 1)(c).astype(numpy.float)
        #mandelbrot = numpy.array(c).astype(numpy.float)
        print("time=", time.clock() - start)
        self.extent = [x0, x1, y0, y1]
        return mandelbrot

    #产生图像数据 #
    def GenerateData(self,cx,cy,border_length,radius):
        # plt.subplot(111)
        print("self.radius:",self.radius)
        self.extent=[-1*self.radius,self.radius,-1*self.radius,self.radius]
        self.figure.add_subplot(111)
        self.mand=self.GetMandelbort(cx, cy,radius,border_length=border_length)
        pass

    #产生图像 #
    def GenerateImg(self,cx,cy,dpi,bgcolor="None"):

        color_str="Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spectral, spectral_r, spring, spring_r, summer, summer_r, terrain, terrain_r, viridis, viridis_r, winter, winter_r"
        color_list=color_str.split(", ")
        print(len(color_list))

        self.GenerateData(radius=self.radius,cx=cx,cy=cy,border_length=dpi)
        self.figure.add_subplot(111)
        #plt.plot(numpy_data)
        import random
        #print(color_list[random.randint(2,152)])
        if(bgcolor=="None"):
            MyColor =cm.get_cmap(color_list[random.randint(3,100)],random.randint(700,1300))
        else:
            MyColor = cm.get_cmap(bgcolor,random.randint(700,1300))
        #print(MyColor)
        MyData =self.mand
        # for i in range(4):
        #     MyData+=numpy.rot90(MyData)
        print(self.extent)
        plt.imshow(MyData, cmap=MyColor, extent=self.extent)
        pass

    # 保存图像
    def SaveImg(self,fileName="",dpi=400):
        if(fileName==""):
            fileName="index"
        import os
        if(os.path.isfile(self.dirName+"/"+self.imgDirName+"/"+fileName+".png")==True):
            print("["+fileName+".png] 已存在.")
            self.SaveImg(fileName+"*",dpi=dpi)
            return
        self.figure.savefig(self.dirName+"/"+self.imgDirName+"/"+fileName,dpi=dpi)
        print("img saved.")
        pass

    #渐变图像
    def Evolve(self,t):
        #t : seconds
        x, y = 0.27322626, 0.595153338
        print("time:",t)
        from moviepy.video.io.bindings import mplfig_to_npimage
        self.mand = self.mand+numpy.rot90(self.mand)
        d=2*((self.evolveRate)**(t*10))
        print("radius:",d)
        self.mand=self.GetMandelbort(cx=x,cy=y,d=d,border_length=200)
        self.GenerateImg(border_length=200,cx=x,cy=y,bgcolor="Blues_r")
        return mplfig_to_npimage(fig=self.figure)

        pass


    #用图片合成GIF
    def GenerateGif(self,fileName,timeLen,fps=10,evolveRate=0.85):
        # import os
        # filelist=os.listdir(self.dirName+"/"+self.imgDirName+"/")
        # print("现有img:"+str(filelist))
        self.evolveRate=evolveRate
        animation = mpy.VideoClip(self.Evolve,duration=timeLen)
        animation.write_gif(self.dirName+"/"+self.gifDirName+"/"+fileName,fps=fps)
        pass

    #展示图像
    def Show(self):
        #self.figure.show()
        plt.show()
        pass




if(__name__=='__main__'):
    testone = MyFigure("TestOne")
    #testone.GenerateImg(400,bgcolor="Set1_r")
    #testone.GenerateImg(border_length=200,bgcolor="Blues_r")
    #testone.Show()
    testone.SaveImg(dpi=600)
    testone.GenerateImg(0.27322626,0.595153338,dpi=300)
    testone.GenerateGif(fileName="test.gif",timeLen=10,fps=30,evolveRate=0.96)