import matplotlib.pyplot as plt
import numpy as np

# First group of GPAs
gpas_group_1 = [
    3.9, 3.9, 3.6, 3.3, 3.2, 2.7, 3.4, 3.1, 2.7, 1.9,
    3.2, 3.9, 2.6, 3.7, 2.6, 3.7, 3.2, 3.7, 3.1, 3.5,
    3.5, 3.9, 3.7, 2.9, 3.8, 3.2, 3.4, 3.4, 2.7, 2.8,
    3.5, 2.8, 3.1, 3.3, 3.8, 3.3, 1.8, 3.2, 3.7, 2.8, 3,
    4, 3.3, 2.5, 3.1, 2.8, 3.7, 3.7, 3.5, 3.3, 2.8,
    3.5, 2.6, 3.2, 4, 2.8, 3.2, 3.8, 3.7, 2.5, 2.9,
    3.7, 3.9, 1.7, 4, 2.5, 3.4, 3, 3.9, 3.6, 2.7, 3.4,
    2.7, 3.3, 2.7, 3.6, 3.7, 2.9, 1.8, 3.9, 3.9, 4,
    1.9, 3.2, 4, 3.5, 3, 3.8, 3, 2.7, 3.6, 3.6, 3.3, 4
]

# Second group of GPAs
gpas_group_2 = [
    4.0, 3.3, 2.5, 3.2, 2.5, 2, 3.2, 1.9, 2.6, 1.9,
    3, 2.8, 2.5, 2.5, 3.1, 2.2, 2.1, 3.1, 3.1, 2.4,
    3.2, 2.8, 3.8, 3.4, 3.1, 3, 2.1, 2.2, 3.2, 2.3,
    2.9, 3.4, 3.8, 2.8, 2.6, 2.5, 2.1, 2.4, 3.4, 2.6,
    2.8, 3.1, 2.6, 2.5, 2.7, 2.5, 3, 2.4, 3, 1.6, 2.4,
    2.8
]

# Calculate frequency of each GPA for both groups
def calculate_frequency(gpa_list):
    unique_gpas = list(set(gpa_list))
    frequency = [gpa_list.count(gpa) for gpa in unique_gpas]
    return unique_gpas, frequency

unique_gpas_group_1, frequency_group_1 = calculate_frequency(gpas_group_1)
unique_gpas_group_2, frequency_group_2 = calculate_frequency(gpas_group_2)

# Scatter plot
plt.figure(figsize=(8, 6))

# Plotting first group in blue color
plt.scatter(unique_gpas_group_1, frequency_group_1, color='blue', label='Tech based note-taking', alpha=0.7)

# Given slope and intercept
slope = 2.618445263
intercept = -2.713776451

# Print the regression formula
print(f"The regression formula is: y = {slope}x + {intercept}")

# Create a new array of x-values from 0 to the maximum GPA
x_values = np.linspace(0, max(unique_gpas_group_1), num=100)

# Calculate the corresponding y-values
y_values = slope * x_values + intercept

# Plot the regression line
plt.plot(x_values, y_values, color='black', label='Regression line')

# Set the limits of the x-axis
plt.xlim(0, max(unique_gpas_group_1))

plt.title('Scatter Plot of GPA Frequency')
plt.xlabel('GPA')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()