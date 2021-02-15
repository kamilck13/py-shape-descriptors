import math
import statistics

import cv2
from math import pi
from warnings import warn

from descriptors.utils import moments as m


def circularity(image, method='Ch', approx_contour=True):
    """
    Function defines two methods of computing circularity.
    C_H: uses Hu moments
    C_st: compares area to perimeter
    I_da:  Inner Distance Approach
    :param image:  np.ndarray, binary mask
    :param method: method
    :param approx_contour: approximate contour to give smoother lines, reduce noise and
                           compute better perimeter approximation
    :return: float \in [0, 1]
    """
    if method == 'Ch':
        m00 = m.m00(image)

        mu20 = m.mu20(image)
        mu02 = m.mu02(image)

        return (m00 * m00) / (2.0 * pi * (mu20 + mu02))
    elif method == 'Cst':
        area = m.m00(image)

        contours, _ = cv2.findContours(image, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 1:
            warn("More than one blob?")
        cnt = contours[0]

        if approx_contour:
            cnt = cv2.approxPolyDP(cnt, epsilon=1, closed=True)
        perimeter = cv2.arcLength(cnt, closed=True)

        return 4 * pi * area / perimeter ** 2
    elif method == 'Ida':
        # calculate moments of binary image
        M = cv2.moments(image)

        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        contours, _ = cv2.findContours(image, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

        if len(contours) != 1:
            warn("More than one blob?")
        cnt = contours[0]

        distances = []
        for contour in contours:
            for c in contour:
                x, y, _, _ = cv2.boundingRect(c)
                distances.append(math.sqrt((x - cX) ** 2 + (y - cY) ** 2))

        mean = statistics.mean(distances)
        deviation = statistics.pstdev(distances)

        return round(mean/deviation/100, 4)
    elif method == 'Rsa':
        area = m.m00(image)
        side = findLargestSquare(image)
        r = (side / 2) * math.sqrt(2)
        area_r = math.pi * r ** 2
        if area_r < area:
            return round(area_r / area, 4)
        return round(area / area_r, 4)
    else:
        warn("Unknown method.")


def findLargestSquare(M):
    # `T[i][j]` stores the size of maximum square submatrix ending at `M[i][j]`
    T = [[0 for x in range(len(M[0]))] for y in range(len(M))]

    # `max` stores the size of the largest square submatrix of 1's
    max = 0

    # fill in a bottom-up manner
    for i in range(len(M)):
        for j in range(len(M[0])):
            T[i][j] = M[i][j]

            # if we are not at the first row or first column and the
            # current cell has value 1
            if i > 0 and j > 0 and M[i][j] == 1:
                # largest square submatrix ending at `M[i][j]` will be 1 plus
                # minimum of largest square submatrix ending at `M[i][j-1]`,
                # `M[i-1][j]` and `M[i-1][j-1]`

                T[i][j] = min(T[i][j - 1], T[i - 1][j], T[i - 1][j - 1]) + 1

            # update maximum size found so far
            if max < T[i][j]:
                max = T[i][j]

    # return size of the largest square matrix
    return max