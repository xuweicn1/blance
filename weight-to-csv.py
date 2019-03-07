import RPi.GPIO as GPIO
from hx711 import HX711
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


# y = -0.4809x + 119.91 线性关系式

# x：子秤重量
# y：距离子秤距离

DT1 = 17
SCK1 = 18

DT2 = 22
SCK2 = 23

DT3 = 26
SCK3 = 20

DIF = 250  # 波动系数
ROT = 299.53  # 称重系数


def zero_fun():
    """初始值"""
    zero1 = HX711(SCK1, DT1).getdv()
    zero2 = HX711(SCK2, DT2).getdv()
    zero3 = HX711(SCK3, DT3).getdv()
    return (zero1 + zero2 + zero3)/3, zero1, zero2, zero3,


def calculate_difference():
    """计算读数差值"""
    cont = zero_fun()
    d0 = cont[0] - initial[0]
    d1 = cont[1] - initial[1]
    d2 = cont[2] - initial[2]
    d3 = cont[3] - initial[3]
    
    # 过滤波动值
    if d0 < DIF:
        d0 = 0
    if d1 < DIF:
        d1 = 0
    if d2 < DIF:
        d2 = 0
    if d3 < DIF:
        d3 = 0

    return d0, d1, d2, d3


def calculate_weight():
    """计算重量"""
    d = calculate_difference()
    w = [i/ROT for i in d]
    return w

    
def weigth_to_csv(file,lst,lenth):
    """将列表写入文件"""
    with open(file, 'a') as csvfile:
        for i, v in enumerate(lst):
            csvfile.write(str(v)+',')
        csvfile.write(str(lenth)+'\n')


initial = zero_fun()

if __name__ == '__main__':


    while True:
        time.sleep(2)
        w = calculate_weight()
        weigth_to_csv('a.csv',w,1.0)
        
        print('实 重：{:.2f}g;\n秤--1：{:.2f}g;\n秤--2：{:.2f}g;\n秤--3：{:.2f}g;'.format(
            w[0], w[1], w[2], w[3]))
        print('*'*20)

