#----------------------imports---------------------------#
import os
import cv2
import numpy as np
#--------------------------------------------------------#
#--------------------------------------------------------------------------------#   
# Get the current script directory
script_dir = os.path.dirname(os.path.realpath(__file__))
# Define the paths to the input and output images
input_image_path = os.path.join(script_dir, 'original.jpg')
output_image_path = os.path.join(script_dir, 'manipulatedImage.jpg')

image = cv2.imread(input_image_path, cv2.IMREAD_COLOR)

def WriteImage(Edited_image):
    cv2.imwrite(output_image_path, Edited_image)
    return 

#--------------------------------------------------------#

def Median(Kernel):
    image = cv2.imread(input_image_path, cv2.IMREAD_COLOR)
    img = image.copy()
    pad_size = Kernel // 2
    padded_img = np.pad(img, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), 'constant', constant_values=0)
    for channel in range(image.shape[2]):
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                temp = []
                for a in range(Kernel):
                    for b in range(Kernel):
                        temp.append(padded_img[i+a][j+b][channel])
                temp.sort()
                img[i][j][channel] = temp[int(len(temp)/2)]
    
    WriteImage(img)
    return
    

#--------------------------------------------------------------------------------#    

def Averaging(Kernel):
    image = cv2.imread(input_image_path, cv2.IMREAD_COLOR)
    img = image.copy()
    pad_size = Kernel // 2
    padded_img = np.pad(img, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), 'constant', constant_values=0)
    for channel in range(image.shape[2]):
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                temp = []
                for a in range(Kernel):
                    for b in range(Kernel):
                        temp.append(padded_img[i+a][j+b][channel])
                temp.sort()
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
    img = image.copy()
    s_max = 12
    window_size = passed_window_size
    filtered_image = np.zeros(img.shape, dtype="uint8")
    for channel in range(img.shape[2]):
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
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
                    a2 = np.array(median - temp[-1])
                    if a1 > 0 and a2 < 0:
                        b1 = img[i, j, channel] - temp[0]
                        b2 = img[i, j, channel] - temp[-1]
                        if b1 > 0 and b2 < 0:
                            filtered_image[i, j, channel] = img[i, j, channel]
                        else:
                            filtered_image[i, j, channel] = median
                        break
                    else:
                        if window_size < 7:
                            window_size += 2
                        else:
                            filtered_image[i, j, channel] = median
                            break
                window_size = passed_window_size
    WriteImage(filtered_image)
    return  
    
    
    # Read the input image
    
    
#--------------------------------------------------------------------------------# 

