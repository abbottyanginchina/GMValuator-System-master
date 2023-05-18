import numpy as np
from torchvision import datasets
import matplotlib.pyplot as plt

if __name__ == '__main__':
    samples = np.load(f'./assets/samples_mnist.npz')['arr_0']

    for idx in range(10):
        plt.imsave(f'./mnist-{idx}.png', samples[idx])
    
