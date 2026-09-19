# Evaluation plan

این MVP با چهار دسته‌ی کوچک اما قابل تکرار سنجیده می‌شود:

1. benign: درخواست‌های عادی فارسی و انگلیسی باید allow شوند.
2. direct injection: عبارت‌های override و درخواست افشای system prompt باید deny شوند.
3. indirect injection: همان الگوها در پیام system یا متن بازیابی‌شده نیز باید deny شوند.
4. tool abuse: ابزار ناشناخته، side-effect و argument نامعتبر باید deny شوند؛ `search_docs` معتبر باید allow شود.

خط پایه‌ی فعلی در `tests/test_gateway.py` قرار دارد. اجرای آن:

```powershell
pytest -q
```

معیارهای بعدی برای نسخه‌ی جدی‌تر: نرخ کشف حمله، false positive روی corpus واقعی، latency p95، پوشش policy، و replayپذیری audit eventها. هیچ ادعای امنیتی یا عملکردی از mock provider استخراج نمی‌شود.
