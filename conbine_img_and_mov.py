import pathlib
import os
import subprocess
import sys

HOME = "./"
TITLE_PATH = "title/AT2019_B*"
WORKS_PATH = "works/AT2019_B*"

MOVIE_TYPE = [".mp4", ".wmv", ".flv", ".mov", ".MP4", ".WMV", ".FLV", ".MOV"]
IMAGE_TYPE = [".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG"]
CONVERT_TO = ".mp4"


def main():

    # init
    subprocess.call("rm tmp/*", shell=True)

    # タイトルと作品の動画を探索
    p_title = pathlib.Path(HOME)
    title_list = sorted(list(p_title.glob(TITLE_PATH)))
    work_list = sorted(list(p_title.glob(WORKS_PATH)))
    slide_list = list()

    # タイトルがあるものを全部探す
    for i in range(len(title_list)):
        # 作品がなければスキップ
        exists = False
        try:
            exists = os.path.exists(str(work_list[i]))
        except IndexError as e:
            print("[!] ERROR:", e)
            print("[!] title_list[%d]: %s" % (i, title_list[i]))
        if not exists:
            print("[!] too less works? or too many titles?")
            continue

        # タイトルも作品もある時
        slide_list.append(title_list[i])
        # work_listがディレクトリの時
        # ディレクトリの中にさらにディレクトリがあっても探索していない
        if os.path.isdir(str(work_list[i])):
            works = sorted(list(p_title.glob(str(work_list[i]) + "/*")))
            for x in works:
                root, exe = os.path.splitext(str(x))
                if exe in MOVIE_TYPE:
                    slide_list.append(x)
        # 動画が一つの時
        else:
            slide_list.append(work_list[i])

    play_list = list()
    for i in range(len(slide_list)):
        tmp = "\r\033[K[-] " + "%d/%s" % (i + 1, len(slide_list))
        sys.stdout.write(tmp)
        sys.stdout.flush()
        # 画像を動画にしてtmpに保存
        # titleは全部pngだって信じてる
        root, exe = os.path.splitext(str(slide_list[i]))
        if exe in IMAGE_TYPE:
            # 画像を5秒程度の動画に変換
            cmd = ["ffmpeg","-loop", "1", "-y", "-i", str(slide_list[i]),
                   "-b:v", "3000k", "-c:v", "h264", "-pix_fmt", "yuv420p",
                   "-t", "5", "-r", "30", "tmp/%03d%s" % (i, CONVERT_TO)]
        elif exe in MOVIE_TYPE:
            # 動画はそのままmp4動画に変換してtmpに保存
            # 3分以上は -t オプションで切る
            cmd = ["ffmpeg", "-i", str(slide_list[i]), "-pix_fmt", "yuv420p",
                   "-t", "00:03:00", "-r", "30", "tmp/%03d%s" % (i, CONVERT_TO)]
        else:
            tmp = "[!] UNKNOWN FILE TYPE: slide_list[%d]:%s, exe:%s\n" % (i, slide_list[i], exe)
            sys.stdout.write(tmp)
            sys.stdout.flush()
            continue
        subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        play_list.append("file tmp/%03d%s\n" % (i, CONVERT_TO))

    tmp = "\r\033[K[*] finished to convert to mp4\n"
    sys.stdout.write(tmp)
    sys.stdout.flush()

    with open("list.txt", mode='w') as f:
        f.writelines(play_list)

    print("[*] Combining movies.")
    cmd = "ffmpeg -y -f concat -i list.txt -pix_fmt yuv420p -r 30 outputB.mp4"
    subprocess.call(cmd, shell=True)
    print("[*] Done.")


if __name__ == "__main__":
    main()
