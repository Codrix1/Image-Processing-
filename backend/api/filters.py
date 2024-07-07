#----------------------imports---------------------------#
import os
import cv2
import numpy as np
import random
import cmath
#--------------------------------------------------------#
#--------------------------------------------------------------------------------#   
# Get the current script directory
script_dir = os.path.dirname(os.path.realpath(__file__))
# Define the paths to the input and output images
input_image_path = os.path.join(script_dir, 'original.jpg')
output_image_path = os.path.join(script_dir, 'manipulatedImage.jpg')
reference_image_path = os.path.join(script_dir, 'reference.jpg')

image = cv2.imread(input_image_path, cv2.IMREAD_COLOR)

def WriteImage(Edited_image):
    cv2.imwrite(output_image_path, Edited_image)
    return 

#--------------------------------------------------------#

def DFT(image):
    M, N = image.shape
    dft = np.zeros((M, N), dtype=complex)
    for u in range(M):
        for v in range(N):
            sum_val = 0
            for x in range(M):
                for y in range(N):
                    sum_val += image[x, y] * np.exp(-2j * np.pi * ((u * x) / M + (v * y) / N))
            dft[u, v] = sum_val
    return dft

def Median(Kernel):
    image = cv2.imread(input_image_path, cv2.IMREAD_COLOR)
    img = image.copy()
    pad_size = Kernel // 2
    for channel in range(image.shape[2]):
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                temp = []
                for a in range(-pad_size, pad_size + 1):
                    for b in range(-pad_size, pad_size + 1):
                        ni, nj = i + a, j + b
                        if 0 <= ni < image.shape[0] and 0 <= nj < image.shape[1]:
                            temp.append(image[ni, nj, channel])
                        else:
                            temp.append(0)  # Pad with zero
                #print(temp)
                temp.sort()
                img[i, j, channel] = temp[len(temp) // 2]
    
    WriteImage(img)
    return
    

#--------------------------------------------------------------------------------#    
def Averaging(Kernel):
    image = cv2.imread(input_image_path, cv2.IMREAD_COLOR)
    img = image.copy()
    pad_size = Kernel // 2
    for channel in range(image.shape[2]):
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                temp = []
                for a in range(-pad_size, pad_size + 1):
                    for b in range(-pad_size, pad_size + 1):
                        ni, nj = i + a, j + b
                        if 0 <= ni < image.shape[0] and 0 <= nj < image.shape[1]:
                            temp.append(image[ni, nj, channel])
                        else:
                            temp.append(0) 
                #print(pad_size) 
                img[i][j][channel] = int(sum(temp)/(Kernel*Kernel))
    WriteImage(img)
    return 
#--------------------------------------------------------------------------------#    
def create_gaussian_noise(mean, standard_deviation):
    image = cv2.imread(input_image_path)
    img = image.copy()
    noisy_image = np.zeros(image.shape)
    gaussian_noise = np.random.normal(mean, standard_deviation, img.shape)
    for channel in range(img.shape[2]):
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                pixel = img[(i, j, channel)]
                new_pixel = pixel + gaussian_noise[i, j, channel]
                noisy_image[i, j, channel] = np.clip(new_pixel, 0, 255)

    noisy_image = noisy_image.astype("uint8")
    WriteImage(noisy_image)
    return   
#--------------------------------------------------------------------------------#       
def unsharp_masking_and_highboost_filtering(k_value):
    image = cv2.imread(input_image_path)
    img = (image).copy().astype(np.float32)
    Median(3)
    blurred_img =cv2.imread(output_image_path).copy().astype(np.float32)
    # mask = np.zeros(img.shape)
    # sharpened_img = np.zeros(img.shape)
    # for channel in range(img.shape[2]):
    #     for i in range(img.shape[0]):
    #         for j in range(img.shape[1]):
    #             mask[i, j, channel] = img[i, j, channel] - blurred_img[i, j, channel]
    #             sharpened_img[i, j, channel] = img[i, j, channel] + k_value * mask[i, j, channel]
    mask = img - blurred_img
    sharpened_img = img + k_value * mask
    WriteImage(sharpened_img)
    return   
#--------------------------------------------------------------------------------#       
def adaptive_median_filter(passed_window_size):
    image = cv2.imread(input_image_path)
    img = image.copy().astype(int)
    s_max = 9
    filtered_image = np.zeros(img.shape, dtype="uint8")
    for channel in range(img.shape[2]):
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                window_size = passed_window_size
                while window_size <= s_max:
                    temp = []
                    for a in range(-window_size // 2, (window_size // 2) + 1):
                        for b in range(-window_size // 2, (window_size // 2) + 1):
                            if 0 <= (i + a) < img.shape[0] and 0 <= (j + b) < img.shape[1]:
                                temp.append(img[i + a, j + b, channel])
                    if len(temp) == 0:
                        break
                    temp.sort()
                    median = temp[int((len(temp) / 2) - 1)]
                    a1 = median - temp[0]
                    a2 = median - temp[-1]
                    if a1 > 0 and a2 < 0:
                        b1 = img[i, j, channel] - temp[0]
                        b2 = img[i, j, channel] - temp[-1]
                        if b1 > 0 and b2 < 0:
                            filtered_image[i, j, channel] = img[i, j, channel]
                        else:
                            filtered_image[i, j, channel] = median
                        break
                    else:
                        if window_size < s_max:
                            window_size += 2
                        else:
                            filtered_image[i, j, channel] = median
                            break
    WriteImage(filtered_image)
    return
    
    
    # Read the input image  
#--------------------------------------------------------------------------------# 
def calculate_histogram(image):
    histogram = [0] * 256
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pixel_value = image[i, j]
            histogram[pixel_value] += 1
    return histogram

def calculate_cdf(histogram):
    cdf = [0] * 256
    cdf[0] = histogram[0]
    for i in range(1, 256):
        cdf[i] = cdf[i - 1] + histogram[i]
    return cdf

def histogram_equalization():
    image = cv2.imread(input_image_path)
    equalized_image = image.copy()
    for channel in range(image.shape[2]):
        histogram = calculate_histogram(image[:, :, channel])
        cdf = calculate_cdf(histogram)
        total_pixels = image.shape[0] * image.shape[1]
        equalized_histogram = [round((cdf[i] * 255) / total_pixels) for i in range(256)]
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                equalized_image[i, j, channel] = equalized_histogram[image[i, j, channel]]
    
    WriteImage(equalized_image)
    return 
#--------------------------------------------------------------------------------# 
def gaussian_kernel(size, sigma):
    kernel = np.zeros((size, size))
    center = size // 2
    for x in range(size):
        for y in range(size):
            x_center = x - center
            y_center = y - center
            kernel[x, y] = np.exp(-(x_center**2 + y_center**2) / (2 * sigma**2))
    #kernel /= 2 * np.pi * sigma**2
    kernel /= np.sum(kernel)
    return kernel

def gaussian_filter( size, sigma):
    image = cv2.imread(input_image_path)
    pad_size = size // 2
    filtered_image = np.zeros_like(image)
    kernel = gaussian_kernel(size, sigma)
    rows = image.shape[0]
    cols = image.shape[1]
    for k in range(image.shape[2]):
        padded_image = np.pad(image[:, :, k], pad_size, mode='reflect')
        for i in range(rows):
            for j in range(cols):
                window = padded_image[i:i+size, j:j+size]
                filtered_image[i, j , k] = np.sum(window * kernel)
    
    WriteImage(filtered_image)
    return 
#--------------------------------------------------------------------------------# 
def generate_uniform_noise(image_shape, noise_level):
    height, width, channels = image_shape
    noise = np.zeros((height, width, channels))
    # Manually generate uniform noise
    for i in range(height):
        for j in range(width):
            for c in range(channels):
                noise[i, j, c] = (np.random.rand() * 2 - 1) * noise_level
    return noise

def add_uniform_noise(noise_level):

    image = cv2.imread(input_image_path)
    noise = generate_uniform_noise(image.shape, noise_level)
    noisy_image = image + noise

    height, width, channels = noisy_image.shape
    for i in range(height):
        for j in range(width):
            for c in range(channels):
                if noisy_image[i, j, c] < 0:
                    noisy_image[i, j, c] = 0
                elif noisy_image[i, j, c] > 255:
                    noisy_image[i, j, c] = 255

    WriteImage(noisy_image.astype(np.uint8))
    return 
#--------------------------------------------------------------------------------#
def interpolation_nearest_neighbor(resize_value):
    image = cv2.imread(input_image_path)
    img = image.copy()
    new_width = img.shape[1] * resize_value
    new_height = img.shape[0] * resize_value
    resized_image = np.zeros((new_height, new_width, img.shape[2]), dtype=img.dtype)
    width_ratio = img.shape[1] / resized_image.shape[1]
    height_ratio = img.shape[0] / resized_image.shape[0]
    for channel in range(resized_image.shape[2]):
        for i in range(resized_image.shape[0]):
            for j in range(resized_image.shape[1]):
                x_nearest_nb = min(round(i * height_ratio), img.shape[0] - 1)
                y_nearest_nb = min(round(j * width_ratio), img.shape[1] - 1)
                resized_image[i, j, channel] = img[x_nearest_nb, y_nearest_nb, channel]
    
    WriteImage(resized_image)
    return 

def interpolation_bilinear(resize_value):
    image = cv2.imread(input_image_path)
    img = image.copy()
    new_width = img.shape[1] * resize_value
    new_height = img.shape[0] * resize_value
    resized_img = np.zeros((new_height, new_width, img.shape[2]), dtype=img.dtype)
    width_ratio = img.shape[1] / new_width
    height_ratio = img.shape[0] / new_height
    for channel in range(resized_img.shape[2]):
        for i in range(resized_img.shape[0]):
            for j in range(resized_img.shape[1]):
                new_x = i * height_ratio
                new_y = j * width_ratio
                # get the 4 neighbors
                x_floored, y_floored = int(np.floor(new_x)), int(np.floor(new_y))
                x_ceil, y_ceil = min(x_floored + 1, img.shape[0] - 1), min(y_floored + 1, img.shape[1] - 1)
                a = new_x - x_floored
                b = new_y - y_floored

                top_right_nb = img[x_ceil, y_ceil, channel]
                top_left_nb = img[x_floored, y_ceil, channel]
                bottom_right_nb = img[x_ceil, y_floored, channel]
                bottom_left_nb = img[x_floored, y_floored, channel]

                new_pixel = ((1 - a) * (1 - b) * bottom_left_nb) + (a * (1 - b) * bottom_right_nb) + (a * b * top_right_nb) + ((1 - a) * b * top_left_nb)
                resized_img[i, j, channel] = new_pixel
    
    WriteImage(resized_img)
    return 
#--------------------------------------------------------------------------------#
def sobya():    
    image = cv2.imread(input_image_path)
    img = image.copy()
    sobel_x = np.array([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]])
    sobel_y = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])
    new_img = np.zeros_like(img, dtype=np.float32)
    for channel in range(img.shape[2]):
        for i in range(1, img.shape[0] - 1):
            for j in range(1, img.shape[1] - 1):
                temp = img[i - 1: i + 2, j - 1: j + 2, channel]
                gx = np.sum(np.multiply(temp, sobel_x))
                gy = np.sum(np.multiply(temp, sobel_y))
                new_img[i, j, channel] = np.sqrt(gx**2 + gy**2)
    
    new_img = new_img / new_img.max() * 255
    new_img = new_img.astype(np.uint8)
    WriteImage(new_img)
    return 
