import enoki as ek
import mitsuba

# Set the desired mitsuba variant
mitsuba.set_variant('packet_rgb')

from mitsuba.core import Float, Vector3f
from mitsuba.core.xml import load_string
from mitsuba.render import SurfaceInteraction3f, BSDFContext

import numpy as np
import argparse, textwrap

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def sph_dir(theta, phi):
    """ Map spherical to Euclidean coordinates """
    st, ct = ek.sincos(theta)
    sp, cp = ek.sincos(phi)
    return Vector3f(cp * st, sp * st, ct)

def get_bsdf():
    # Load desired BSDF plugin
    bsdf = load_string("""<bsdf version='2.0.0' type='roughconductor'>
                            <float name="alpha" value="0.2"/>
                            <string name="distribution" value="ggx"/>
                        </bsdf>""")

    # Create a (dummy) surface interaction to use for the evaluation
    si = SurfaceInteraction3f()

    # Specify an incident direction with 45 degrees elevation
    si.wi = sph_dir(ek.pi * 45 / 180, 0.0)

    # Create grid in spherical coordinates and map it onto the sphere
    res = 300
    theta_o, phi_o = ek.meshgrid(
        ek.linspace(Float, 0,     ek.pi,     res),
        ek.linspace(Float, 0, 2 * ek.pi, 2 * res)
    )
    wo = sph_dir(theta_o, phi_o)

    # Evaluate the whole array (18000 directions) at once
    values = bsdf.eval(BSDFContext(), si, wo)
    return values

def plot_bsdf(values):
    res = 300
    # Extract red channel of BRDF values and reshape into 2D grid
    values_r = np.array(values)[:, 0]
    values_r = values_r.reshape(2 * res, res).T

    # Plot values for spherical coordinates
    fig, ax = plt.subplots(figsize=(12, 7))

    im = ax.imshow(values_r, extent=[0, 2 * np.pi, np.pi, 0],
                cmap='jet', interpolation='bicubic')

    ax.set_xlabel(r'$\phi_o$', size=14)
    ax.set_xticks([0, np.pi, 2 * np.pi])
    ax.set_xticklabels(['0', '$\\pi$', '$2\\pi$'])
    ax.set_ylabel(r'$\theta_o$', size=14)
    ax.set_yticks([0, np.pi / 2, np.pi])
    ax.set_yticklabels(['0', '$\\pi/2$', '$\\pi$'])

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.05)
    plt.colorbar(im, cax=cax)

    fig.savefig("bsdf_eval.jpg", dpi=150, bbox_inches='tight', pad_inches=0)
    plt.show()

if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(description='Get BXDF from mitsuba2.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c','--config', dest='config', action='store',
                        help='overwrite by following args') # TODO
    parser.add_argument('-a','--material', dest='material', action='store',
                        help='<bsdf ...>...<bsdf/>') # TODO
    parser.add_argument('-i','--incident-angle', dest='i', action='store',
                        help='[0 ±1 ±2] Incident angle') # TODO
    parser.add_argument('-s','--scattered-angle', dest='s', action='store',
                        help='[0] Scattered angle') # TODO
    parser.add_argument('-d','--mode', dest='mode', action='store',
                        help=textwrap.dedent('''
                            [ 0 ] meshgrid(i, s)
                            [ 1 ] s =  i,       e.g. (i, s) = (30,  30)
                            [-1 ] s = -i,       e.g. (i, s) = (30, 330)
                            [ 2 ] s + i = 180,  e.g. (i, s) = (30, 150)
                            [-2 ] s - i = 180,  e.g. (i, s) = (30, 210)
                            [ 3 ] spherical coordinate''')) # TODO
    parser.add_argument('-ti','--theta-incident', dest='ti', action='store',
                        help='[3] Theta incident') # TODO
    parser.add_argument('-pi','--phi-incident', dest='pi', action='store',
                        help='[3] Phi incident') # TODO
    parser.add_argument('-ts','--theta-scattered', dest='ts', action='store',
                        help='[3] Theta scattered') # TODO
    parser.add_argument('-ps','--phi-scattered', dest='ps', action='store',
                        help='[3] Phi scattered') # TODO
    parser.add_argument('-o','--output-file', dest='o', action='store',
                        help='Output file') # TODO
    parser.add_argument('-n','--output-npy', dest='npy', action='store_', # TODO
                        help='Output format') # TODO
    parser.add_argument('-m','--output-mat', dest='mat', action='store_', # TODO
                        help='Output format') # TODO
    parser.add_argument('-j','--output-mat', dest='jpg', action='store_', # TODO
                        help='Output format') # TODO
    parser.add_argument('-p','--output-mat', dest='png', action='store_', # TODO
                        help='Output format') # TODO
    args = parser.parse_args()
    print(args.f)
    # make data
    values = get_bsdf()
    # show & write data
    plot_bsdf(values)