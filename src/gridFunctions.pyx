import math

def sincGridC(double xpix, double ypix, 
              double xdata, double ydata,
              double pixPerBeam):
    cdef double a,b,Rsup,dmin,distance,pia,wt,b2
    a = 1.55
    b = 2.52
    b2 = 1/b**2
    Rsup = 3.
    dmin = 1e-4
    pia = 3.1415626535897/a

    distance = (((xdata-xpix)/pixPerBeam)**2+\
                ((ydata-ypix)/pixPerBeam)**2)**(0.5)
    if distance>Rsup:
        return(0.0)
    if distance<dmin:
        return(1.0)
    wt = math.exp(-distance**2*b2)*\
         math.sin(pia*distance)/\
         (pia*distance)
    return wt
