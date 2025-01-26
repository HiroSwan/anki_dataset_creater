import os
from pdf2image import convert_from_path

def pdf_to_images(pdf_path, output_dir, prefix="Q", letter="A", dpi=300):
    """
    1つのPDFを、ページごとにprefix_letter番号.png という名前で出力する。
    
    Parameters:
    -----------
    pdf_path : str
        変換するPDFファイルのパス
    output_dir : str
        画像の出力先ディレクトリ
    prefix : str
        出力ファイル名の接頭辞 ("Q" or "A" など)
    letter : str
        数字の前に付与するアルファベット（A～X）
    dpi : int
        画像化する際の解像度
    """
    # PDFをページごとにImageオブジェクトに変換
    pages = convert_from_path(pdf_path, dpi=dpi)

    # 出力先のディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)

    saved_paths = []
    total_pages = len(pages)  # 総ページ数を取得
    digits = len(str(total_pages))  # ゼロ埋めの桁数を計算

    for i, page in enumerate(pages, start=1):
        # ファイル名の作成 (例: Q_A01.png, A_A01.png)
        filename = f"{prefix}_{letter}{str(i).zfill(digits)}.png"
        out_path = os.path.join(output_dir, filename)
        page.save(out_path, "PNG")
        saved_paths.append(out_path)
    return saved_paths


if __name__ == "__main__":
    # A～X まで対応すると仮定（必要に応じて変更）
    letters = [chr(c) for c in range(ord('A'), ord('X') + 1)]
    
    # 問題PDFがあるフォルダ
    question_dir = "pdf/q"
    # 解答PDFがあるフォルダ
    answer_dir = "pdf/a"
    # 画像の出力先ベース
    base_img_dir = "img"

    for letter in letters:
        # 変換対象のPDF
        q_pdf_path = os.path.join(question_dir, f"{letter}.pdf")  # 例: pdf/q/A.pdf
        a_pdf_path = os.path.join(answer_dir, f"{letter}.pdf")    # 例: pdf/a/A.pdf
        
        # 出力先: img/A/ (フォルダ)
        output_dir_for_letter = os.path.join(base_img_dir, letter)
        
        # 1) 問題PDF → Q_Axx.png
        if os.path.exists(q_pdf_path):
            pdf_to_images(
                pdf_path=q_pdf_path,
                output_dir=output_dir_for_letter,
                prefix="Q",
                letter=letter,
                dpi=150
            )
        else:
            print(f"Warning: {q_pdf_path} not found.")
        
        # 2) 解答PDF → A_Axx.png
        if os.path.exists(a_pdf_path):
            pdf_to_images(
                pdf_path=a_pdf_path,
                output_dir=output_dir_for_letter,
                prefix="A",
                letter=letter,
                dpi=150
            )
        else:
            print(f"Warning: {a_pdf_path} not found.")
        
        print(f"[{letter}] Done.")