from PIL import Image
import numpy as np

orig_color_correction = np.array([
    [1.3251670598983765, -0.08847951143980026, -0.2366875857114792],
    [-0.2856792211532593, 1.39799964427948, -0.11233043670654297],
    [-0.03820543736219406, -0.722199022769928, 1.7604109048843384]
])

undo_color_correction = np.linalg.inv(orig_color_correction)

img_arr = np.array(Image.open("other_data\\arducam_uncorrected.png"))
new_img_arr = np.zeros_like(img_arr)

print(img_arr.shape)

for row in range(img_arr.shape[0]):
    if row % 10 == 0:
        print(row / img_arr.shape[0])
    for col in range(img_arr.shape[1]):
        new_img_arr[row,col,:] = orig_color_correction @ img_arr[row,col,:]

Image.fromarray(new_img_arr).save("other_data\\arducam_recorrected.png")

