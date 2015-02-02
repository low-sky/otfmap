import astropy
import numpy as np
import scipy
import astropy.wcs as wcs
import pdb
import astropy.io.fits as fits
import pyximport; pyximport.install()
import gridFunctions, gridData

def otfgrid(inFile, beamSize = 0.0087, pixPerBeam = 3.0,
            buffer = 1.1, wcsObject = None):

    hdu = fits.open(inFile)
    data = hdu[1].data
    longitude = data['CRVAL2']
    latitude = data['CRVAL3']
    minLon = longitude.min()
    maxLon = longitude.max()
    minLat = latitude.min()
    maxLat = latitude.max()

    naxis3 = len(data[0]['DATA'])
    crpix3 = data[0]['CRPIX1']
    crval3 = data[0]['CRVAL1']
    ctype3 = data[0]['CTYPE1']
    cdelt3 = data[0]['CDELT1']

    naxis2 = np.ceil((maxLat-minLat)/(beamSize/pixPerBeam)+2*pixPerBeam)
    crpix2 = naxis2/2
    cdelt2 = beamSize/pixPerBeam
    crval2 = (maxLat+minLat)/2
    ctype2 = data[0]['CTYPE3']+'--TAN'
# The projections need better definition

    cdelt1 = beamSize/pixPerBeam
    naxis1 = np.ceil((maxLon-minLon)/(beamSize/pixPerBeam)*\
                     np.cos(crval2/180*np.pi)+2*pixPerBeam)
    crpix1 = naxis1/2
    crval1 = (minLon+maxLon)/2
    ctype1 = data[0]['CTYPE2']+'---TAN'
    w = wcs.WCS(naxis=3)
    w.wcs.crpix = [crpix1,crpix2,crpix3]
    w.wcs.cdelt = np.array([cdelt1,cdelt2,cdelt3])
    w.wcs.crval = [crval1,crval2,crval3]
    w.wcs.ctype = [ctype1,ctype2,ctype3]

    xpoints,ypoints,zpoints = w.wcs_world2pix(data['CRVAL2'],
                                              data['CRVAL3'],
                                              data['CRVAL1'],0)
    dataPlane = data['DATA']
    outCube, outWeight = gridData(naxis1,naxis2,naxis3,\
                                  xpoints,ypoints,\
                                  dataPlane)
