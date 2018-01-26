import os, dlib, cv2
from time import clock
from skimage import io

dirname = './imgs'

# test foreach
def testGLOB():
    start_time = clock()
    for file in glob.glob(dirname + '/*'):
        head, tail = os.path.split(file)
        # print(head, tail, '=>', ('C:\\Other\\' + tail))
    end_time = clock()
    print("method glob costs time is : " , str(end_time - start_time))

def testListdir():
    start_time = clock()
    for file in os.listdir(dirname):
        os.path.join(dirname, file)
        # print(dirname, file, '=>', )
    end_time = clock()
    print("method list costs time is : " , str(end_time - start_time))

def testWalk():
    start_time = clock()
    for(dirname, subshere, fileshere) in os.walk('.'):
        # print('[' + dirname + ']')
        for fname in fileshere:
            os.path.join(dirname, fname)
            # print()
    end_time = clock()
    print("method walk costs time is : " , str(end_time - start_time))

# testGLOB()
# testListdir()
# testWalk()

# test read image
def vc2imread():
    start_time = clock()

    for file in os.listdir(dirname):
        image = cv2.imread(os.path.join(dirname, file))

    end_time = clock()
    print("CV2.imread time is : " , str(end_time - start_time))

def ioimread():
    start_time = clock()

    for file in os.listdir(dirname):
        image = io.imread(os.path.join(dirname, file))

    end_time = clock()
    print("io.imread time is : " , str(end_time - start_time))

vc2imread()
ioimread()