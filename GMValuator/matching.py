import faiss
import math
import numpy as np
from PIL import Image
from imgbeddings import imgbeddings
from torchvision import datasets

def init_PQ(vec):
    '''
    :param vec: vector embedding of all the training data points
    :return: indices(ranking top k training data points from left to right), distances(the distances of ranking top k training data points)
    '''
    dimension = len(vec[0])
    quantizer = faiss.IndexFlatL2(dimension)  # coarse quantizer
    # define the inverted index
    index = faiss.IndexIVFPQ(quantizer, dimension, 256, 8, 8)
    index.train(vec)
    index.add(vec)
    return index

def convertSimilarity(distanceArray):
    '''
    Convert distance to similarity and normalized
    :param distanceArray:
    :return:
    '''
    sum_exp = 0
    similarity = []
    for dis in distanceArray:
        sum_exp += math.exp(-dis)

    for dis in distanceArray:
        sim = math.exp(-dis) / sum_exp
        similarity.append(sim)

    return similarity

def matching(generated_img):
    print("=========matching=========")
    # initialize faiss
    original_embedding = np.load(f'./GMValuator/assets/mnist_embedding.npz')['arr_0']
    init_search = init_PQ(original_embedding)
    imgbedding = imgbeddings()

    # embedding input generated data
    query_embedding = imgbedding.to_embeddings(generated_img)

    # Similarity search
    distances, indices = init_search.search(query_embedding, 4)
    print("distances", distances[0])
    print("indices:", indices[0])

    # get value of each matched image
    similarity_scores = convertSimilarity(distances[0])
    print('similarity scores:', similarity_scores)

    # vislualize matched images
    matched_images = []
    train_datasets = datasets.MNIST('./GMValuator/data', train=True, download=False)
    for idx in indices[0]:
        matched_images.append(train_datasets[idx][0])

    return matched_images, similarity_scores

if __name__ == '__main__':
    matching('./GMValuator/mnist-0.png')
