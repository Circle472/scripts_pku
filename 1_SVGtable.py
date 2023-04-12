# -*- coding: utf-8 -*-
import json
import numpy as np
from tqdm import tqdm
import multiprocessing as mp
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import info

plt.rcParams["font.sans-serif"] = ["mingliu"]  # font family: 'SimSun宋體'
plt.rcParams["axes.unicode_minus"] = False


def decimal_to_binary(number, digits):
    index = digits - 1
    binaries = [0] * digits
    while number > 0:
        binaries[index] = number % 2  # True / False
        index -= 1
        number >>= 1
    return binaries  # list of booleans


def v_d_s_line(axes):  # vertical dashed line & solid line
    X1 = [10, 140]
    X2 = [154, 284]
    for i in range(10, 198, 17):
        axes.plot(X1, [i, i], linewidth=1, color="black", linestyle="--")
        axes.plot(X2, [i, i], linewidth=1.5, color="black")


def h_d_s_line(axes):  # horizontal dashed line & solid line
    X1 = np.arange(26.25, 124, 16.25)
    X2 = np.arange(170.25, 268, 16.25)
    Y = [10, 180]
    for i in range(7):
        axes.plot([X1[i], X1[i]], Y, linewidth=1, color="black", linestyle="--")
        axes.plot([X2[i], X2[i]], Y, linewidth=1.5, color="black")
    axes.plot([10, 10], [10, 197], linewidth=1, color="black", linestyle="--")
    axes.plot([140, 140], [10, 197], linewidth=1, color="black", linestyle="--")
    axes.plot([154, 154], [10, 197], linewidth=1.5, color="black")
    axes.plot([284, 284], [10, 197], linewidth=1.5, color="black")


def create_plot(page):
    # figure, figsize in inches
    fig = plt.figure(num=page, figsize=(11.69, 8.27), dpi=72, facecolor="white")
    axes = plt.subplot(111)

    plt.text(12, 202, "字體設計與文字編碼", fontsize=12.5, color="black")
    plt.text(65, 202, f"{info.ID}_{info.NAME}", fontsize=12.5, color="black")

    # midline
    axes.plot(
        [147, 147], [5, 205], linewidth=2, color="black", linestyle="--", dashes=(4, 4)
    )

    v_d_s_line(axes)
    h_d_s_line(axes)

    # page number
    temp_page = page + 1
    plt.text(
        110,
        202,
        f"第 {temp_page:>3d}/{info.TOTAL_PAGES} 頁",
        fontsize=12.5,
        color="black",
    )

    # decimal to binary
    binaries = decimal_to_binary(temp_page, 8)

    # square
    for j, fill in enumerate(binaries):
        rect = patches.Rectangle(
            (156 + 16.25 * j, 182.5),
            12,
            12,
            linewidth=1.5,
            edgecolor="black",
            facecolor="black",
            fill=fill,
        )
        axes.add_patch(rect)

    # number
    number = info.NUMBER
    plt.text(12, 192, f"編號：{number:>2d}", fontsize=10, color="black")

    # decimal to binary
    binaries = decimal_to_binary(number, 7)

    # number square
    for j, fill in enumerate(binaries):
        rect = patches.Rectangle(
            (28.25 + 16.25 * j, 182.5),
            12,
            12,
            linewidth=1.5,
            edgecolor="black",
            facecolor="black",
            fill=fill,
        )
        axes.add_patch(rect)


def read_json(file):
    with open(file) as f:
        p = json.load(f)
        v = [""] * 13759
        for i in range(13759):
            # 128 - 255: 'UNICODE' = '     '; 0 - 31: unable to print
            if (128 <= i & i < 256) or (0 <= i & i < 32):
                v[i] = "123"
            else:
                code = p["CP950"][i]["UNICODE"][2:6]
                v[i] = f"\\u{code}"  # ex: 0x1234 --> \\u1234
        return v


def print_font(count, page, fnip):
    index = 0
    for i in range(10):
        for j in range(8):
            if count >= 13759:
                plt.text(12.5 + 16.25 * j, 23 + 17 * i, "", fontsize=32, color="black")
            else:
                if unicode[count] == "123" or count >= 13759:
                    plt.text(
                        12.5 + 16.25 * j, 23 + 17 * i, "", fontsize=32, color="black"
                    )
                    fnip[page][index] = ""  # 第(page+1)頁 第(index+1)個字
                    # plt.text(7+16.25*j, 26.7+17*i, '\\u25A0'.encode('ascii').decode('unicode-escape'), fontsize=64, color='black')
                else:
                    plt.text(
                        12.5 + 16.25 * j,
                        23 + 17 * i,
                        unicode[count].encode("ascii").decode("unicode-escape"),
                        fontsize=32,
                        color="black",
                    )
                    fnip[page][index] = unicode[count][2:6]
                index += 1
            count += 1


def output_svg(filename):
    plt.axis("off")  # 刪除座標軸
    plt.xlim(0, 297)
    plt.ylim(210, 0)
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)  # 刪除白邊
    plt.margins(0, 0)
    plt.savefig(f"./Table/{filename}.svg")


def pipeline(args):
    (page, count) = args
    create_plot(page)
    print_font(count, page, fnip)
    output_svg(f"{page+1:03d}")
    plt.close(page)


fnip = [[""] * 80 for _ in range(info.TOTAL_PAGES)]  # Font Number in Page (Unicode)
unicode = read_json("./CP950.json")

if __name__ == "__main__":
    cpus = mp.cpu_count()  # count of CPU cores
    print(f"Using {cpus = }")
    pool = mp.Pool(cpus)
    args = zip(range(0, info.TOTAL_PAGES), range(0, info.TOTAL_PAGES * 80 + 1, 80))
    for _ in tqdm(pool.imap_unordered(pipeline, args), total=info.TOTAL_PAGES):
        ...
    pool.close()
    pool.join()
