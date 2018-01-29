# Change log

## 2018年1月24日

人脸检测部分已经完成了，然后根据自己的理解，将代码进行了简单的拆分成可复用调用的方法

- 人脸检测方法：**facial_regional_marker** @params imagePath 需要识别的图片路径

> 可更新部分：接受参数不限于项目路径，即可读取多种来源路径（file path|url|相机|摄像头|……）

---

## 2018年1月25日

人脸识别部分完成，原来案例的代码也拆分出来了不同方法

**关于识别部分说明：** 对于面部识别的耗时稍长，精准度并不是很高，原案例的代码我并没有跑过，所以没确认问题是源案例的还是我更改代码后的。

- 面部模型采集方法：**facial_model_acquisition** 默认读取 **faces** 文件夹下的图片 
- 人脸检测方法：**facial_feature** @params imagePath 需要识别的图片路径

> 可更新部分：目前还需手动添加面部模型对应名称，读取路径可独立成一个方法，返回 **image** 对象

---

## 2018年1月26日

关于面部识别耗时较长的问题进行简单的梳理。

开始对代码进行优化，在简单的整理代码后发现 **可能** 存在性能问题的地方进行改造。

将 **可能** 部分优化完后后续再进行性能测试来具体发生在那个阶段的问题。

1. 将引入模型进行提取为独立的方法在运行时进行初始化，不再是方法内调用。
2. 遍历文件优化方法，将 **glob** 替换成 **os.listdir**。
3. 将 **detector** 配置第二参数取消，直接使用原图可以提升 约200ms 左右的处理时间。

> 关于正面人脸检测器 **detector**  
> **detector(image, 1), detector = dlib.get_frontal_face_detector()**  
> 单张耗时 150~450ms，未尝试过大体积文件 size > 1024kb

> 关于人脸特征描述 **descriptor**  
> **descriptor.compute_face_descriptor(image, shape)**  
> 单张耗时 > 500ms，未尝试过大体积文件 size > 1024kb

> 关于遍历优化，测试了数据样本为 10, 130, 310, 1330, 2660, 5320个文件的情况。  
> 测试方法为 **glob.glob**，**os.listdir**，**os.walk** 三种

**测试代码：**

```python
from time import clock
dirname = './imgs'
def testGLOB():
    start_time = clock()
    for file in glob.glob(dirname + '/*'):
        head, tail = os.path.split(file)
    end_time = clock()
    print("method glob costs time is : " , str(end_time - start_time))

def testListdir():
    start_time = clock()
    for file in os.listdir(dirname):
        os.path.join(dirname, file)
    end_time = clock()
    print("method list costs time is : " , str(end_time - start_time))

def testWalk():
    start_time = clock()
    for(dirname, subshere, fileshere) in os.walk('.'):
        for fname in fileshere:
            os.path.join(dirname, fname)
    end_time = clock()
    print("method walk costs time is : " , str(end_time - start_time))
```

**结论：**

> **os.listdir** 在文件越多的情况下优势越明显  
> **os.listdir** > **glob.glob** > **os.walk**

---

## 2018年1月29日

动态追踪学习实现

参考 [http://python.jobbole.com/81593/](http://python.jobbole.com/81593/)

**原理：** 主要是利用了摄像头读取到的 **第一帧(first frame)** 作为背景模型，以及对读取到的每一帧都做预处理，先转 **灰度图**，再进行 **高斯滤波**，然后会对这些帧进行计算与背景的差异值，从而得到 **分差图（different map）**，这样就可以得到和捕获动态物体的轮廓了，最后再输出出来即可。

```python
# Camera object.
camera = cv2.VideoCapture(0)

# Read the camera frame, it's loop.
while Ture:
    grabbed, frame = camera.read()

    ……
    # Color revised
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # GaussianBlur
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    ……

    # different map
    frameDelta = cv2.absdiff(firstFrame, gray)
    # threshold to binary
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # Morphological dilation.  
    thresh = cv2.dilate(thresh, es, iterations = 2)
    _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

```