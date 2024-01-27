from sklearn.cluster import KMeans
from sklearn.neighbors import KernelDensity
from scipy.spatial import distance
from scipy.stats import norm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import json


def Compare(df_train= pd.DataFrame(),df_test= pd.DataFrame(), x_label='x',y_label='x'):
    # Extract x_train and y_train from df_train
    x_train = df_train[x_label].values
    y_train = df_train[y_label].values

    # Combine x_train and y_train into a 2D array
    data_train = np.column_stack((x_train, y_train))
    

    # Use KMeans to find the cluster center
    kmeans = KMeans(n_clusters=1).fit(data_train)

    # The cluster center is stored in the cluster_centers_ attribute
    center_x, center_y = kmeans.cluster_centers_[0]

    print(f"Cluster center is at ({center_x:.5f}, {center_y:.5f})")

    # Fit a Kernel Density Estimation model
    # kde = KernelDensity(kernel='gaussian').fit(data_train)
    kde = KernelDensity(kernel='epanechnikov').fit(data_train)
    # kde = KernelDensity(kernel='exponential').fit(data_train)
    # kde = KernelDensity(kernel='linear').fit(data_train)

    data_whole = np.column_stack((np.linspace(35, 90, 1024),np.linspace(0, 20, 1024)))  
    # Calculate the log probability density for each point in the training set
    log_prob_density = kde.score_samples(data_whole)
    # Convert the log probability density to the original probability density
    prob_density = np.exp(log_prob_density)
    max_prob_density = np.max( prob_density)

    # Extract x_test and y_test from df_test
    x_test = df_test[x_label].values
    y_test = df_test[y_label].values
    
    data_test = np.column_stack((x_test, y_test))
    data_whole = np.column_stack((np.linspace(35, 90, 1024),np.linspace(0, 20, 1024)))    
    # Calculate the log probability density for each point in the training set
    log_whole_prob_density = kde.score_samples(data_whole)
    # Convert the log probability density to the original probability density
    prob_density = np.exp(log_whole_prob_density)
    test_densities = kde.score_samples(data_test)                    
    test_probabilities = np.exp(test_densities)
    
    max_prob_density = max(np.max(prob_density),np.max(test_probabilities))
    test_probabilities /=  max_prob_density 

    for i, prob in enumerate(test_probabilities):
        print(f"Probability for test point {i+1} ({x_test[i]}, {y_test[i]}) is: {prob:.3f}")

    
    return(test_probabilities)


# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)

# 获取当前文件的目录
current_directory = os.path.dirname(current_file_path)
# 改变当前工作目录
os.chdir(current_directory)


# 创建一个宽高比为2:1的figure
fig = plt.figure(figsize=(10, 5))     
ax = fig.add_subplot(1, 1, 1)
# 设置axes的宽高比为3:2
ax.set_aspect(3/2)

n = 9

with open('tas_cord.json') as file:
    cord = json.load(file)
# 绘制TAS图解边界线条
# Draw TAS diagram boundary lines
for line in cord['coords'].values():
    x_coords = [point[0] for point in line]
    y_coords = [point[1] for point in line]
    ax.plot(x_coords, y_coords, color='black', linewidth=0.3)
    

# 在TAS图解中添加岩石种类标签
# Add rock type labels in TAS diagram
# for label, coords in cord['coords'].items():
#     x_coords = [point[0] for point in coords]
#     y_coords = [point[1] for point in coords]
#     x_center = sum(x_coords) / len(x_coords)
#     y_center = sum(y_coords) / len(y_coords)
#     ax.text(x_center, y_center, label, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.3), fontsize=9)



df_train = pd.read_pickle('df_Mugearite.pkl')
df_train['SIO2_wt_calibred']
df_train['ALL_Alkaline_wt_calibred']
# print(df_train)

# Generate testing data
x_test = np.array([45.76428218, 31.81390091, 55.28563359, 60.96200656, 70.43711105,
       40.88503457])
y_test = np.array([13.76185634, 10.33199649, 8.79003757, 14.88086825, 9.92049699,
       2.49193062])

x_test = np.linspace(35, 80, n)
y_test = np.linspace(2, 16, n)

# x_test_mesh, y_test_mesh = np.meshgrid(x_test, y_test)
# test_points = np.c_[x_test_mesh.ravel(), y_test_mesh.ravel()]
# df_test = pd.DataFrame(test_points, columns=['SIO2_wt_calibred', 'ALL_Alkaline_wt_calibred'])
df_test = pd.DataFrame({'SIO2_wt_calibred': x_test, 'ALL_Alkaline_wt_calibred': y_test})


# Call the Compare function
target_probabilities = Compare(df_train, df_test,'SIO2_wt_calibred', 'ALL_Alkaline_wt_calibred')

# Plot Mugearite Training Data in blue
ax.scatter(df_train['SIO2_wt_calibred'], df_train['ALL_Alkaline_wt_calibred'], color='blue', label='Mugearite Training Data',edgecolors= None,alpha=0.1)


# Plot testing data in red
ax.scatter(df_test['SIO2_wt_calibred'], df_test['ALL_Alkaline_wt_calibred'], color='red', label='Testing data',edgecolors= None,alpha=0.3)

# Add probability labels to the test points
for i, (x, y) in enumerate(zip(df_test['SIO2_wt_calibred'], df_test['ALL_Alkaline_wt_calibred'],)):
    plt.text(x, y, f"{target_probabilities[i]:.2f}", ha='right')


ax.set_xlabel(r"$SiO2$", fontsize=9)
ax.set_ylabel(r"$Na2O+K2O$", fontsize=9)
ax.set_title(r"Extended TAS Diagram", fontsize=9)
ax.set_xlim(35,80)
ax.set_ylim(0,17.647826086956513)  

ax.tick_params(axis='both', labelsize=9)
# legend = ax.legend(loc='upper left', fontsize=4, bbox_to_anchor=(1, 1))

# Add a legend
plt.legend()

# Show the plot
plt.show()