import os
import tempfile
import PyPDF2
import difflib
from django.shortcuts import render
from django.http import JsonResponse

def extract_text_from_pdf(file):
    """PDFファイルからテキストを抽出する関数"""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def compare_texts(text1, text2):
    """2つのテキストを比較し、差分を取得する関数"""
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    
    # difflibを使用して差分を取得
    diff = difflib.HtmlDiff()
    diff_table = diff.make_file(lines1, lines2)
    
    return diff_table

def index(request):
    """アップロードページを表示する関数"""
    return render(request, 'upload.html')

def process_files(request):
    """アップロードされたPDFファイルを処理する関数"""
    if request.method == 'POST':
        # ファイルが提供されているか確認
        if 'file1' not in request.FILES or 'file2' not in request.FILES:
            return JsonResponse({'error': 'ファイルが提供されていません'}, status=400)
        
        file1 = request.FILES['file1']
        file2 = request.FILES['file2']
        
        # ファイルがPDFかどうかを確認
        if not file1.name.endswith('.pdf') or not file2.name.endswith('.pdf'):
            return JsonResponse({'error': 'PDFファイルのみ対応しています'}, status=400)
        
        # PDFからテキストを抽出
        text1 = extract_text_from_pdf(file1)
        text2 = extract_text_from_pdf(file2)
        
        # テキストをセッションに保存
        request.session['text1'] = text1
        request.session['text2'] = text2
        request.session['file1_name'] = file1.name
        request.session['file2_name'] = file2.name
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'POSTリクエストが必要です'}, status=405)

def show_result(request):
    """結果ページを表示する関数"""
    text1 = request.session.get('text1', '')
    text2 = request.session.get('text2', '')
    file1_name = request.session.get('file1_name', 'ファイル1')
    file2_name = request.session.get('file2_name', 'ファイル2')
    
    # テキストを行に分割
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    
    # 差分比較ロジック
    d = difflib.Differ()
    diff = list(d.compare(lines1, lines2))
    
    # 差分のリストを作成
    diff_result = []
    for line in diff:
        if line.startswith('  '):  # 変更なし
            diff_result.append({'type': 'unchanged', 'line': line[2:], 'line_orig': line[2:]})
        elif line.startswith('- '):  # 削除
            diff_result.append({'type': 'deleted', 'line': line[2:], 'line_orig': ''})
        elif line.startswith('+ '):  # 追加
            diff_result.append({'type': 'added', 'line': '', 'line_orig': line[2:]})
        elif line.startswith('? '):  # 変更のヒント (無視)
            continue
    
    context = {
        'file1_name': file1_name,
        'file2_name': file2_name,
        'diff_result': diff_result
    }
    
    return render(request, 'result.html', context)