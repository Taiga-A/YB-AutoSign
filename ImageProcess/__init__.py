from ast import List
from copy import deepcopy
from PIL import Image
import numpy as np


def noHave(x: int, y: int, array: np.ndarray) -> bool:
    return (x < 0 or y < 0 or x >= array.shape[0] or y >= array.shape[1])


def dfs(x: int, y: int, ptarr: np.ndarray, visit: np.ndarray, img: np.ndarray, clearType: bool = False, clearPoint: List = [255, 255, 255]) -> int:
    if noHave(x, y, img) or visit[x][y] == 1 or (not np.array_equal(img[x][y], ptarr)):
        return 0
    ans = 1
    visit[x][y] = True
    if(clearType):
        img[x][y] = np.array(clearPoint)
    ans += dfs(x+1, y, ptarr, visit, img, clearType, clearPoint)
    ans += dfs(x-1, y, ptarr, visit, img, clearType, clearPoint)
    ans += dfs(x, y+1, ptarr, visit, img, clearType, clearPoint)
    ans += dfs(x, y-1, ptarr, visit, img, clearType, clearPoint)
    return ans

def imageProccess(inputImage: Image.Image) -> Image.Image:
    # inputImage = Image.open("./img.png")
    img = np.asarray(inputImage)
    visit = np.zeros(img.shape[:2])
    shape = img.shape
    voidArr = np.array([255, 255, 255])
    for x in range(shape[0]):
        for y in range(shape[1]):
            if(np.array_equal(img[x][y], voidArr)):
                continue
            visitCopy = deepcopy(visit)
            nums = dfs(x, y, img[x][y], visit, img, clearType=False)
            if(nums < 19):
                dfs(x, y, deepcopy(img[x][y]),
                    visitCopy, img, clearType=True)
            else:
                dfs(x, y, deepcopy(img[x][y]), visitCopy,
                    img, clearType=True, clearPoint=[0, 0, 0])

    return Image.fromarray(img)


if __name__ == "__main__":
    print("这不是程序的正确入口, 请执行main.py")
