## 1

c. 

Configuration for  0  is:  [[ 0.441 -0.245 -0.145 -0.656 -0.03  -0.362  0.   ]]	

<img src="implementation.assets/Screenshot from 2021-11-08 17-04-16.png" alt="Screenshot from 2021-11-08 17-04-16" style="zoom: 50%;" />

Configuration for  1  is:  [[-0.     1.058 -0.    -1.834  0.    -1.318  0.   ]]

<img src="implementation.assets/Screenshot from 2021-11-08 17-04-59.png" alt="Screenshot from 2021-11-08 17-04-59" style="zoom:50%;" />



Configuration for  2  is:  [[-0.229  0.301  0.131 -2.045  0.051 -1.135 -0.   ]]

<img src="implementation.assets/Screenshot from 2021-11-08 17-08-40.png" alt="Screenshot from 2021-11-08 17-08-40" style="zoom:50%;" />



Configuration for  3  is:  [[ 1.7    0.903 -0.771 -0.336 -0.359 -0.381  0.   ]]

<img src="implementation.assets/Screenshot from 2021-11-08 17-09-30.png" alt="Screenshot from 2021-11-08 17-09-30" style="zoom:50%;" />

Configuration for  4  is:  [[ 1.712 -0.023 -0.607 -0.552 -0.237 -0.292  0.   ]]

<img src="implementation.assets/Screenshot from 2021-11-08 17-08-12.png" alt="Screenshot from 2021-11-08 17-08-12" style="zoom:50%;" />

d.

Configuration for  0  is:  [[ 0.246 -0.3   -0.556 -0.711 -0.029 -0.261  0.   ]]

<img src="implementation.assets/Screenshot from 2021-11-08 17-30-38.png" alt="Screenshot from 2021-11-08 17-30-38" style="zoom:50%;" />

Configuration for  1  is:  [[-0.276  1.038 -0.384 -1.832 -0.003 -1.257 -0.   ]]

<img src="implementation.assets/Screenshot from 2021-11-08 17-31-18.png" alt="Screenshot from 2021-11-08 17-31-18" style="zoom:50%;" />

Configuration for  2  is:  [[-0.56   0.333 -0.205 -2.048  0.072 -1.121 -0.   ]]

<img src="implementation.assets/Screenshot from 2021-11-08 17-32-15.png" alt="Screenshot from 2021-11-08 17-32-15" style="zoom:50%;" />

3, 4: Failed with  beta = 5e-2

With beta = 1e-2:

Configuration for  3  is:  [[ 1.711  0.916 -0.8   -0.487 -1.156 -0.    -0.   ]]

<img src="implementation.assets/Screenshot from 2021-11-08 17-36-15.png" alt="Screenshot from 2021-11-08 17-36-15" style="zoom:50%;" />

Configuration for  4  is:  [[ 1.683 -0.048 -0.71  -0.55  -0.237 -0.302  0.   ]]

<img src="implementation.assets/Screenshot from 2021-11-08 17-35-10.png" alt="Screenshot from 2021-11-08 17-35-10" style="zoom:50%;" />

## 2

a. 

V.T= [[-0.529 -0.003  0.848]
 [-0.058 -0.998 -0.039]
 [ 0.846 -0.07   0.528]]

<img src="implementation.assets/Screenshot from 2021-11-09 23-43-26.png" alt="Screenshot from 2021-11-09 23-43-26" style="zoom:50%;" />

b.

Vs.T [[-0.529 -0.058  0.846]
 [-0.003 -0.998 -0.07 ]
 [ 0.     0.     0.   ]]

(the last row is simply to keep the dimension for plot, can be removed in practice)

<img src="implementation.assets/Screenshot from 2021-11-09 23-43-30.png" alt="Screenshot from 2021-11-09 23-43-30" style="zoom:50%;" />

c.

<img src="implementation.assets/Screenshot from 2021-11-09 23-43-36.png" alt="Screenshot from 2021-11-09 23-43-36" style="zoom:50%;" />

3.

Plane: 0 =  0.733 *x +  -0.321 *y +  0.6 *z +  -0.343

<img src="implementation.assets/Screenshot from 2021-11-09 19-04-53.png" alt="Screenshot from 2021-11-09 19-04-53" style="zoom:50%;" />

4. 

   a. Plots for the Last iteration 

   <img src="implementation.assets/Screenshot from 2021-11-09 20-52-56.png" alt="Screenshot from 2021-11-09 20-52-56" style="zoom:50%;" />

   <img src="implementation.assets/Screenshot from 2021-11-09 20-53-02.png" alt="Screenshot from 2021-11-09 20-53-02" style="zoom:50%;" />

   b. Plot for error v.s. #outliers

   <img src="implementation.assets/Screenshot from 2021-11-09 21-11-57.png" alt="Screenshot from 2021-11-09 21-11-57" style="zoom: 33%;" />

   ​	Plot for time v.s. #outliers

   <img src="implementation.assets/Screenshot from 2021-11-09 21-12-05.png" alt="Screenshot from 2021-11-09 21-12-05" style="zoom: 33%;" />

   c. Discussion about the performance

   From the results above, we can observed that both methods can fit with a satisfying model. 

   In my case the time for the two algorithms are quite different. The time for RANSAC is far larger than that of PCA. In general, RANSAC needs at least one fit for the inliers, which cost the time similar to PCA. Moreover, the RANSAC method depends on the iteration set. In my case, the max iteration is set to 100. A smaller iteration can improve speed but reduce stability. 

   For the error, the PCA method has an increasing trend while the trend for RANSAC is not clear. This indicates that, when the amount of outliers is large, the RANSAC might give a better performance. However, the RANSAC is a random method and depends on the max iteration, it is not guaranteed to be better than PCA.   

   

5. 

   cloud_icp_target0

   <img src="implementation.assets/Screenshot from 2021-11-09 23-25-06.png" alt="Screenshot from 2021-11-09 23-25-06" style="zoom:50%;" />

   <img src="implementation.assets/Screenshot from 2021-11-09 23-25-12.png" alt="Screenshot from 2021-11-09 23-25-12" style="zoom: 33%;" />

   cloud_icp_target1

   <img src="implementation.assets/Screenshot from 2021-11-09 23-26-38.png" alt="Screenshot from 2021-11-09 23-26-38" style="zoom:50%;" />

   <img src="implementation.assets/Screenshot from 2021-11-09 23-26-42.png" alt="Screenshot from 2021-11-09 23-26-42" style="zoom:33%;" />

   cloud_icp_target2

   <img src="implementation.assets/Screenshot from 2021-11-09 23-28-17.png" alt="Screenshot from 2021-11-09 23-28-17" style="zoom:50%;" />

   <img src="implementation.assets/Screenshot from 2021-11-09 23-28-21.png" alt="Screenshot from 2021-11-09 23-28-21" style="zoom:33%;" />

   cloud_icp_target3

   <img src="implementation.assets/Screenshot from 2021-11-09 23-29-09.png" alt="Screenshot from 2021-11-09 23-29-09" style="zoom:50%;" />

   <img src="implementation.assets/Screenshot from 2021-11-09 23-29-13.png" alt="Screenshot from 2021-11-09 23-29-13" style="zoom:33%;" />

   Given the results, target 3 is more difficult to fit. One reason is that the target is a scaled version of the source, which isn't considered in our R, t transformation. The target 0 seems to be second difficult one and one probable reason is that the ICP method fails into a local minimum since the points are distributed in layers and we have fit the most layers except the uppermost and lowest ones. 