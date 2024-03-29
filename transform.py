from image import Image
import numpy as np

def brighten(image, factor):
   
   
    x_pixels, y_pixels, num_channels = image.array.shape 
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels) 

    new_im.array = image.array * factor

    return new_im

def adjust_contrast(image, factor, mid):
   
    x_pixels, y_pixels, num_channels = image.array.shape  #
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels) 
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = (image.array[x, y, c] - mid) * factor + mid

    return new_im

def blur(image, kernel_size):

    x_pixels, y_pixels, num_channels = image.array.shape  
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  
    neighbor_range = kernel_size // 2 
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
             
                total = 0
                for x_i in range(max(0,x-neighbor_range), min(new_im.x_pixels-1, x+neighbor_range)+1):
                    for y_i in range(max(0,y-neighbor_range), min(new_im.y_pixels-1, y+neighbor_range)+1):
                        total += image.array[x_i, y_i, c]
                new_im.array[x, y, c] = total / (kernel_size ** 2)
    return new_im

def apply_kernel(image, kernel):
  
  
    x_pixels, y_pixels, num_channels = image.array.shape  
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)  
    neighbor_range = kernel.shape[0] // 2  
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                total = 0
                for x_i in range(max(0,x-neighbor_range), min(new_im.x_pixels-1, x+neighbor_range)+1):
                    for y_i in range(max(0,y-neighbor_range), min(new_im.y_pixels-1, y+neighbor_range)+1):
                        x_k = x_i + neighbor_range - x
                        y_k = y_i + neighbor_range - y
                        kernel_val = kernel[x_k, y_k]
                        total += image.array[x_i, y_i, c] * kernel_val
                new_im.array[x, y, c] = total
    return new_im

def combine_images(image1, image2):

   
    x_pixels, y_pixels, num_channels = image1.array.shape  
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels) 
    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = (image1.array[x, y, c]**2 + image2.array[x, y, c]**2)**0.5
    return new_im
    
if __name__ == '__main__':
    lake = Image(filename='lake.png')
    city = Image(filename='city.png')


    sobel_x = apply_kernel(city, np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]))
    sobel_x.write_image('edge_x.png')
    sobel_y = apply_kernel(city, np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]))
    sobel_y.write_image('edge_y.png')

    # let's combine these and make an edge detector!
    sobel_xy = combine_images(sobel_x, sobel_y)
    sobel_xy.write_image('edge_xy.png')

