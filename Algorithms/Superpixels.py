from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
import skimage.segmentation as seg
import skimage.measure as measure
from skimage.util import img_as_float
from PIL import Image
import numpy as np
import cv2
from DataStructures.Point import Point, ApproxPoint
from DataStructures.Segments.MultipointSegment import MultipointSegment


class Superpixels:
    @staticmethod
    def get_superpixels(img: Image,
                        n_segments: int = 10):
        img_np = img_as_float(np.array(img))
        segments = slic(img_np,
                        n_segments=n_segments,
                        sigma=15,
                        compactness=40)
        s = measure.regionprops(segments)
        empty_img = np.zeros_like(img_np)
        img_np = mark_boundaries(empty_img, segments, color=1)
        boundaries = np.argwhere(img_np != 0)

        edges = {}
        for i in range(len(s)):
            edges[i] = dict()
        a = 1
        for point in boundaries:
            i, j, k = point
            neighbors = [
                segments[i - a if i >= a else i, j],
                segments[i - a if i >= a else i, j - a if j >= a else j],
                segments[i - a if i >= a else i, j + a if j < img_np.shape[1] - a else j],
                segments[i, j - a if j >= a else j],
                segments[i + a if i < img_np.shape[0] - a else i, j],
                segments[i + a if i < img_np.shape[0] - a else i, j + a if j < img_np.shape[1] - a else j],
                segments[i + a if i < img_np.shape[0] - a else i, j - a if j >= a else j],
                segments[i, j + a if j < img_np.shape[1] - 1 else j]
            ]
            neighbors = list(set(neighbors))
            num_neigh = len(neighbors)

            def add_if(first, second):
                if edges.get(first) and edges.get(first).get(second):
                    edges[first][second].add_point(j, i)
                else:
                    edges[first][second] = MultipointSegment(first, second,
                                                             img_np.shape[1], img_np.shape[0])
                    edges[first][second].add_point(j, i)

            if num_neigh == 2:
                first = min(neighbors)
                second = max(neighbors)
                add_if(first, second)

            elif num_neigh == 3:
                neighbors.sort()
                for first, second in [[neighbors[0], neighbors[1]],
                                      [neighbors[1], neighbors[2]],
                                      [neighbors[0], neighbors[2]]]:
                    add_if(first, second)
                    edges[first][second].add_vertex_point(j, i)

        return edges
