import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.patches as mpatches
from base64 import b64encode
from io import BytesIO
from js import document

def find_sign_change(coeff=1):
  """
  Finds the x-values corresponding to sign changes in a cosine function

  Parameters:
  coeff: Coefficient of cosine function

  Returns:
  important_x: Array of x-values corresponding to sign changes
  """
  unit = 1 / (2*coeff)
  important_x = [0]
  for i in range(0, 2*coeff):
    important_x.append(unit + 2*unit*i)
  important_x.append(2)
  return np.array(important_x)

def get_patches(coeffs=[1]):
  """
  Finds the coordinates and dimensions of regions where two cosine functions share the same sign

  Parameters:
  coeffs: Coefficients of two cosine functions

  Returns:
  patches: List of matplotlib patches
  """
  patches = []

  important_min_x = find_sign_change(min(coeffs))
  important_max_x = find_sign_change(max(coeffs))

  # Add patches where two cosine functions are both positive
  for i in range(0, len(important_min_x), 2):
    for j in range(0, len(important_max_x), 2):
      vert = [important_min_x[i], important_max_x[j]]
      width = important_min_x[i+1] - important_min_x[i]
      height = important_max_x[j+1] - important_max_x[j]
      rect = mpatches.Rectangle(vert, width, height, alpha=0.1, facecolor="blue")
      patches.append(rect)

  # Add patches where two cosine functions are both negative
  for i in range(1, len(important_min_x)-1, 2):
    for j in range(1, len(important_max_x)-1, 2):
      vert = [important_min_x[i], important_max_x[j]]
      width = important_min_x[i+1] - important_min_x[i]
      height = important_max_x[j+1] - important_max_x[j]
      rect = mpatches.Rectangle(vert, width, height, alpha=0.1, facecolor="blue")
      patches.append(rect)

  return patches

def yoverload(x_line, y_line, max_length=20):
    """
    Plots ratio of angles from two cosine functions on a torus in the y-direction

    Parameters:
    x_line, y_line: Set of cartesian coordinates of original linear function
    max_length: Maximum number of lines to plot, note some pairings of cosine functions may produce more than max_length lines

    Returns:
    x_line, y_line: Cartesian coordinates of plotted linear function on torus
    """
    # Initial check to see if number of lines in y_line is over max_length
    if len(y_line) > max_length:
      return x_line, y_line

    # We are concerned with the last element of the set y_line
    y = y_line[-1]

    # We need index where y first passes 2, as this is where y re-enters from the bottom of torus
    index = len(y)
    for i in range(len(y)):
      if y[i] > 2:
        index = i
        break

    # Loop through y-values and subtract 2 until all values are less than or equal to 2
    for i in range(math.ceil(1000/index)):
      # Split y on index so that last element in y contains only numbers greater than 2
      y = np.split(y, [index])

      # If y[-1] contains elements, we parse through and subtract 2
      # Then, we update the index
      if len(y[-1]) > 0:
        for j in range(len(y[-1])):
          y[-1][j] = y[-1][j] - 2
        for j in range(len(y[-1])):
          if y[-1][-1] <= 2:
            index += len(y[-1])
            break
          if y[-1][j] > 2:
            index += j
            break
        y = np.concatenate(y)

      # If y[-1] is empty, we break out of the loop
      # This means all y-values are less than 2
      else:
        break

    y = np.concatenate(y)

    # Replace last element of y_line with our new array of values in range [0, 2]
    y_line[-1] = y

    # If last element of new array is less than two, line re-enters on other side of torus
    # We account for re-entry on x-direction with xoverload() function
    if y[-1] < 2:
      return xoverload(x_line, y_line)

    # Return x_line and y_line with values adjusted for torus geometry
    return x_line, y_line

def xoverload(x_line, y_line):
    """
    Plots ratio of angles from two cosine functions on a torus in the x-direction

    Parameters:
    x_line, y_line: Set of cartesian coordinates of original linear function

    Returns:
    yoverload(x, y): Cartesian coordinates of plotted linear function on torus in x-direction, y-direction to be adjusted by yoverload()
    """

    # Get the input values
    num1 = int(document.getElementById("input1").value)
    num2 = int(document.getElementById("input2").value)
    coeffs = [num1, num2]

    # Calculate slope from coefficients
    slope = max(coeffs)/min(coeffs)

    # Point of re-entry on x-axis is (0, right_endpoint)
    right_endpoint =y_line[-1][-1]

    # Adjust y-values with intercept
    y_appendage = slope * np.linspace(0, 2, 1000) + right_endpoint

    # Append both x_line and y_line with new lines, now adjusted in x-direction
    x = np.append(x_line, [np.linspace(0, 2, 1000)], axis=0)
    y = np.append(y_line, [y_appendage], axis=0)

    # Pass to yoverload to adjust y-values so that they are in range [0, 2]
    return yoverload(x, y)

def generate_graph():
    # Clear the previous graph
    graph_div = document.getElementById("lineplot")
    graph_div.innerHTML = ""  # This clears the existing plot

    # Get the input values
    num1 = int(document.getElementById("input1").value)
    num2 = int(document.getElementById("input2").value)
    coeffs = [num1, num2]

    # Calculate slope from coefficients
    slope = max(coeffs)/min(coeffs)

    # Define original set of linear lines
    # Original set should contain only one line
    x_0 = np.array([np.linspace(0, 2, 1000)])
    y_0 = np.array([slope * np.linspace(0, 2, 1000)])

    x, y = yoverload(x_0, y_0, 20)
    patches = get_patches()
    fig = plt.figure()
    for i in range(len(y)):
      plt.scatter(x[i], y[i], s=1, color='blue')
    for patch in patches:
      plt.gca().add_patch(patch)
    plt.xlim(0, 2)
    plt.ylim(0, 2)
    plt.xlabel('Radians')
    plt.ylabel('Radians')
    plt.title('Ratio of Cosine Angles on Torus')
    plt.grid()
    
    # Save the plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Encode the image to base64
    img_str = b64encode(buf.read()).decode('utf-8')
    
    # Insert the image into the HTML
    img_tag = f'<img src="data:image/png;base64,{img_str}"/>'
    graph_div.innerHTML = img_tag