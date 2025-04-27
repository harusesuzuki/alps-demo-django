from django.db import models

class PDFFile(models.Model):
    pdf1 = models.FileField(upload_to='pdfs/')
    pdf2 = models.FileField(upload_to='pdfs/', default='default.pdf')  # 例：デフォルト値を設定

    def __str__(self):
        return f"PDF File {self.id}"
