def DICer(**kwargs):

	if 'subset' in kwargs.keys(): subset = 'subset_{}'.format(kwargs['subset']) #specify subset you want to analyze based on ID in paraview
	if 'frames' in kwargs.keys(): frames = kwargs['frames'] #this is based on the number of solution text files in the dice_working_dir
	if 'data' in kwargs.keys(): data = kwargs['data'] #specify what data you want plotted
	if 'scale' in kwargs.keys(): scale = kwargs['scale'] #scaling factor in [in/pxl], used for plotting displacements

	import matplotlib.pyplot as plt

	fileList = []
	file_indices=[]
	for number in range(frames):
		index = '0'*len(str(frames)) + str(number)
		index = index[-4:]
		file_indices.append(index)

	for index in file_indices: #import DICe solution files (file_00 --> file_n) into list where each list item is a list of lines in each file
		file = open('DICe_solution_{}.txt'.format(index))
		file = file.readlines()
		fileList.append(file)


	for file in fileList: 
		file.remove(file[0]) #remove first row of headers from each file
		subsets = len(fileList[0]) 
		for line in range(0,subsets): 
			file[line] = file[line].split(',') #split file lines by comma to separate data values
				
			
	dataDict = {} #organize DICe data into dictionary by subset, then store data for each frame (xx_strain, yy_strain, etc.) under each subset
	for file in fileList: 
		for line in file:
			dataDict['subset_{}'.format(line[0])] = {}
	frameCount = 0
	frameVals = []
	for file in fileList: 
		frameVals.append(frameCount)
		for line in file:
			dataDict['subset_{}'.format(line[0])].update({'frame_{}'.format(frameCount): {'x_coordinate':float(line[1]),'y_coordinate':float(line[2]),'x_displacement':float(line[3]),'y_displacement':float(line[4]),'sigma':float(line[5]),'gamma':float(line[6]),'beta':float(line[7]),'status_flag':float(line[8]),'uncertainty':float(line[9]),'xx_strain':float(line[10]),'yy_strain':float(line[11]),'xy_strain':float(line[12])}})
		frameCount+=1

	def ListMult(multiplier,numlist): #multiply a list of numbers by a float
		newlist = [multiplier*i for i in numlist]
		return newlist

	dataVals = [] #plot results
	for frame in dataDict[subset]:
		dataVals.append(dataDict[subset][frame][data])
	if data=='y_displacement' or data =='x_displacement':
		dataVals = ListMult(scale, dataVals)
	plt.plot(frameVals,dataVals,'ro')
	plt.xlabel('frame number')
	if data=='y_displacement' or data=='x_displacement':
		plt.ylabel('{} {}'.format(data,'[in]'))
	else:
		plt.ylabel(data)
	plt.title('{}: {}'.format(subset,data))
	return plt.show()

DICer(frames=1178,subset=329,data='x_displacement',scale=(0.053/32))


# DISPLACEMENT_X          // u
# DISPLACEMENT_Y          // v
# ROTATION_Z              // (theta) rotation about the z-axis, z is out of the plane
# NORMAL_STRAIN_X         // normal stretch in the x direction (of the subset shape function)
# NORMAL_STRAIN_Y         // normal stretch in the y direction (of the subset shape function)
# SHEAR_STRAIN_XY         // shear strain in the x-y plane (of the subset shape function)
# COORDINATE_X            // x position in image space
# COORDINATE_Y            // y position in image space
# MODEL_COORDINATES_X     // model x position in physical space (for stereo only)
# MODEL_COORDINATES_Y     // model x position in physical space (for stereo only)
# MODEL_COORDINATES_Z     // model x position in physical space (for stereo only)
# SIGMA                   // predicted std. dev. of the displacement solution given std. dev. of image
#                         // noise and interpolation bias, smaller sigma is better
# GAMMA                   // template match quality (value of the cost function),
#                         // smaller gamma is better, 0.0 is perfect match
# BETA                    // sensitivity of the cost function to small perturbations in the displacement solution
# NOISE_LEVEL             // estimated std. dev. of the image noise
# CONSTRAST_LEVEL         // std. dev. of the subset image intensity values
# ACTIVE_PIXELS           // number of pixels that are active (not obstructed or deactivated for this step)
# MATCH                   // 0 means match was found -1 means match failed
# ITERATIONS              // number of iterations taken by the solution algorithm
# STATUS_FLAG             // information about the initialization method or error flags on failed steps
# NEIGHBOR_ID             // the global id of the neighboring subset to use for initialization by neighbor value
# CONDITION_NUMBER        // quality metric for the psuedoinverse matrix in the gradient-based method

# ADDITIONAL NOTES:
#
# SIGMA estimates the predicted variation in the displacement solution given variations in the data
# 	due to noise and interpolation bias. SIGMA can be used as an uncertainty metric if the following 
#	conditions are met: the displacements are smaller than one pixel in magnitude and the noise level 
# 	in the images is less than roughly three or four percent. Use SIGMA to determine the confidence 
#	in the computed solution. For SIGMA lower values are better and imply lower uncertainty.
#
# GAMMA measures how well the template or subset from the reference image matches the deformed image. 
#	GAMMA is the value of the correlation criteria (or objective functional or cost function magnitude). 
#	GAMMA provides the user with a way to tell if the subset is still registering on the correct location 
#	in the deformed image. For GAMMA lower values are better, 0.0 implies an identical or perfect match 
#	between the reference and deformed subset.
#
# BETA provides a measure of how sensitive the cost function (or correlation criteria) is to small 
#	perturbations in the displacement solution. If the cost function is highly sensitive, it will increase 
#	dramatically for even slight errors in the displacement solution. If the cost function is not sensitive, 
#	it implies that it cannot differentiate between many potential solutions. Again, for BETA lower values 
#	are better. Common sources of high BETA are poor contrast, lack of randomness in the speckle pattern, 
#	subset sizes too small, or high image noise levels.