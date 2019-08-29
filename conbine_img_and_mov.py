import pathlib
import os
import subprocess
import sys

HOME = "./"

"""
作品は%03dの形式でナンバリングされていて、タイトルと同じ番号になっている前提
まあソートできればなんでも良い。
"""
TITLE_PATH = "title/AT2019_B*"
WORKS_PATH = "works/AT2019_B*"

# タイトルを表示する時間
SlIDE_TIME = 5

# 一時的に作成したファイルを削除するか？
REMOVE_TMP = False

MOVIE_TYPE = [".mp4", ".wmv", ".flv", ".mov", ".MP4", ".WMV", ".FLV", ".MOV"]
IMAGE_TYPE = [".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG"]
CONVERT_TO = ".mp4"

"""
subprocess.call()でshell=Trueにするとシェルインジェクション的な危険が危ないので
外部入力でsubprocess.call(CMD, Shell=True)に渡さないように注意
そんな悪意のある人いないでしょ...
"""


def main():

    # init

    print("[*] Initializing...")

    # 一時ディレクトリ作成
    tmp_num = 0
    while os.path.exists("tmp%d" % tmp_num):
        tmp_num += 1
    tmp_path = "tmp%d" % tmp_num
    subprocess.call("mkdir %s" % tmp_path, shell=True)

    print("[*] Done.")

    # タイトルと作品の動画を探索
    p_title = pathlib.Path(HOME)
    title_list = sorted(list(p_title.glob(TITLE_PATH)))
    work_list = sorted(list(p_title.glob(WORKS_PATH)))
    slide_list = list()

    print("[*] Listing title and works.")
    # タイトルがあるものを全部探す
    for i in range(len(title_list)):

        # 作品がなければスキップ
        f_continue = False
        try:
            work_list[i]
        except IndexError as e:
            print("[!] ERROR:", e)
            print("[!] title_list[%d]: %s" % (i, title_list[i]))
            print("[!] too less works?")
            f_continue = True
        if f_continue:
            continue

        # タイトルも作品もある
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
    print("[*] Done.")

    play_list = list()
    for i in range(len(slide_list)):
        tmp = "\r\033[K[-] " + "%d/%s" % (i + 1, len(slide_list))
        sys.stdout.write(tmp)
        sys.stdout.flush()

        # titleは全部pngだって信じてる
        root, exe = os.path.splitext(str(slide_list[i]))

        # 画像の時
        if exe in IMAGE_TYPE:
            # 画像を5秒程度の動画に変換
            cmd = ["ffmpeg", "-loop", "1", "-y", "-i", str(slide_list[i]),
                   "-b:v", "3000k", "-c:v", "h264", "-pix_fmt", "yuv420p",
                   "-t", str(SlIDE_TIME), "-r", "30", "%s/%03d%s" % (tmp_path, i, CONVERT_TO)]
        # 動画の時
        elif exe in MOVIE_TYPE:
            # 動画はそのままmp4動画に変換してtmpに保存
            # 3分以上は -t オプションで切る
            cmd = ["ffmpeg", "-i", str(slide_list[i]), "-pix_fmt", "yuv420p",
                   "-t", "00:03:00", "-r", "30", "%s/%03d%s" % (tmp_path, i, CONVERT_TO)]

            """
            ここで各動画の音声を抽出したい。
            audio_list.append(AUDIO_PATH)
            """

        # 拡張子がIMAGE_TYPEにもMOVIE_TYPEにもなかった時
        else:
            tmp = "[!] UNKNOWN FILE TYPE: slide_list[%d]:%s, exe:%s\n" % (i, slide_list[i], exe)
            sys.stdout.write(tmp)
            sys.stdout.flush()
            continue
        subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        play_list.append("file %s/%03d%s\n" % (tmp_path, i, CONVERT_TO))

    tmp = "\r\033[K[*] finished to convert to mp4\n"
    sys.stdout.write(tmp)
    sys.stdout.flush()

    """
    ここで音声を一つに結合したい。
    SLIDE_TIME秒の無音 + 動画1の音 + SLIDE_TIME秒の無音 + 動画2の音　+ ... + 動画len(audio_list)の音
    """

    with open("list.txt", mode='w') as f:
        f.writelines(play_list)

    print("[*] Combining movies.")
    # list.txtに記入された動画を繋げる
    # 音はない。
    cmd = "ffmpeg -y -f concat -i list.txt -pix_fmt yuv420p -c copy -r 30 outputB.mp4"
    subprocess.call(cmd, shell=True)
    print("[*] Done.")

    """
    一つにした音声と動画を結合させる。
    """

    if REMOVE_TMP:
        print("[*] Remove %s" % tmp_path)
        subprocess.call("rm %s/*" % tmp_path, shell=True)
        subprocess.call("rmdir %s" % tmp_path, shell=True)


if __name__ == "__main__":
    main()
