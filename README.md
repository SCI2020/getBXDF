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
-i START END STEPS
  [START, END], including START and END
-s START END STEPS
  [START, END], required if -mode 0
-mode INT
   0: meshgrid(i, s)
   1: s =  i,       e.g. (i, s) = (30,  30)
  -1: s = -i,       e.g. (i, s) = (30, 330)
   2: s + i = 180,  e.g. (i, s) = (30, 150)
  -2: s - i = 180,  e.g. (i, s) = (30, 210)
   3: spherical coordinate
-ti START END STEPS
  polar angle of the incident, required if -mode 3
-pi START END STEPS
  azimuthal angle of the incident, required if -mode 3
-ts START END STEPS
  polar angle of the scatter, required if -mode 3
-ps START END STEPS
  azimuthal angle of the scatter, required if -mode 3
-o FILE
  output filename, "./out.npy" by default
```
 
## config file
```
material:
  - type: roughconductor
  - alpha: 0.01
i: [START, END, STEPS]
s: [START, END, STEPS]
mode: INT
ti: [START, END, STEPS]
pi: [START, END, STEPS]
ts: [START, END, STEPS]
ps: [START, END, STEPS]
o: FILE
```

## BRDF-coincident
```
i: [0, 180, 100]
mode: 1
```

## BTDF-specular
```
i: [0, 180, 100]
mode: -2
```

## BSDF-circle
```
i: [0, 360, 200]
s: [0, 360, 200]
mode: 0
```

## BSDF-spherical
```
mode: 3
ti: [60, 120, 50]
pi: [45, 135, 50]
ts: [60, 120, 50]
ps: [45, 135, 50]
```

## references
https://mitsuba2.readthedocs.io/en/latest/src/python_interface/bsdf_eval.html \
https://github.com/mitsuba-renderer/mitsuba2/blob/master/docs/examples/05_bsdf_eval/bsdf_eval.py
