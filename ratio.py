import RPi.GPIO as GPIO
from hx711 import HX711
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


DT1 = 17
SCK1 = 18

DT2 = 22
SCK2 = 23

DT3 = 26
SCK3 = 20


def zero_fun():
    """初始值"""
    zero1 = HX711(SCK1, DT1).getdv()
    zero2 = HX711(SCK2, DT2).getdv()
    zero3 = HX711(SCK3, DT3).getdv()
    return (zero1 + zero2 + zero3)/3


def average_fun(num):
    """计算列表平均数"""
    nsum = 0
    for i in range(len(num)):
        nsum += num[i]
    return nsum / len(num)


def ratio_avg():
    """计算称重系数"""
    nums = []
    for _ in range(3):
        print('请放200g砝码...')
        time.sleep(3)
        mod = (zero_fun() - initial)/200
        nums.append(mod)
        print('拿走砝码!')
        time.sleep(2)
    return average_fun(nums)


initial = zero_fun()


if __name__ == '__main__':

    r = ratio_avg()

    print('3次测量平均值：{:.2f}'.format(r))
