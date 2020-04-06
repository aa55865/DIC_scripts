import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

angle = 0
specimen = 8

file = 'C:\\Users\\aa55865\\Desktop\\lattice_strut_study\\final_strut_samples\\5mm_specimens\\{}deg\\specimen{}\\stress-strain_data.csv'.format(angle,specimen)

df = pd.read_csv(file, names=['strain','stress']) #read in csv files from excel
df = df.dropna()
df.plot(kind='scatter',x='strain',y='stress',color='red') #plot curve and pick points to use for interpolation
plt.show()
first_point = int(input('first point: '))-1 #select points from beginning of stress-strain curve between which to interpolate
second_point = int(input('second point: '))-1
strain = df['strain'].tolist() #extract stress-strain values as two lists
stress = df['stress'].tolist()

x1 = strain[first_point]
x2 = strain[second_point]
y1 = stress[first_point]
y2 = stress[second_point]

strain = strain[first_point:] #remove points before selected interpolation points from stress/strain data sets
stress = stress[first_point:]

slope = (y2-y1)/(x2-x1) #calculate coefficients for line that intersects linear region of original stress-strain curve
intercept = y2-slope*x1
x_intercept = -intercept/slope

strain = [value-x_intercept for value in strain] #shift strain values by x-intercept of the line calculated above
point1 = [0,0]
point2 = [strain[0],stress[0]]
x_values = list(np.linspace(0,strain[0],100))
interpolated_slope = point2[1]/point2[0]
y_values = [interpolated_slope*value for value in x_values] #generate line of points to connect origin to original data
adjusted_strain = x_values+strain
adjusted_stress = y_values+stress
plt.figure()
plt.plot(adjusted_strain,adjusted_stress,'bo')
plt.title('Stress-Strain: {} deg specimen {}'.format(angle, specimen))
plt.xlabel('Strain [pxl/pxl]')
plt.ylabel('Stress [MPa]')
plt.savefig('C:\\Users\\aa55865\\Desktop\\lattice_strut_study\\final_strut_samples\\5mm_specimens\\{}deg\\specimen{}\\stress-strain_curve_adjusted.png'.format(angle,specimen))
plt.show()

with open('C:\\Users\\aa55865\\Desktop\\lattice_strut_study\\final_strut_samples\\5mm_specimens\\{}deg\\specimen{}\\stress-strain_data_adjusted.csv'.format(angle,specimen),'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(adjusted_strain, adjusted_stress))
