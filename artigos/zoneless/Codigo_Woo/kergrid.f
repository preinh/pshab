C*****************************************************************
C*****************************************************************
C  PROGRAM  KERFRANCE                                            *
C                                                                *
C  FORTRAN program to evaluate magnitude-dependent activity rates*
C  at a box-array of (Lat., Lon.) grid locations, using a        *
C  regional catalogue of shallow earthquakes.                    *
C  The program allows use of two alternative types of kernel:    *                                                
C  one infinite (AKER; Vere-Jones 1992), and the other finite    * 
C  (AKER1; Kagan and Jackson, JGR, Vol.99, 1994)                 *
C                                                                *
C  The (Lat., Lon.) epicentres in the catalogue are smoothed by  *
C  a directional fractal kernel.                                 * 
C                                                                *
C  Version 1.0    March 2001                                     *                                                                 *
C  Written by Dr. Gordon Woo (Ref: BSSA,Vol.86,No.2, April 1996) *
C                                                                *
C                                                                *
C  Subroutines:  AKER, AKER1                                     *
C  --------------------------------------------------------------*                  
C  Input Files:  CATALIN.D   {Earthquake catalogue}              *
C                   KGIN.D   {Kernel and problem-specific data}  *
C  Output File:    KGOUT.D   {Grid activity Rate Output}         *
C                                                                *
C  Arrays are dimensioned for up to 5000 events in the catalogue *
C  and for a main grid block of size 200 x 200.                  *
C ****************************************************************
C  Below is an illustration of a rectangular Main Block consisting 
C  of 6 x 2 = 12 sub-blocks.  The horizontal width of each sub-block 
C  is DX; and the vertical height of each sub-block is DY.
C
C              ------------------------------------
C              | DX  |     |     |     |     |     |
C            D |     |     |     |     |     |     |
C            Y |     |     |     |     |     |     |
C              -------------------------------------
C              |     |     |     |     |     |     |
C              |     |     |     |     |     |     |
C              |     |     |     |     |     |     |
C              -------------------------------------
C
C******************************************************************* 
      COMMON/QUAKE/QKE(5000,4),ERR(5000,4),YR(5000),DL(5000),TH(5000)
      COMMON/GRID/XLAM(11,200,200)
      COMMON/GRD/NGLOBX, NGLOBY,GMESH
      COMMON/BAND/PL,BWIDA,BWIDB,RMIN,RMAX,DELDIR
      DIMENSION IYR(5000),IM(5000), ID(5000), TIT(80),TOTMAG(11)
      DIMENSION EPHI(22), DEEP(5000)
      DIMENSION XMAG(11)
      DATA EPHI/0.00,10.18,16.20,20.70,24.48,27.88,31.00,33.97,36.80
     *,39.55,42.25,44.92,47.62,50.28,53.02,55.83,58.77,61.85,65.18
     *,68.87,73.18,78.83/
      OPEN(UNIT=5,FILE='catalin.d')
      OPEN(UNIT=6,FILE='kgout.d')
      OPEN(UNIT=7,FILE='kgin.d')
C Read in Title card
      READ (7,991) (TIT(I),I=1,80)
      WRITE(6,992) (TIT(I),I=1,80)
