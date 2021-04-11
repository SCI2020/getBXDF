# getBXDF
get BXDF in mitsuba2

## environment
[build mitsuba2 with variant "packet_rgb"](https://mitsuba2.readthedocs.io/en/latest/) \
add mitsuba and enoki to python import search path
```
export PYTHONPATH="<..mitsuba repository..>/build/dist/python:$PYTHONPATH"
```

## arguments
```
-config PATH
  overwrite by following args
-material STRING
  "type roughconductor alpha 0.01"
-i START END STEP
  [START, END), including START, excluding END
-s START END STEP
  [START, END), required if -mode 0
-mode INT
   0: meshgrid(i, s)
   1: s =  i,       e.g. (i, s) = (30,  30)
  -1: s = -i,       e.g. (i, s) = (30, 330)
   2: s + i = 180,  e.g. (i, s) = (30, 150)
  -2: s - i = 180,  e.g. (i, s) = (30, 210)
   3: spherical coordinate
-ti START END STEP
  polar angle of the incident, required if -mode 3
-pi START END STEP
  azimuthal angle of the incident, required if -mode 3
-ts START END STEP
  polar angle of the scatter, required if -mode 3
-ps START END STEP
  azimuthal angle of the scatter, required if -mode 3
-o FILE
  output filename, "./out.npy" by default
```
 
## config file
```
material:
  - type: roughconductor
  - alpha: 0.01
i: [START, END, STEP]
s: [START, END, STEP]
mode: INT
ti: [START, END, STEP]
pi: [START, END, STEP]
ts: [START, END, STEP]
ps: [START, END, STEP]
o: FILE
```

## BRDF-coincident
```
i: [0, 181, 5]
mode: 1
```

## BTDF-specular
```
i: [0, 181, 5]
mode: -2
```

## BSDF-circle
```
i: [0, 360, 5]
s: [0, 360, 5]
mode: 0
```

## BSDF-spherical
```
mode: 3
ti: [60, 121, 5]
pi: [45, 136, 5]
ts: [60, 121, 5]
ps: [45, 136, 5]
```

## references
https://mitsuba2.readthedocs.io/en/latest/src/python_interface/bsdf_eval.html \
https://github.com/mitsuba-renderer/mitsuba2/blob/master/docs/examples/05_bsdf_eval/bsdf_eval.py
