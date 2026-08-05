# 验证：Python 对象的"地址"和大小
import sys

x = 5
y = 5
z = 6

print("=" * 50)
print("【id() = 对象在内存中的地址编号】")
print(f"x = {x} 的地址: {id(x)}")
print(f"y = {y} 的地址: {id(y)}")
print(f"z = {z} 的地址: {id(z)}")
print()
print(f"x 和 y 地址相同? {id(x) == id(y)}  ← 小整数缓存，5 只有一份")
print(f"x 和 z 地址相同? {id(x) == id(z)}  ← 6 是另一个对象")
print()

print("=" * 50)
print("【指针/地址宽度 = 机器位数】")
print(f"Python 是 {'64位' if sys.maxsize > 2**32 else '32位'} 程序")
print(f"地址编号范围: 0 ~ {sys.maxsize}")
print(f"理论上最多能寻址: {sys.maxsize} 字节 = {sys.maxsize/1024**3:.1f} GB")
print()

print("=" * 50)
print("【字 vs 字节：CPU 一次拿多少】")
print(f"Python int 对象占 {sys.getsizeof(5)} 字节（含对象头，不止 4/8 字节）")
print(f"Python list 空列表占 {sys.getsizeof([])} 字节")
