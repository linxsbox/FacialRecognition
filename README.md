# FacialRecognition

现在的人脸识别技术已经得到了非常广泛的应用，支付领域、身份验证、美颜相机里都有它的应用。

用Python实现人脸检测。人脸检测是人脸识别的基础。人脸检测的目的是识别出照片里的人脸并定位面部特征点，人脸识别是在人脸检测的基础上进一步告诉你这个人是谁。

## 业务场景


## 实现逻辑

    人脸检测 -> 人脸识别 -> 人脸检测训练 -> 人脸识别训练

**参考来源**

人脸检测部分：[Python爱好者社区](https://mp.weixin.qq.com/s/oDMFoPh6wLYFnTP2rG2AuA) 强哥

人脸识别部分：[CVPy](https://mp.weixin.qq.com/s/3O0m7F712dwnwhpwMXck4Q) 冰不语 

## 依赖库

- Dlib: [http://dlib.net/](http://dlib.net/)
> Dlib是一个跨平台的C++公共库，除了线程支持，网络支持，提供测试以及大量工具等等优点，Dlib还是一个强大的机器学习的C++库，包含了许多机器学习常用的算法。同时支持大量的数值算法如矩阵、大整数、随机数运算等等。Dlib同时还包含了大量的图形模型算法。
- numpy
- scipy
- opencv-python

**安装所需库**

    $ pip install numpy
    $ pip install scipy
    $ pip install opencv-python
    $ pip install dlib

*方案一：免安装 dlib 方式(来自 冰不语)：
下载 blib : Python Package Index *.whl, 文件夹内 pip install dlib.whl

经过查找后得知，Dlib 依赖于 **boots** 和 **CMake**，所以需要先安装这些依赖库，并且配置环境。

> CMake: [https://cmake.org/](https://cmake.org/)  
> boot: [http://www.boost.org/](http://www.boost.org/)  
> **注：**  
> - CMake 3.10.x  
> - boots 1.66.x  
> - Dlib 19.9.x  
> - Dlib-face-landmarks 68 [训练模型](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)

**boots**  需要 **C++** 系列编译器进行编译 (以下任选其一)

> TDM-GCC: [TDM-GCC](http://tdm-gcc.tdragon.net/)  
> MSVC: [MS Tools](https://www.visualstudio.com/zh-hans/downloads/) 安装需要7G左右空间，放弃！！！

## 如何运行