#--------------------------------------------------------------------------------#
def apply_roberts_operator():
    image = cv2.imread(input_image_path)
    img = image.copy()
    roberts_cross_v = np.array([[1, 0], [0, -1]])
    roberts_cross_h = np.array([[0, 1], [-1, 0]])
    rows = img.shape[0]
    cols = img.shape[1]
    gradient_x = np.zeros((rows, cols), dtype=np.float32)
    gradient_y = np.zeros((rows, cols), dtype=np.float32)
    gradient_magnitude = np.zeros((rows, cols ,img.shape[2] ), dtype=np.float32)
    for k in range(img.shape[2]):
        for i in range(1, rows-1):
            for j in range(1, cols-1):
                x = (roberts_cross_v[0, 0] * img[i-1, j-1 , k] + 
                     roberts_cross_v[0, 1] * img[i-1, j , k] + 
                     roberts_cross_v[1, 0] * img[i, j-1 , k] + 
                     roberts_cross_v[1, 1] * img[i, j , k])

                y = (roberts_cross_h[0, 0] * img[i-1, j-1 , k] + 
                     roberts_cross_h[0, 1] * img[i-1, j, k] + 
                     roberts_cross_h[1, 0] * img[i, j-1, k] + 
                     roberts_cross_h[1, 1] * img[i, j, k])
                gradient_x[i, j] = x
                gradient_y[i, j] = y

        for i in range(rows):
            for j in range(cols):
                gradient_magnitude[i, j , k] = np.clip(min(255, max(0, np.sqrt(gradient_x[i, j]**2 + gradient_y[i, j]**2))) , 0, 255)
    
    WriteImage(gradient_magnitude)
    return 
