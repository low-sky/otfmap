import gridFunctions
import numpy as np
cimport numpy as np
cimport cython 

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t
@cython.boundscheck(False)
def gridData(int naxis1, int naxis2, int naxis3, \
             np.ndarray[DTYPE_t,ndim=1] xdata, \
             np.ndarray[DTYPE_t,ndim=1] ydata, \
             np.ndarray[DTYPE_t,ndim=2] spectra):

    cdef float pixPerBeam = 3.0
    cdef int nSpec = spectra.shape[0]
    cdef np.ndarray[DTYPE_t,ndim=3] outData = \
        np.zeros([naxis1, naxis2,naxis3])
    cdef np.ndarray[DTYPE_t,ndim=3] outWeight = \
        np.zeros([naxis1, naxis2])
    for xpix in range(naxis1):
        for ypix in range(naxis2):
            for specIdx in range(nSpec):
                weight = gridFunctions.sincGridC(xpix,ypix,xdata[specIdx],\
                                                 ydata[specIdx],pixPerBeam)
                if weight != 0:
                    outData[xdata[specIdx],\
                            ydata[specIdx],:] = weight*spectra[specIdx,:]
                    outWeight[xdata[specIdx],ydata[specIdx]] += weight
    return outData,outWeight
