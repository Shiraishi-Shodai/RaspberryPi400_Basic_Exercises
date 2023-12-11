""" それぞれのキーがUnicodeで表すと何番になるのか調べるコード"""

import cv2
import numpy as np

while True:
    # 画像を取得
    img = np.full((210, 425, 3), 128, dtype=np.uint8)
    img = cv2.resize(img, (500, 300))
    cv2.imshow("watch key num", img)    
    k= cv2.waitKey(1)
    if k != -1:
        #print("input key num is: ",k, " which means: ", chr(k))
        print(k, ",", chr(k))
        # press enterkey to kill
        if k == 13: break
 
cv2.destroyAllWindows()