#--------------------------------------------------------------------------------#
def apply_laplacian_operator():
    
    image = cv2.imread(input_image_path)
    img = image.copy()
    laplacian_kernel = np.array([[0, 1, 0], 
                                 [1, -4, 1], 
                                 [0, 1, 0]])
    
    rows = img.shape[0]
    cols = img.shape[1]
    gradient_magnitude = np.zeros((rows, cols, img.shape[2]), dtype=np.float32)
    
    for k in range(img.shape[2]):
        for i in range(1, rows-1):
            for j in range(1, cols-1):
                laplacian_value = (laplacian_kernel[0, 0] * img[i-1, j-1, k] + 
                                   laplacian_kernel[0, 1] * img[i-1, j, k] + 
                                   laplacian_kernel[0, 2] * img[i-1, j+1, k] +
                                   laplacian_kernel[1, 0] * img[i, j-1, k] + 
                                   laplacian_kernel[1, 1] * img[i, j, k] + 
                                   laplacian_kernel[1, 2] * img[i, j+1, k] +
                                   laplacian_kernel[2, 0] * img[i+1, j-1, k] + 
                                   laplacian_kernel[2, 1] * img[i+1, j, k] + 
                                   laplacian_kernel[2, 2] * img[i+1, j+1, k])

                gradient_magnitude[i, j, k] = np.clip(laplacian_value, 0, 255)
    
    WriteImage(gradient_magnitude)
    return 