991   FORMAT(80A1)
992   FORMAT('KERGRID PROGRAM:  ',80A1,//)
C 
C Read in flag for infinite or finite kernel
      READ (7,928) NKER
C Read in Kernel fractal scaling index
      READ (7,917) PL
917   FORMAT(/50X,F14.4)
C Read in Kernel bandwidth parameters (a,b) in H=a.exp(bM)
      READ( 7,909) BWIDA, BWIDB
909   FORMAT(50X,2F12.3)
C Read in Finite Kernel minimum and maxmium radii (km)
      READ(7,909) RMIN, RMAX
C Read in the parameter which controls the azimuthal concentration
C     of seismic activity around a fault plane
      READ(7,909) DELDIR
C
C
C Read in numbers of main grid blocks {Lat. x Lon.}
      READ (7,928) NGLOBY, NGLOBX
      NGXY = NGLOBX*NGLOBY
C Read in Latitude and Longitude of Southwestmost site coordinates
      READ( 7, 909) YSIT0, XSIT0
C
C Calculate site conversion factors for degrees latitude and longitude
      DO 17 IPHI=1,22
      IPOL=23-IPHI
      IF (ABS(YSIT0+5.0).GE.EPHI(IPOL)) GOTO 19
  17  CONTINUE
  19  HGHT=FLOAT(8-IPOL)
      PI2=0.017453293
      RADY=PI2*(6371.0+HGHT)
C
C
C Read in width of a main grid block (fraction of deg. Latitude)
      READ (7,929) DY
C Read in height of a main grid block (fraction of deg. Longitude)
      READ (7,929) DX
C Read in Sub-Grid mesh size (kms)
      READ (7,929) GMESH
928   FORMAT(/50X,2I9)
929   FORMAT(50X,F14.4)
C
C  Read in the extra magnitude-dependent activity rate contributions
C  for the entire block
      READ(7,969)
969   FORMAT()
      DO 33 NG = 1,11
      READ (7, 913) XMAG(NG)
913   FORMAT(50X,F6.2)
33    CONTINUE
C
C  Read in catalogue magnitude observability periods
      READ(7,969)
      READ(7,937) IPER40
      READ(7,937) IPER45
      READ(7,937) IPER50
      READ(7,937) IPER55
      READ(7,937) IPER60
      READ(7,937) IPER65
      READ(7,937) IPER70
937   FORMAT(50X,I10)
C
C Read in earthquake dates, epicentres, (Latitude and Longitude)  
C and magnitudes.
C
C Read in the angle of lineament (from fault mapping, fault plane
C solution etc.)   TH(I)
C (angle is measured in degrees anticlockwise from due East).
C Use may be made of focal mechanism solutions.
C      
      CATMAX = 0.0
C Read in the number of events in the shallow earthquake catalogue
      READ(5,988) NPT
988   FORMAT(28X,I6,/) 
      DO 10 I=1,NPT
C Read event Date, Longitude, Latitude, Magnitude, Lineament angle      
      READ(5,990) IYR(I),IM(I),ID(I),KDEP,QKE(I,2),QKE(I,1),QKE(I,3)
      DEEP(I) = KDEP
      TH(I) = 0.0
990   FORMAT(I5,I5,I5,I5,F7.4,7X,F7.4,46X,F3.1)
      DL(I) = DELDIR
C Assume isotropic smoothing if a null lineament angle is given
      IF (TH(I).LT.0.01) DL(I) = 0.0
C
C
      IF (  QKE(I,3).GE.7.0)                         YR(I) = IPER70
      IF ( (QKE(I,3).GE.6.5).AND.(QKE(I,3).LT.7.0) ) YR(I) = IPER65      
      IF ( (QKE(I,3).GE.6.0).AND.(QKE(I,3).LT.6.5) ) YR(I) = IPER60            
      IF ( (QKE(I,3).GE.5.5).AND.(QKE(I,3).LT.6.0) ) YR(I) = IPER55 
      IF ( (QKE(I,3).GE.5.0).AND.(QKE(I,3).LT.5.5) ) YR(I) = IPER50     
      IF ( (QKE(I,3).GE.4.5).AND.(QKE(I,3).LT.5.0) ) YR(I) = IPER45           
      IF ( (QKE(I,3).GE.4.0).AND.(QKE(I,3).LT.4.5) ) YR(I) = IPER40  
C
C
      IF (QKE(I,3).GT.CATMAX) CATMAX = QKE(I,3)
10    CONTINUE
C
C%%%%%%%%%%%%%%%%%%%%%%%%%%% END OF DATA INPUT %%%%%%%%%%%%%%%%%%%%%%%%
C
C
C 2*DELTA is the magnitude increment used in summing over events
C of different sizes
      DELTA = 0.125
C Initialize magnitude-dependent grid activity rate densities
      DO 150 MAGN  = 1,10
      DO 150 KSITX = 1,NGLOBX
      DO 150 KSITY = 1,NGLOBY
150   XLAM(MAGN,KSITX,KSITY) = 0.0
C&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
C
C Iterate over the regional catalogue events
      DO 200 I=1,NPT
      IF (QKE(I,3).LT.4.0) GOTO 200
      IF (DEEP(I).GT.40.0) GOTO 200
C Evaluate the contribution from each event (Magnitude 4+)
C to the Grid sub-block (KSITX, KSITY)
      DO 400 KSITY = 1, NGLOBY
      YSITE = YSIT0 + DY*(KSITY-1)
      RADX=COS(YSITE*PI2)*RADY
C
      DO 400 KSITX = 1, NGLOBX
      XSITE = XSIT0 + DX*(KSITX-1)
C      
      Y0 = (QKE(I,1) - YSITE) * RADY            
      X0 = (QKE(I,2) - XSITE) * RADX
C Filter out events which are too distant to contribute 
C to the grid activity rate density
      DISG = SQRT(X0*X0+Y0*Y0)
      IF (DISG.GT.500.0) GOTO 400
C
C Consider different magnitude values, ranging from 4.0 up to 6.5
      DO  500 MG = 1,11
C GMAG is the magnitude associated with the intensity distribution
      GMAG = 4.0 + (MG-1)*2.0*DELTA 
C
C Check if the event magnitude lies
C between GMAG + DELTA and GMAG - DELTA
      DMAG = ABS(QKE(I,3) - GMAG)
C Skip to next magnitude, if this magnitude is not close to GMAG
C
      IF (DMAG.GE.DELTA) GOTO 500 
C      
C Integrate over sub-block to derive sub-block contributions
      NGRIDX = DX*RADX/GMESH
      NGRIDY = DY*RADY/GMESH
C
      DO 50 IX = 1,NGRIDX
      DO 50 IY = 1,NGRIDY
C Accumulate the activity rate densities within a sub-block
      XPOS = (IX-NGRIDX*0.5)*GMESH
      YPOS = (IY-NGRIDY*0.5)*GMESH
C Choose either the infinite or finite kernel
      IF (NKER.EQ.0) ADD = AKER(I,GMAG,XPOS-X0,YPOS-Y0)/(YR(I)) 
      IF (NKER.EQ.1) ADD = AKER1(I,GMAG,XPOS-X0,YPOS-Y0)/(YR(I))  
C      
      XLAM(MG,KSITX,KSITY) = XLAM(MG,KSITX,KSITY) + ADD*GMESH*GMESH
50    CONTINUE
C
C Cycle over all scenario magnitudes
500   CONTINUE
C Cycle over all sub-blocks within the Main Block
400   CONTINUE
C Cycle over all catalogue events
200   CONTINUE
C
C Allow for Additional Background Seismicity Events
      DO 600 MG = 1,11
      GMAG = 4.0 + (MG-1)*2.0*DELTA   
      DO 650 KSITX=1,NGLOBX
      DO 650 KSITY=1,NGLOBY
      XLAM(MG,KSITX,KSITY)=XLAM(MG,KSITX,KSITY)+XMAG(MG)/(FLOAT(NGXY))
650   CONTINUE
600   CONTINUE
C
C Output Activity Rates at Global Grid Locations
      SUM = 0.0
      DO 700 MG = 1,11
      TOTMAG(MG) = 0.0
      GMAG = 4.0 + (MG-1)*2.0*DELTA   
      DO 750 KSITX=1,NGLOBX
      XSITE = XSIT0 + DX*(KSITX-1)     
      DO 750 KSITY=1,NGLOBY
      YSITE = YSIT0 + DY*(KSITY-1)     
C Accumulate the magnitude-dependent activity rates over the region     
      TOTMAG(MG) = TOTMAG(MG) + XLAM(MG,KSITX,KSITY) 
C Output the main scenario parameters: Lat., Lon., Mag., Activity Rate      
      WRITE(6,733) YSITE,XSITE, GMAG, XLAM(MG,KSITX,KSITY)
733   FORMAT(3F8.2,5X,E15.4)
750   CONTINUE
C Accumulate the regional activity rates over all magnitudes
      SUM = SUM + TOTMAG(MG)
700   CONTINUE
C Write out the total regional activity, and the breakdown according
C to magnitude:5, 5.25, 5.5, 5.75, 6.0, 6.25, 6.5
      WRITE(*,674)
674   FORMAT(//,6X,'  ACTIVITY RATES AGGREGATED OVER THE MAIN BLOCK') 
      WRITE(*,675)   
675   FORMAT(6X,'4.0         4.25        4.50         4.75        5.00')
      WRITE(*,676) (TOTMAG(K),K=1,5)
      WRITE(*,677)  
677   FORMAT(//,6X,'5.25        5.50        5.75         6.00'        
     *,'        6.25         6.50')         
      WRITE(*,676) (TOTMAG(K),K=6,11)           
676   FORMAT(8E12.2)
      WRITE(*,678) SUM
678   FORMAT(//'RATE OF ACTIVITY OF EVENTS > 4.0:',E12.2)
C      
      STOP
      END
C
C
      FUNCTION AKER(IQ,GMAG,X,Y)
C******************************************************************
C Infinite range Kernel function for smoothing intensities        *
C See Vere-Jones (1992)                                           *
C******************************************************************
      COMMON/QUAKE/QKE(5000,4),ERR(5000,4),YR(5000),DL(5000),TH(5000)
      COMMON/GRID/XLAM(11,200,200)
      COMMON/GRD/NGLOBX,NGLOBY,GMESH
      COMMON/BAND/PL,BWIDA,BWIDB,RMIN,RMAX,DELDIR
      PI = 3.14159265
      RAD = PI/180.0
C H is the bandwidth of the kernel   
      H = BWIDA*EXP(BWIDB*GMAG)
      CN = PI/(PL-1.0)
      H2 =H*H
      CONST = 1.0/(CN*H2)
C CANG is the normalization for the anisotropic factor ANISO
      CANG = 2.0*PI/( 2.0*PI + DL(IQ)*PI )
      R2 = X*X + Y*Y
      IF (R2.LT.0.01) X = 0.01
      ANG1 = ATAN2(Y,X)
      ANG2 = TH(IQ)*RAD
      IF (ANG2.GT.PI) ANG2 = -2.0*PI + ANG2
C ANG is the orientation of the site with respect to the lineament
      ANG = ANG1 - ANG2
      ANISO = (1.0+DL(IQ)*COS(ANG)*COS(ANG)) * CANG   
      ATTEN = (1.0 + (R2/H2))**(-PL)
      AKER = CONST*ANISO*ATTEN
      RETURN
      END 
C      
      FUNCTION AKER1(IQ,GMAG,X,Y)
C******************************************************************
C Kernel function for smoothing intensities                       *
C using a finite range kernel (Kagan and Jackson, 1994)           *
C******************************************************************
      COMMON/QUAKE/QKE(5000,4),ERR(5000,4),YR(5000),DL(5000),TH(5000)
      COMMON/GRID/XLAM(11,200,200)
      COMMON/GRD/NGLOBX,NGLOBY,GMESH
      COMMON/BAND/PL,BWIDA,BWIDB,RMIN,RMAX,DELDIR
      PI = 3.14159265
      RAD = PI/180.0
      CN = 2.0*PI*(RMAX - RMIN*0.5)
      CONST = 1.0/CN
C CANG is the normalization for the anisotropic factor ANISO
      CANG = 2.0*PI/( 2.0*PI + DL(IQ)*PI )
      R2 = X*X + Y*Y
      R = SQRT(R2)
      IF (R2.LT.0.01) X = 0.01
      ANG1 = ATAN2(Y,X)
      ANG2 = TH(IQ)*RAD
      IF (ANG2.GT.PI) ANG2 = -2.0*PI + ANG2
C ANG is the orientation of the site with respect to the lineament
      ANG = ANG1 - ANG2
      ANISO = (1.0+DL(IQ)*COS(ANG)*COS(ANG)) * CANG   
      IF (R.LT.RMIN) ATTEN = 1.0/RMIN    
      IF (R.GT.RMIN) ATTEN = 1.0/R
      IF (R.GT.RMAX) ATTEN = 0.0
      AKER1 = CONST*ANISO*ATTEN
      RETURN
      END 

