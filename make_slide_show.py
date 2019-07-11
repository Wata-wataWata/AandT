import os
import pathlib
import subprocess

HOME_PATH = "./"
TITLE_PATH = "title/AT2019_C*"
WORKS_PATH = "works/AT2019_C*"

CONVERT_IMAGE_TO = "png"

# 高さを合わせるコマンド
# OSXにしかないかも？
CMD_RESAMPLE_HEIGHT = ["sips", "--resampleHeight", "1080", "tmp/*"]
# 2Kに合わせて切り抜くコマンド
CMD_CROP_FULLHD = ["sips", "-c", "1080", "1920", "tmp/*"]
# スライドショーを作るコマンド
CMD_MAKE_SLIDE_SHOW = ["ffmpeg", "-y", "-r", "0.2", "-i", "tmp/%03d.png",
                       "-b:v", "3000k", "-c:v", "h264", "-pix_fmt", "yuv420p", "-r", "30", "out.mp4"]


def main():

    # init
    subprocess.call("rm ./tmp/*", shell=True)

    # 画像からスライドショーを作る

    # タイトルと作品の画像を探索
    p_title = pathlib.Path(HOME_PATH)
    title_list = sorted(list(p_title.glob(TITLE_PATH)))
    work_list = sorted(list(p_title.glob(WORKS_PATH)))

    slide_list = list()

    # タイトルがあるものを全部探す
    for i in range(len(title_list)):
        slide_list.append(title_list[i])

        # work_listがディレクトリの時
        if os.path.isdir(str(work_list[i])):
            works = sorted(list(p_title.glob(str(work_list[i]) + "/*")))
            for x in works:
                slide_list.append(x)
        # 画像一枚の時
        else:
            slide_list.append(work_list[i])

    # slide_listの画像たちを ./tmp/ に連番で保存する
    # 全部pngに変換したい
    for i in range(len(slide_list)):
        cmd = ["sips", "-s", "format", CONVERT_IMAGE_TO, str(slide_list[i]),
               "--out", "tmp/%03d.%s" % (i, CONVERT_IMAGE_TO)]
        subprocess.call(cmd)

    # tmp のファイルたちのサイズを統一する　1920×1080
    subprocess.call(CMD_RESAMPLE_HEIGHT, shell=True)
    subprocess.call(CMD_CROP_FULLHD, shell=True)

    try:
        subprocess.call(CMD_MAKE_SLIDE_SHOW)
    except subprocess.STD_ERROR_HANDLE as e:
        print(e)

    # 終了処理
    subprocess.call('rm ./tmp/*', shell=True)
    subprocess.call('rm list.txt', shell=True)


if __name__ == "__main__":
    main()
