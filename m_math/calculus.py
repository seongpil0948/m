import numpy as np
import matplotlib.pylab as plt

""" 
numerical_analysis(수치해석) 적으로 작성된 코드로
기존 함수의 정의 와는 조금 다를 수 있다
print(np.float32(1e-50)) # 0.0 쉣                                                                                                                                                         vus
"""
def derivative(f,x):
    h = 1e-4 #0.0001
    return (
      f(x + h) - f(x - h)) / 2 * h

def partial_derivative(f, x):
  # x = 2D
  h = 1e-4  #0.0001
  grad = np.zeros_like(x)
  for idx in range(x.size): # size is flatten length
    tmp_val = x[idx]
    # f(x+h)
    x[idx] = tmp_val + h
    fxh1 = f(x)

    # f(x-h) 계산
    x[idx] = tmp_val-h
    fxh2 = f(x)    

    grad[idx] = (fxh1 - fxh2) / (2 * h)
    x[idx] = tmp_val

    return grad

def second_partial_derivative(f, x):
  

"""
def f1(x):
  return np.sum(x ** 2)


# 이처럼 (x0,x1) 각 점에서의 기울기를 계산할 수 있다.
print(
  partial_derivative(
    f1, 
    np.array([3.0,4.0, 2.0])
  )
)

# Gradient
x0 = np.arange(1, 10, 1) 
x1 = np.arange(-1, -10, -1)
X, Y = np.meshgrid(x0, x1)
X = X.flatten()
Y = Y.flatten()
grad = partial_derivative(f1, np.array([X, Y]) )

plt.figure()

plt.quiver(X, Y, -grad[0], -grad[1],  angles="xy",color="#666666")#,headwidth=10,scale=40,color="#444444")
plt.xlim([-2, 2])
plt.ylim([-2, 2])

plt.xlabel('x0')
plt.ylabel('x1')

plt.grid()

plt.legend()
plt.draw()
plt.show()
"""