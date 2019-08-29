from PIL import Image, ImageDraw, ImageFont


def main():
    make_title_image("AT2019_A001", "hogehoge", "sato\nsuzuki\ntakahashi",
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

    # 余白の量
    margin_w = int(width / 10)
    margin_h = int(height / 10)

    # フォントサイズ
    number_fsize = 24
    title_fsize = 200
    member_fsize = 24

    # 各文字の位置
    number_pos = (margin_w, height / 4)
    title_pos = (margin_w, height / 2 - title_fsize / 2)
    member_pos = (margin_w, height / 3 * 2)

    # titleの最大サイズ
    title_width = width - margin_w * 2
    title_height = height / 8
    out_title_size = (title_width + 1, title_height + 1)

    # 新規画像生成
    img = Image.new('RGB', (width, height), 'black')
    draw = ImageDraw.Draw(img)

    # number を描く
    font = ImageFont.truetype(font_file_name, number_fsize)
    draw.text(number_pos, number, fill='#FFF', font=font)
    # title を描く

    while title_width < out_title_size[0] or title_height < out_title_size[1]:
        title_fsize -= 1
        font = ImageFont.truetype(font_file_name, title_fsize)
        # font のサイズをtextsize()で取得
        out_title_size = draw.textsize(title, font=font)
    draw.text(title_pos, title, fill='#FFF', font=font)
    # member を描く
    font = ImageFont.truetype(font_file_name, member_fsize)
    draw.text(member_pos, member, fill='#FFF', font=font)

    img.show()
    print(dst_path)
    img.save(dst_path)


if __name__ == "__main__":
    main()
