from modular_arithmetic import *
import matplotlib.pyplot as plt
import matplotlib

font = {
    'weight' : 'normal',
    'size' : 16
}

matplotlib.rc('font', **font)


# Experiment for 3^x % 35

data = [exp_modular(35, 3, i) for i in range(37)]
ones = [i for i in range(len(data)) if data[i] == 1]
T = ones[1] - ones[0]

plt.figure(facecolor='white')
plt.plot(range(37), data, marker='x', ls='--', linewidth=2)
plt.plot(ones, [1] * len(ones), marker='x', color='red', linestyle='None')
plt.xlabel('x')
plt.ylabel(r'$3^{x}$ mod 35')
plt.title('Example where T: ' + str(T))
plt.show()

# Experiment for 7^x % 173

data = [exp_modular(173, 7, i) for i in range(200)]
ones = [i for i in range(len(data)) if data[i] == 1]
T = ones[1] - ones[0]

plt.figure(facecolor='white')
plt.plot(range(200), data, marker='x', ls='--', linewidth=1)
plt.plot(ones, [1] * len(ones), marker='x', color='red', linestyle='None')
plt.xlabel('x')
plt.ylabel(r'$7^{x}$ mod 173')
plt.title('Example where T: ' + str(T))
plt.show()

# Experiment for 54^x % 299

data = [exp_modular(299, 54, i) for i in range(300)]
ones = [i for i in range(len(data)) if data[i] == 1]
T = ones[1] - ones[0]

plt.figure(facecolor='white')
plt.plot(range(300), data, marker='x', ls='--', linewidth=1)
plt.plot(ones, [1] * len(ones), marker='x', color='red', linestyle='None')
plt.xlabel('x')
plt.ylabel(r'$54^{x}$ mod 299')
plt.title('Example where T: ' + str(T))
plt.show()