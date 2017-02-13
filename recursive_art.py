""" Generates "random" artwork using sine, cosine, sigmoid, products, averaging,
squaring, and cubing functions. """

import random
import math
from PIL import Image


functions = ['prod', 'sigmoid', 'squared', 'cubed', 'avg', 'cos_pi', 'sin_pi']
function_count = len(functions)

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    # Hit bottom node
    if max_depth < 2:
        # Randomly pick x or y
        return 'x' if random.random() > 0.5 else 'y'

    # Generate new functions
    f = functions[random.randrange(0,function_count,1)]
    # Pick a random maximum depth
    max_depth_1 = min_depth + math.ceil(random.random() * (max_depth - min_depth)) - 1
    # print('min_depth =',min_depth,'r =',r,'max_depth_1 =',max_depth_1)
    if f == 'sin_pi' or f == 'cos_pi' or f == 'sigmoid':
        return [f, build_random_function(min_depth-1, max_depth_1)]
    # Pick second random maximum depth
    max_depth_2 = min_depth + math.ceil(random.random() * (max_depth - min_depth)) - 1
    # print('Min depth:',min_depth,'New max depths:', max_depth_1, max_depth_2)
    return [f, build_random_function(min_depth-1, max_depth_2), build_random_function(min_depth-1, max_depth_2)]


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    # print("f[0] ==",f[0])
    if f[0] == 'prod':
        # print("Evaluating product of",f[1],'and',f[2])
        return evaluate_random_function(f[1],x,y) * evaluate_random_function(f[2],x,y)
    if f[0] == 'sigmoid':
        # print("Evaluating sigmoid of",f[1])
        return 1/(1+math.exp(-evaluate_random_function(f[1],x,y)))
    if f[0] == 'squared':
        # print("Evaluating",f[1],'squared')
        return math.pow(evaluate_random_function(f[1],x,y),2)
    if f[0] == 'cubed':
        # print("Evaluating",f[1],'cubed')
        return math.pow(evaluate_random_function(f[1],x,y),3)
    if f[0] == 'avg':
        # print("Evaluating average of",f[1],'and',f[2])
        return (evaluate_random_function(f[1],x,y) + evaluate_random_function(f[2],x,y)) / 2
    if f[0] == 'cos_pi':
        # print("Evaluating cosine of",f[1])
        return math.cos(evaluate_random_function(f[1],x,y)*math.pi)
    if f[0] == 'sin_pi':
        # print("Evaluating sine of",f[1])
        return math.sin(evaluate_random_function(f[1],x,y)*math.pi)
    if f[0] == 'x':
        # print("Returning x")
        return x
    if f[0] == 'y':
        # print("Returning y")
        return y
    # A constant
    # print("Returning",f[0])
    return f[0]



def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    # Calculate values needed for normalizing
    in_range = input_interval_end - input_interval_start
    in_med = in_range / 2 + input_interval_start
    out_range = output_interval_end - output_interval_start
    out_med = out_range / 2 + output_interval_start
    scalar = in_range / out_range
    # Center our value about zero
    val -= in_med
    # Scale it down to our new range
    val /= scalar
    # Shift it back to have the correct midpoint
    val += out_med

    return val


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    #doctest.run_docstring_examples(remap_interval, globals())
    # doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png")
    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
