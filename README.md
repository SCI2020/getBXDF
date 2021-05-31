# getBXDF

get BXDF in mitsuba2

## environment

[build mitsuba2 with variant "packet_rgb"](https://mitsuba2.readthedocs.io/en/latest/)

### Linux

add mitsuba and enoki to python import search path

```
export PYTHONPATH="<..mitsuba repository..>/build/dist/python:$PYTHONPATH"
```

or edit and run

```
source setpypath.sh
```

### Windows

add Environment Variable

|Variable|Value|
|:-:|:-:|
|PYTHONPATH|C:\Users\YOUR-USERNAME\source\repos\mitsuba2\dist\python|

## arguments

```
-h, --help            show this help message and exit
-c CONFIG, --config CONFIG
                      overwrite by following args
-a MATERIAL, --material MATERIAL
                      <bsdf ...>...<bsdf/>
-i I I I, --incident-angle I I I
                      [ 0 ±1 ±2 ] Incident angle
-s S S S, --scattered-angle S S S
                      [ 0 ] Scattered angle
-d MODE, --mode MODE
                      [ 0 ] meshgrid(i, s)
                      [ 1 ] s =  i,       e.g. (i, s) = (30,  30)
                      [-1 ] s = -i,       e.g. (i, s) = (30, 330)
                      [ 2 ] s + i = 180,  e.g. (i, s) = (30, 150)
                      [-2 ] s - i = 180,  e.g. (i, s) = (30, 210)
                      [ 3 ] spherical coordinate
-ti TI TI TI, --theta-incident TI TI TI
                      [ 3 ] Theta incident
-pi PI PI PI, --phi-incident PI PI PI
                      [ 3 ] Phi incident
-ts TS TS TS, --theta-scattered TS TS TS
                      [ 3 ] Theta scattered
-ps PS PS PS, --phi-scattered PS PS PS
                      [ 3 ] Phi scattered
-o O, --output O      Output filename
-n, --npy             Output .npy file
-m, --mat             Output .mat file
-j, --jpg             Output .jpg file
-p, --png             Output .png file
-w, --show            Show plot
```
 
## config file

```
material: "<bsdf ...>...</bsdf>"
i: [START, END, STEPS]
s: [START, END, STEPS]
mode: INT
ti: [START, END, STEPS]
pi: [START, END, STEPS]
ts: [START, END, STEPS]
ps: [START, END, STEPS]
o: FILE
f: "nmjpw"
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
