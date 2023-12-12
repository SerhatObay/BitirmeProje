import cv2
import pickle

image_path = "first_frame.png"

try:
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Hata: Yüklenecek resim bulunamadı. '{image_path}'.")

    with open("noktalar", "rb") as f:
        liste = pickle.load(f)
except FileNotFoundError:
    print(f"Uyarı: Dosya bulunamadı.")
    liste = []

def mouse(event, x, y, flags, params):
    global liste
    if event == cv2.EVENT_LBUTTONDOWN:
        liste.append((x, y))

    elif event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in reversed(list(enumerate(liste))):
            x1, y1 = pos
            if x1 < x < x1 + 24 and y1 < y < y1 + 12:
                liste.pop(i)

    with open("noktalar", "wb") as f:
        pickle.dump(liste, f)

cv2.namedWindow("otopark")
cv2.setMouseCallback("otopark", mouse)

while True:
    img_copy = img.copy()
    for l in liste:
        cv2.rectangle(img_copy, l, (l[0] + 24, l[1] + 12), (255, 0, 0), 2)

    cv2.imshow("otopark", img_copy)

    cv2.waitKey(10)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
