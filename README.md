# Secure AI Gateway

یک دروازه‌ی کوچک و قابل‌اجرا برای کنترل درخواست‌های مدل زبانی و ابزارهای متصل به آن. این پروژه برای نمونه‌کار ساخته شده، اما مسئله‌ی واقعی را هدف می‌گیرد: قبل از رسیدن درخواست به مدل یا ابزار، سیاست امنیتی باید قابل مشاهده، قابل تست و قابل audit باشد.

## قابلیت‌های MVP

- FastAPI و endpoint ‏`POST /v1/chat` با پاسخ deterministic و بدون نیاز به کلید خارجی.
- تشخیص baseline برای prompt injection و تلاش برای افشای prompt یا exfiltration.
- allowlist ابزار؛ فقط `search_docs` به‌صورت read-only مجاز است و ابزارهای side-effect مثل `send_email` رد می‌شوند.
- rate limit در سطح client با هدر `X-Client-ID`.
- audit log بدون ذخیره‌ی متن خام؛ فقط hash، طول، تصمیم و کد نتیجه ثبت می‌شود.
- تست‌های امنیتی، Docker و CI.

این regexها «اثبات امنیت» نیستند؛ یک baseline شفاف و قابل توسعه‌اند. در محصول واقعی باید authentication، storage پایدار audit، policy engine و ارزیابی adversarial مستقل اضافه شود.

## اجرا

در PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

سپس `http://127.0.0.1:8000/docs` را باز کنید.

درخواست مجاز:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/v1/chat -Method Post -ContentType 'application/json' -Body '{"messages":[{"role":"user","content":"Summarize this policy."}]}'
```

درخواست ابزار مجاز:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/v1/chat -Method Post -ContentType 'application/json' -Body '{"messages":[{"role":"user","content":"Find the policy."}],"tool":{"name":"search_docs","arguments":{"query":"policy"}}}'
```

## بررسی کیفیت

```powershell
ruff check .
ruff format --check .
pytest -q
docker build -t secure-ai-gateway .
```

## مرزهای امنیتی

مسیر اعتماد در [THREAT_MODEL.md](THREAT_MODEL.md) و سناریوهای ارزیابی در [EVALUATION.md](EVALUATION.md) آمده است. این مثال عمداً provider محلی دارد تا بدون credentials اجرا شود. جایگزینی provider باید پشت همین policy boundary انجام شود؛ هرگز نباید مدل مستقیماً ابزار دلخواه را اجرا کند.

نقشه‌ی کامل توسعه از MVP فعلی تا نسخه‌ی قابل ارائه به مشتری در [ROADMAP_FA.md](ROADMAP_FA.md) نوشته شده است.

نسخه‌ی فعلی فقط server-side Node/Python-style deployment را نمایش می‌دهد و برای browser یا Edge runtime ادعای پشتیبانی ندارد. این پروژه یک نمونه‌ی آموزشی/portfolio است، نه محصول امنیتی آماده‌ی production.
