import numpy as np
import cv2
from collections import namedtuple
import operator
import os

def angle_cos(p0, p1, p2):
    d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))


def find_cards(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    cards = []

    for gray in cv2.split(img):
        for thrs in range(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                _, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
                rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
                topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
                bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos(cnt[i], cnt[(i + 1) % 4], cnt[(i + 2) % 4]) for i in range(4)])
                    if max_cos < 0.1 and cv2.contourArea(cnt) < 50000:
                        cards.append(cv2.boundingRect(np.array([leftmost, rightmost, topmost, bottommost])))
    return cards


def find_shapes(image):
    num_shapes = {"squiggles": 0, "diamonds": 0, "ovals": 0}

    blur_img = cv2.blur(image, (3, 3))
    gray_img = cv2.cvtColor(blur_img, cv2.COLOR_BGR2GRAY)
    thr_image = cv2.Canny(gray_img, 40, 210, apertureSize=3)
    thr_image = cv2.dilate(thr_image, np.ones((3, 3), np.uint8))
    contours, _ = cv2.findContours(thr_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            cv2.drawContours(card_img, [cnt], 0, (0, 255, 0), 1)
            epsilon = 0.01 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            if approx.shape[0] < 9:
                num_shapes["diamonds"] += 1
            elif approx.shape[0] > 12:
                num_shapes["squiggles"] += 1
            else:
                num_shapes["ovals"] += 1

    total_num_shapes = num_shapes["ovals"] + num_shapes["squiggles"] + num_shapes["diamonds"]
    shape_type = max(num_shapes.items(), key=operator.itemgetter(1))[0]
    shapes = namedtuple("shapes", ["type", "number", "color", "shade"])
    return shapes(shape_type, total_num_shapes, "UNKNOWN", "UNKNOWN")

if __name__ == '__main__':
    from glob import glob
    save_folder = "/Users/dimitrichrysafis/PycharmProjects/setSolverCV/cards"
    os.makedirs(save_folder, exist_ok=True)

    for fn in glob('gameboard2.jpg'):
        img = cv2.imread(fn)
        cards = find_cards(img)
        cards = cv2.groupRectangles(cards, 1, 0.2)[0]  # Updated groupRectangles call

        for idx, card in enumerate(cards):
            card_img = img[card[1]:card[1]+card[3], card[0]:card[0]+card[2]]
            card_filename = os.path.join(save_folder, f'card_{idx + 1}.jpg')
            cv2.imwrite(card_filename, card_img)
            print(f"Saved {card_filename}")

            cv2.imshow(f'Card {idx + 1}', card_img)
            ch = cv2.waitKey(0)
            if ch == 27:
                break

        print("Found {num} cards.".format(num=len(cards)))

        img_with_shapes = img.copy()
        for card in cards:
            cv2.rectangle(img_with_shapes, (card[0], card[1]), (card[0]+card[2], card[1]+card[3]), (255, 0, 0), thickness=2)

        cv2.imshow('squares', img_with_shapes)
        ch = cv2.waitKey()
        if ch == 27:
            break

    cv2.destroyAllWindows()
