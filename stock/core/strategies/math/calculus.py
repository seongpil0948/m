import numpy as np
from typing import List, 

Vector = 

""" 
numerical_analysis(수치해석) 적으로 작성된 코드로
기존 함수의 정의 와는 조금 다를 수 있다
print(np.float32(1e-50)) # 0.0 쉣                                                                                                                                                         vus
"""
def numerucal_gradient(f,x):
  h = 1e-4  #0.0001
  grad = np.zeros_like(x)
  for idx in range(x.size):
    tmp_val = x[idx]
    # f(x+h)
    x[idx] = tmp_val+h
    fxh1 = f(x)
    # f(x-h) 계산
    x[idx] = tmp_val-h
    fxh2 = f(x)    
    grad[idx] = (fxh1-fxh2)/(2*h)
    x[idx] = tmp_val

    return grad

def f1(x: List) -> List:
  return np.sum(x ** 2)

