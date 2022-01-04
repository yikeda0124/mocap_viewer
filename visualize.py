import pandas as pd
import argparse
import matplotlib.pyplot as plt
import os
import glob
import cv2
from mpl_toolkits.mplot3d import Axes3D


def read_csv(filename):
    df = pd.read_csv('./data/' + filename + '.csv', header=None)
    return df

def delete_images(savedir):
    pathname = savedir + '*.png'
    for p in glob.glob(pathname):
        if os.path.isfile(p):
            os.remove(p)

def make_figure(savedir, data):
    index = int(data[0])
    print('processing', index)
    pathname = savedir + ('000'+str(index))[-4:] + '.png'
    
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlim(1, 2)
    ax.set_ylim(1, 2)
    ax.set_zlim(0, 0.5)

    for i in range(2, len(data), 3):
        if not pd.isnull(data[i]):
            ax.scatter(data[i], data[i+1], data[i+2])

    fig.savefig(pathname)
    plt.clf()
    plt.close()

def make_movie(savedir, fps):
    now = datetime.datetime.now()
    pathname = savedir + now.strftime('%Y%m%d_%H%M%S') + '.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    outfh = cv2.VideoWriter(pathname, fourcc, fps, (640, 480))
    for photo_name in sorted(glob.glob('./images/*.png')):
        im = cv2.imread(photo_name)
        outfh.write(im)
    outfh.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='visualize mocap data')
    parser.add_argument('--filename', type=str, default='throw1', help='specify filename')
    parser.add_argument('--savedir', type=str, default='./images/', help='movie save dir')
    parser.add_argument('--fps', type=int, default=120, help='mocap rec fps')

    args = parser.parse_args()

    df = read_csv(args.filename)

    delete_images(args.savedir)

    for index, data in df.iterrows():
        make_figure(args.savedir, data)

    make_movie(args.savedir, args.fps)
    delete_images(args.savedir)
    print('done!')
