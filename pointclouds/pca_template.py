#!/usr/bin/env python
import utils
import numpy
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
###YOUR IMPORTS HERE###
import numpy as np
###YOUR IMPORTS HERE###


def main():

    #Import the cloud
    pc = utils.load_pc('cloud_pca.csv')

    ###YOUR CODE HERE###
    # Show the input point cloud
    fig = utils.view_pc([pc])

    #Rotate the points to align with the XY plane
    print ( np.array(pc).shape ) # (200,3,1)
    X = utils.convert_pc_to_matrix(pc)
    # X = np.squeeze(X)
    print ( "X",X.shape ) # (3,200)
    miu = np.mean(X,axis=1)
    print ( "miu",miu.shape ) # (3,)
    X = X - miu
    print ( np.sum( np.mean(X,axis=1) ) )
    # n = X.shape[1]
    # Q = (X@X.T) / (n-1)
    # Qnp = np.cov(X)
    # print ( "Qdiff", np.linalg.norm( Q-Qnp ) )
    Q = np.cov(X)
    print ( "Q" , Q.shape )
    U, S, Vh = np.linalg.svd(Q)
    X_new = Vh.T @ X
    print ( Vh.shape )
    print ( "Vh.T=", np.round(Vh.T,3))

    #Show the resulting point cloud
    pc_a = utils.convert_matrix_to_pc(X_new)
    fig = utils.view_pc([pc_a] , fig, color='r')


    #Rotate the points to align with the XY plane AND eliminate the noise
    fig1 = utils.view_pc([pc_a], color='r')
    s = np.diag(S**2)
    print ( "s=diag(S2)=", s.shape)
    VhT = Vh.T
    threshold = 1e-3
    idx_to_remove = []
    idx_keep = []
    for i in range ( s.shape[0] ):
        if ( s[i,i] < threshold ):
            idx_to_remove.append(i)
        else:
            idx_keep.append(i)
    # Vs = Vh[:,idx_keep]
    Vs = Vh
    Vs[:,idx_to_remove] = np.zeros_like(Vs[:,idx_to_remove])
    print ( "Vs.T", np.round(Vs.T,3) )
    X_b = Vs.T @ X
    pc_b = utils.convert_matrix_to_pc( X_b )
    fig1 = utils.view_pc([pc_b], fig1, color='g')

    # Show the resulting point cloud

    ###YOUR CODE HERE###
    fig2 = utils.view_pc([pc])
    normalU = np.expand_dims(U[:,-1],axis=1)
    print ( normalU.shape )
    print ( miu.shape )
    print ( normalU )
    fig2 = utils.draw_plane(fig2,normalU,miu, color=(0,1,0,0.3))

    plt.show()
    #input("Press enter to end:")


if __name__ == '__main__':
    main()
