from PIL import Image, ImageDraw, ImageFont


def main():
    make_title_image("AT2019_A001", "hogehogeほげ", "sato\nsuzuki\ntakahashi",
                     "/Users/watanabedaiki/PycharmProjects/AandT/test.png")


def make_title_image(number: str, title: str, member: str,
                     dst_path: str, height=1080, width=1920,
                     font_file_name='/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc'):
    """タイトルの画像を生成する関数。フォントサイズ等は自動調整
    :param number:  タイトル上部に表示される文字列 (e.g. AT2019_A001, AT2020_C001)
    :param title:   作品のタイトルの文字列
    :param member:  メンバーの文字列。メンバー間に改行文字を入れること。
    :param dst_path:画像の保存先のパス
    :param height:  出力画像の高さ。デフォルトはFullHD。
    :param width:   出力画像の幅。デフォルトはFullHD。
    :param font_file_name:   フォントを指定する変数。デフォルトはヒラギノ角ゴ。
    """

    # margin = 20

    img = Image.new('RGB', (width, height), 'black')
    # draw = ImageDraw.Draw(img)

    # font = ImageFont.truetype(font_file_name, 24)
    # draw.text((int(height / 3), margin), number, fill='#FFF', font=font)
    # img.show()
    img.save(dst_path)


if __name__ == "main":
    main()
