import heapq
import numpy as np
import cv2
import os

class HuffmanNode:
    def __init__(self, value, frequency):
        self.value = value
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def calculate_frequencies(image_array):
    frequency_dict = {}
    for pixel in image_array.flatten():
        if pixel in frequency_dict:
            frequency_dict[pixel] += 1
        else:
            frequency_dict[pixel] = 1
    return frequency_dict

def build_huffman_tree(frequencies):
    heap = [HuffmanNode(value, freq) for value, freq in frequencies.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.frequency + node2.frequency)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
    
    return heap[0]

def generate_huffman_codes(node, prefix="", codebook={}):
    if node is not None:
        if node.value is not None:
            codebook[node.value] = prefix
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)
    return codebook

def encode_image(image_array, codebook):
    encoded_image = ""
    for pixel in image_array.flatten():
        encoded_image += codebook[pixel]
    return encoded_image

def save_encoded_data(encoded_image, codebook, image_shape, filename):
    with open(filename, 'w') as f:
        f.write(f"{image_shape}\n")
        f.write(f"{str(codebook)}\n")
        f.write(encoded_image)

def load_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image_array = np.array(image)
    return image_array

def huffman_compress(image_path, output_filename):
    image_array = load_image(image_path)
    frequencies = calculate_frequencies(image_array)
    huffman_tree = build_huffman_tree(frequencies)
    codebook = generate_huffman_codes(huffman_tree)
    encoded_image = encode_image(image_array, codebook)
    save_encoded_data(encoded_image, codebook, image_array.shape, output_filename)

script_dir = os.path.dirname(os.path.realpath(__file__))
input_image_path = os.path.join(script_dir, 'original.jpg')
huffman_compress(input_image_path, 'h.txt')
