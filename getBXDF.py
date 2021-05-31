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

def get_bsdf_s(args, theta_i, phi_i):
    # Load desired BSDF plugin
    bsdf = load_string(args.material)

    # Create a (dummy) surface interaction to use for the evaluation
    si = SurfaceInteraction3f()

    # Specify an incident direction with 45 degrees elevation
    si.wi = sph_dir(theta_i, phi_i)

    # Create grid in spherical coordinates and map it onto the sphere
    d2r = ek.pi / 180
    theta_s, phi_s = ek.meshgrid(
        ek.linspace(Float, d2r*args.ts[0], d2r*args.ts[1], args.ts[2]),
        ek.linspace(Float, d2r*args.ps[0], d2r*args.ps[1], args.ps[2])
    )
    ws = sph_dir(theta_s, phi_s)

    # Evaluate the whole array (18000 directions) at once
    values = bsdf.eval(BSDFContext(), si, ws)
    values_r = np.array(values)[:, 0]
    values_r = values_r.reshape(args.ts[2], args.ps[2]).T
    return values_r

def get_bsdf_i(args): # parallel get_bsdf_s
    ret = np.zeros((args.ti[2], args.pi[2], args.ts[2], args.ps[2]),
                    dtype=float)
    pass

def plot_bsdf(args, values):
    res = 128
    # Extract red channel of BRDF values and reshape into 2D grid
    values_r = np.array(values)[:, 0]
    values_r = values_r.reshape(res, res).T

    # Plot values for spherical coordinates
    fig, ax = plt.subplots(figsize=(8, 8))

    im = ax.imshow(values_r, extent=[0, 2 * np.pi, 2 * np.pi, 0],
                cmap='jet', interpolation='bicubic')

    ax.set_xlabel(r'$\phi_o$', size=14)
    ax.set_xticks([0, np.pi, 2 * np.pi])
    ax.set_xticklabels(['0', '$\\pi$', '$2\\pi$'])
    ax.set_ylabel(r'$\theta_o$', size=14)
    ax.set_yticks([0, np.pi, 2 * np.pi])
    ax.set_yticklabels(['0', '$\\pi$', '$2\\pi$'])

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.05)
    plt.colorbar(im, cax=cax)

    #fig.savefig("bsdf_eval.jpg", dpi=150, bbox_inches='tight', pad_inches=0)
    plt.show()

if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser(description='Get BXDF from mitsuba2.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c','--config', dest='config',
                        action='store', type=str, default=None,
                        help='overwrite by following args')
    parser.add_argument('-a','--material', dest='material',
                        action='store', type=str,
                        default="<bsdf version='2.0.0' type='roughconductor'><float name='alpha' value='0.2'/><string name='distribution' value='ggx'/></bsdf>",
                        help='<bsdf ...>...<bsdf/>')
    parser.add_argument('-i','--incident-angle', dest='i',
                        action='store', nargs=3,
                        default=[0.0, 360.0, 128],
                        help='[ 0 ±1 ±2 ] Incident angle')
    parser.add_argument('-s','--scattered-angle', dest='s',
                        action='store', nargs=3,
                        default=[0.0, 360.0, 128],
                        help='[ 0 ] Scattered angle')
    parser.add_argument('-d','--mode', dest='mode',
                        action='store', type=int, default=3,
                        help=textwrap.dedent('''
                            [ 0 ] meshgrid(i, s)
                            [ 1 ] s =  i,       e.g. (i, s) = (30,  30)
                            [-1 ] s = -i,       e.g. (i, s) = (30, 330)
                            [ 2 ] s + i = 180,  e.g. (i, s) = (30, 150)
                            [-2 ] s - i = 180,  e.g. (i, s) = (30, 210)
                            [ 3 ] spherical coordinate'''))
    parser.add_argument('-ti','--theta-incident', dest='ti',
                        action='store', nargs=3,
                        default=[0.0, 360.0, 128],
                        help='[ 3 ] Theta incident')
    parser.add_argument('-pi','--phi-incident', dest='pi',
                        action='store', nargs=3,
                        default=[0.0, 360.0, 128],
                        help='[ 3 ] Phi incident')
    parser.add_argument('-ts','--theta-scattered', dest='ts',
                        action='store', nargs=3,
                        default=[0.0, 360.0, 128],
                        help='[ 3 ] Theta scattered')
    parser.add_argument('-ps','--phi-scattered', dest='ps',
                        action='store', nargs=3,
                        default=[0.0, 360.0, 128],
                        help='[ 3 ] Phi scattered')
    parser.add_argument('-o','--output', dest='o', action='store',
                        default='out', help='Output filename')
    parser.add_argument('-n','--npy', dest='npy', action='store_true',
                        default=False, help='Output .npy file')
    parser.add_argument('-m','--mat', dest='mat', action='store_true',
                        default=False, help='Output .mat file')
    parser.add_argument('-j','--jpg', dest='jpg', action='store_true',
                        default=False, help='Output .jpg file')
    parser.add_argument('-p','--png', dest='png', action='store_true',
                        default=False, help='Output .png file')
    parser.add_argument('-w','--show', dest='show', action='store_true',
                        default=False, help='Show plot')
    args = parser.parse_args()
    # make data
    values = get_bsdf_s(args, 0, 0)
    print(np.array(values).shape)
    # show & write data
    #plot_bsdf(values,args)