import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy

img = plt.imread('a.jpg')
# print(img.shape)
width = img.shape[0]
height = img.shape[1]

img = img.reshape(width * height, 3)
# print(img.shape)

kmeans =  KMeans(n_clusters= 4).fit(img)
labels = kmeans.predict(img)
clusters = kmeans.cluster_centers_
# method 1
# img2 = numpy.zeros_like(img)
# # print(img2)

# for i in range(len(img2)):
#     img2[i] = clusters[labels[i]]


#method 2: create new a new normal picture with the size of width and height 
img2 = numpy.zeros((width,height, 3), dtype=numpy.uint8)

#width = 656, height = 561
index = 0
for i in range(width):
    for j in range(height):
        label_of_pixel = labels[index]
        img2[i][j] = clusters[label_of_pixel]
        index += 1

# img2 = img2.reshape(height, width, 3)
# turn off frame
fig = plt.figure(frameon = False)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)

plt.imshow(img2)
plt.show()
#clusters
# [[ 48.39373676  57.07017857  27.67476583] 
#  [204.08423842 209.41929469 209.62171225] 
#  [116.98548772 129.66317674  48.47625464] 
#  [ 87.765104   119.55806418 170.17463677]]




