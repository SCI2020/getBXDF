# getBXDF
get BXDF in mitsuba2

## arguments
```
-config PATH
  overwrite by following args
-material STRING
  "type roughconductor alpha 0.01"
-sun START END STEP
  [START, END), including START, excluding END
-cam START END STEP
  [START, END), required if -follow 0
-follow INT
   0: meshgrid(sun, cam)
   1: cam =  sun,       eg. (sun, cam) = (30,  30)
  -1: cam = -sun,       eg. (sun, cam) = (30, 330)
   2: cam + sun = 180,  eg. (sun, cam) = (30, 150)
  -2: cam - sun = 180,  eg. (sum, cam) = (30, 210)
-o FILE
  output filename, "./out.npy" by default
```
 
## config file
```
material:
  - type: roughconductor
  - alpha: 0.01
sun: [START, END, STEP]
cam: [START, END, STEP]
follow: INT
out: FILE
```

## BRDF
```
sun: [0, 181, 5]
follow: 1
```

## BTDF
```
sun: [0, 181, 5]
follow: -2
```

## BSDF
```
sun: [0, 360, 5]
cam: [0, 360, 5]
follow: 0
```