#--------------------------------------------------------------------------------#
def apply_impulse_noise(salt_prob, pepper_prob):
    image = cv2.imread(input_image_path)    
    noisy_image = np.copy(image)
    
    rows, cols, channels = noisy_image.shape
    
    for k in range(channels):
        for i in range(rows):
            for j in range(cols):
                rand_val = random.random()
                if rand_val < salt_prob:
                    noisy_image[i, j , k] = 225
                elif rand_val < salt_prob + pepper_prob:
                    noisy_image[i, j , k] = 0
    
    WriteImage(noisy_image)
    return 
#--------------------------------------------------------------------------------#
def histogram_specification():
    
    input_image = cv2.imread(input_image_path, cv2.IMREAD_COLOR)
    reference_image = cv2.imread(reference_image_path, cv2.IMREAD_COLOR)
    specified_image = np.zeros_like(input_image)

    for channel in range(input_image.shape[2]):
        input_histogram = calculate_histogram(input_image[:, :, channel])
        reference_histogram = calculate_histogram(reference_image[:, :, channel])

        input_cdf = calculate_cdf(input_histogram)
        reference_cdf = calculate_cdf(reference_histogram)

        total_pixels_input = input_image.shape[0] * input_image.shape[1]
        total_pixels_reference = reference_image.shape[0] * reference_image.shape[1]

        input_cdf_normalized = [cdf_val / total_pixels_input for cdf_val in input_cdf]
        reference_cdf_normalized = [cdf_val / total_pixels_reference for cdf_val in reference_cdf]

        mapping = np.zeros(256, dtype=np.uint8)
        ref_index = 0
        for input_index in range(256):
            while ref_index < 255 and reference_cdf_normalized[ref_index] < input_cdf_normalized[input_index]:
                ref_index += 1
            mapping[input_index] = ref_index

        for i in range(input_image.shape[0]):
            for j in range(input_image.shape[1]):
                specified_image[i, j, channel] = mapping[input_image[i, j, channel]]
    
    WriteImage(specified_image)
    return 

#--------------------------------------------------------------------------------#

def add_images():
    image1 = cv2.imread(input_image_path)
    image2 = cv2.imread(output_image_path)
    height, width, channels = image1.shape
    result_image = np.zeros((height, width, channels), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            for c in range(channels):
                pixel_value = int(image1[i, j, c]) + int(image2[i, j, c])
                result_image[i, j, c] = min(255, pixel_value)

    WriteImage(result_image)
    return 
#--------------------------------------------------------------------------------#
def fourier():
    def dft_2d(image):
        return np.fft.fft2(image)

    def shift_frequency(F):
        return np.fft.fftshift(F)

    def save_spectrum(F):
        magnitude_spectrum = np.log(np.abs(F) + 1)
        magnitude_spectrum_normalized = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX)
        WriteImage(magnitude_spectrum_normalized)

    def main(image_path):
        ini = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        up_width = 350
        up_height = 350
        up_points = (up_width, up_height)
        image = cv2.resize(ini, up_points, interpolation=cv2.INTER_LINEAR)
        F = dft_2d(image)
        shifted_F = shift_frequency(F)
        save_spectrum(shifted_F)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_image_path = os.path.join(script_dir, 'original.jpg')
    main(input_image_path)