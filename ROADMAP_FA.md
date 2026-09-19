# Secure AI Gateway

نقشه‌ی کامل پروژه از صفر تا صد

## 1. این پروژه چیست؟

`Secure AI Gateway` یک لایه‌ی کنترل بین کاربر، مدل زبانی و ابزارهای متصل به مدل است.

وقتی یک برنامه‌ی AI مستقیماً درخواست کاربر را به مدل می‌فرستد و اجازه می‌دهد مدل ابزارهایی مثل جست‌وجو، ارسال ایمیل، خواندن فایل یا اجرای عملیات را صدا بزند، چند خطر به وجود می‌آید:

- کاربر می‌تواند مدل را فریب دهد تا دستورهای اصلی را نادیده بگیرد.
- مدل ممکن است ابزار اشتباه یا خطرناک را صدا بزند.
- اطلاعات حساس ممکن است وارد log یا پاسخ مدل شود.
- یک کاربر می‌تواند با درخواست‌های زیاد هزینه یا منابع سیستم را مصرف کند.
- در زمان بررسی حادثه، ممکن است ندانیم چه اتفاقی افتاده است.

Gateway قبل از رسیدن درخواست به مدل یا ابزار، آن را بررسی می‌کند و تصمیم می‌گیرد:

```text
درخواست کاربر
      ↓
اعتبارسنجی اندازه و ساختار
      ↓
بررسی prompt injection و محتوای خطرناک
      ↓
بررسی مجوز ابزار
      ↓
اعمال rate limit
      ↓
ثبت audit بدون ذخیره‌ی متن خام
      ↓
ارسال کنترل‌شده به مدل یا ابزار
```

نسخه‌ی فعلی یک MVP آموزشی و قابل توسعه است. هدف آن اثبات این است که می‌توان سیاست‌های امنیتی را به‌صورت روشن، تست‌پذیر و قابل مشاهده در اطراف یک برنامه‌ی LLM قرار داد.

## 2. هدف اصلی

هدف پروژه این نیست که ادعا کند یک سیستم با چند regex کاملاً امن شده است. هدف واقعی این است که یک پایه‌ی تمیز برای یادگیری و توسعه‌ی امنیت AI داشته باشیم و بتوانیم بعداً آن را به یک برنامه‌ی واقعی LLM یا agent متصل کنیم.

در پایان مسیر، پروژه باید بتواند:

1. درخواست عادی را عبور دهد.
2. درخواست مشکوک به prompt injection را متوقف کند.
3. ابزارهای ناشناخته یا خطرناک را رد کند.
4. برای ابزارهای مجاز، argument را اعتبارسنجی کند.
5. تعداد درخواست‌ها را محدود کند.
6. تصمیم‌های امنیتی را بدون ذخیره‌ی متن حساس ثبت کند.
7. با یک provider واقعی OpenAI-compatible قابل اتصال باشد.
8. در Docker اجرا شود.
9. در CI تست شود.
10. برای یک تیم کوچک قابل توضیح و قابل استفاده باشد.

## 3. وضعیت فعلی

نسخه‌ی فعلی در حد MVP قرار دارد.

### امکانات موجود

- FastAPI
- endpoint به نام `POST /v1/chat`
- endpoint سلامت به نام `GET /healthz`
- provider محلی و deterministic بدون نیاز به API key
- تشخیص چند الگوی پایه‌ی prompt injection
- allowlist ابزارها
- ابزار read-only نمونه به نام `search_docs`
- رد کردن ابزارهای ناشناخته یا side-effect مثل `send_email`
- rate limiting در سطح client
- audit log با hash و طول متن به‌جای ذخیره‌ی prompt خام
- تست‌های pytest
- Dockerfile
- GitHub Actions
- مستندات threat model و evaluation

### چیزی که هنوز وجود ندارد

- اتصال واقعی به مدل زبانی
- authentication و authorization واقعی کاربران
- ذخیره‌ی پایدار audit log
- اجرای sandbox شده‌ی ابزارها
- policy engine قابل تنظیم از فایل یا database
- تست adversarial بزرگ و چندزبانه
- deployment واقعی
- داشبورد مشاهده‌ی رخدادها
- ارزیابی هزینه، latency و کیفیت provider واقعی

این موارد نقص پنهان نیستند؛ عمداً در مراحل بعدی قرار گرفته‌اند تا پروژه قابل فهم و قابل تست بماند.

## 4. ساختار فعلی پروژه

```text
secure-ai-gateway/
├── app/
│   ├── audit.py       # ثبت رخدادهای امنیتی بدون متن خام
│   ├── config.py      # تنظیمات محیطی و محدودیت‌ها
│   ├── main.py        # FastAPI و pipeline اصلی gateway
│   ├── models.py      # مدل‌های ورودی و خروجی API
│   ├── policy.py      # allowlist و اعتبارسنجی ابزارها
│   ├── provider.py    # provider محلی برای اجرای بدون credential
│   └── security.py    # scan متن و rate limiter
├── tests/
│   └── test_gateway.py
├── .github/workflows/ci.yml
├── Dockerfile
├── README.md
├── THREAT_MODEL.md
├── EVALUATION.md
├── ROADMAP_FA.md
├── pyproject.toml
├── requirements.txt
└── requirements-dev.txt
```

## 5. اجرای پروژه از صفر

مسیر اصلی پروژه:

```text
C:\Users\Reza\Desktop\Secure AI Gateway
```

در PowerShell:

```powershell
cd 'C:\Users\Reza\Desktop\Secure AI Gateway'
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

اجرای API:

```powershell
python -m uvicorn app.main:app --reload
```

بعد این آدرس‌ها را باز کن:

- مستندات API: `http://127.0.0.1:8000/docs`
- سلامت سرویس: `http://127.0.0.1:8000/healthz`

اجرای تست‌ها:

```powershell
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
```

## 6. نسخه‌ی صفر تا یک: تثبیت MVP

هدف این مرحله این است که رفتار فعلی دقیق، قابل تکرار و قابل فهم باشد.

### کارها

- اضافه کردن test case برای درخواست عادی فارسی و انگلیسی
- اضافه کردن test case برای prompt injection در پیام system
- اضافه کردن test case برای injection در متن بازیابی‌شده
- تست اعتبارسنجی argument ابزار
- تست چند client مستقل برای rate limit
- اضافه کردن response code ثابت و مستند
- افزودن مثال‌های curl و PowerShell به README
- بررسی کامل `ruff` و `pytest`

### معیار پایان

- همه‌ی تست‌ها سبز باشند.
- هر deny دلیل و code مشخص داشته باشد.
- متن خام کاربر در audit ذخیره نشود.
- رفتار endpoint در README قابل تکرار باشد.

## 7. نسخه‌ی یک تا دو: policy واقعی‌تر

در این مرحله regexها فقط اولین خط دفاعی می‌مانند و سیاست‌ها ساختارمندتر می‌شوند.

### کارها

- تعریف policy با مدل مشخص:

```json
{
  "tool": "search_docs",
  "access": "read",
  "max_query_chars": 500,
  "requires_confirmation": false
}
```

- جدا کردن policy تصمیم‌گیری از FastAPI
- تعریف کدهای خطای ثابت
- اضافه کردن deny-by-default
- اضافه کردن محدودیت اندازه برای پیام‌ها و argumentها
- اضافه کردن مفهوم سطح ریسک ابزار
- اضافه کردن policy برای ابزارهای نیازمند تأیید کاربر

### معیار پایان

- اضافه کردن ابزار جدید بدون دست‌زدن به endpoint اصلی ممکن باشد.
- هر ابزار قبل از اجرا policy مشخص داشته باشد.
- ابزار ناشناخته به‌صورت پیش‌فرض رد شود.
- side-effect بدون confirmation قابل اجرا نباشد.

## 8. نسخه‌ی دو تا سه: اتصال provider واقعی

در این مرحله provider محلی حفظ می‌شود و یک adapter اختیاری برای providerهای OpenAI-compatible اضافه می‌شود.

### طراحی پیشنهادی

```text
Gateway
  ├── Security pipeline
  ├── Policy engine
  ├── Audit log
  └── Provider interface
        ├── MockProvider
        └── OpenAICompatibleProvider
```

### قواعد مهم

- API key فقط از environment خوانده شود.
- key هرگز در response یا audit نوشته نشود.
- provider مستقیماً اجازه‌ی اجرای ابزار نداشته باشد.
- تمام tool callها دوباره از policy عبور کنند.
- در خطای provider، پاسخ امن و قابل توضیح برگردد.
- تست‌ها با mock provider بدون network اجرا شوند.

### معیار پایان

- اجرای local بدون credential همچنان ممکن باشد.
- provider واقعی فقط یک adapter قابل تعویض باشد.
- تست‌های CI به سرویس خارجی وابسته نباشند.
- خطای timeout، rate limit provider و پاسخ نامعتبر مدیریت شود.

## 9. نسخه‌ی سه تا چهار: ابزار واقعی اما محدود

در این مرحله می‌توان یک ابزار واقعی read-only اضافه کرد؛ مثلاً جست‌وجو در اسناد محلی.

### ابزار اول پیشنهادی

```text
search_documents(query)
```

این ابزار باید:

- فقط در یک directory مشخص جست‌وجو کند.
- path traversal را رد کند.
- حجم خروجی را محدود کند.
- فقط متن لازم را برگرداند.
- نتیجه را با source id و metadata همراه کند.
- امکان اجرای shell نداشته باشد.

### ابزارهایی که فعلاً نباید اضافه شوند

- اجرای shell
- ارسال ایمیل
- تغییر database production
- حذف فایل
- انتقال پول
- دسترسی unrestricted به filesystem

این ابزارها برای اثبات امنیت لازم نیستند و ریسک را بی‌دلیل بالا می‌برند.

## 10. نسخه‌ی چهار تا پنج: audit و مشاهده‌پذیری

audit فعلی حافظه‌ای است. برای استفاده‌ی واقعی باید رخدادها قابل جست‌وجو و قابل نگهداری باشند.

### اطلاعات مناسب برای audit

- request id
- client id یا user id ناشناس‌شده
- زمان
- تصمیم allow یا deny
- دلیل تصمیم
- نام ابزار
- طول ورودی
- hash ورودی
- زمان پاسخ
- provider
- status code

### اطلاعاتی که نباید ذخیره شوند

- متن خام prompt حساس
- API key
- password
- token
- فایل خصوصی
- محتوای کامل سند کاربر

### گزینه‌ی فنی

برای نسخه‌ی کوچک SQLite کافی است. برای چند instance می‌توان بعداً PostgreSQL یا یک log store جدا اضافه کرد.

## 11. نسخه‌ی پنج تا شش: ارزیابی امنیتی

امنیت را با چند مثال دستی نمی‌توان اثبات کرد. باید یک corpus قابل تکرار داشته باشیم.

### دسته‌های corpus

1. درخواست عادی فارسی
2. درخواست عادی انگلیسی
3. نادیده‌گرفتن دستور قبلی
4. درخواست افشای system prompt
5. درخواست ارسال secret
6. injection در متن retrieved document
7. ابزار ناشناخته
8. argument نامعتبر
9. query بیش از حد طولانی
10. تلاش برای path traversal

### معیارها

- attack detection rate
- false positive روی درخواست سالم
- tool deny rate
- policy coverage
- p95 latency
- تعداد رخدادهای ثبت‌شده
- reproducibility اجرای تست

### نکته‌ی مهم

اگر یک حمله رد شود، نتیجه فقط درباره‌ی همان test case است. نباید از آن نتیجه ادعای «امن بودن کامل» ساخت.

## 12. نسخه‌ی شش تا هفت: داشبورد کوچک

یک dashboard سبک برای نمایش رخدادها اضافه می‌شود.

### صفحه‌های پیشنهادی

- تعداد درخواست‌های allow و deny
- دلایل deny
- ابزارهای درخواست‌شده
- روند rate limit
- آخرین رخدادها
- فیلتر بر اساس بازه‌ی زمانی

این dashboard برای نمایش نمونه‌کار مفید است، اما نباید به‌خاطر آن معماری را پیچیده کنیم. ابتدا API و audit باید درست باشند.

## 13. نسخه‌ی هفت تا هشت: Docker و deployment

### Docker

```powershell
docker build -t secure-ai-gateway .
docker run --rm -p 8000:8000 secure-ai-gateway
```

### قبل از deployment باید بررسی شود

- health check
- environment variables
- عدم وجود secret در image
- اجرای migration در صورت داشتن database
- log بدون اطلاعات حساس
- محدودیت request body
- timeout
- shutdown صحیح

### deployment نمونه

برای دمو می‌توان از یک سرویس ساده‌ی cloud یا VM کوچک استفاده کرد. deployment production زمانی انجام می‌شود که provider واقعی و authentication اضافه شده باشند.

## 14. نسخه‌ی هشت تا نه: آماده‌سازی برای مشتری

در این مرحله پروژه باید از «نمونه‌کد» به «دموی قابل ارائه» تبدیل شود.

### خروجی‌هایی که باید آماده شوند

- یک ویدئوی دو دقیقه‌ای
- یک architecture diagram
- یک threat model خلاصه
- یک گزارش test result
- یک demo URL یا اجرای Docker
- یک case study کوتاه
- یک صفحه‌ی محدودیت‌ها

### سناریوی demo

```text
1. درخواست عادی ارسال می‌شود و پاسخ می‌گیرد.
2. prompt injection ارسال می‌شود و deny می‌شود.
3. search_docs مجاز اجرا می‌شود.
4. send_email رد می‌شود.
5. audit نشان می‌دهد چه تصمیمی گرفته شده است.
```

## 15. نسخه‌ی نه تا ده: استفاده‌ی واقعی

برای پیدا کردن استفاده‌کننده، باید پروژه را به یک مسئله‌ی مشخص وصل کنیم.

نمونه‌ی target:

- تیمی که chatbot داخلی دارد.
- شرکتی که RAG روی اسناد خصوصی ساخته است.
- استارتاپی که agent با tool calling دارد.
- آژانسی که برای چند مشتری اپلیکیشن LLM می‌سازد.

پیشنهاد خدماتی ساده:

> من مسیر ورودی و tool calling برنامه‌ی LLM شما را بررسی می‌کنم، چند سناریوی prompt injection و tool abuse را اجرا می‌کنم و یک لایه‌ی policy و audit قابل اجرا با Docker تحویل می‌دهم.

نسخه‌ی اول خدمات باید محدود باشد:

- یک application
- یک یا دو provider
- حداکثر چند ابزار
- گزارش کوتاه
- زمان و هزینه‌ی مشخص

## 16. مهارت‌هایی که در طول پروژه یاد می‌گیریم

قرار نیست چند ماه جداگانه درس بخوانیم و بعد پروژه را شروع کنیم.

| نیاز پروژه | مهارت هم‌زمان |
| --- | --- |
| ساخت endpoint | Python و FastAPI |
| ورودی امن | Pydantic و API validation |
| کنترل ابزار | authorization و policy design |
| ثبت رخداد | logging و privacy |
| تست حمله | pytest و threat modeling |
| اجرای سرویس | Docker و Linux |
| provider واقعی | API integration و secret handling |
| اجرای خودکار | GitHub Actions و CI |
| سنجش کیفیت | evaluation و metrics |
| ارائه به مشتری | documentation و case study |

## 17. قانون‌های پروژه

- هیچ ادعایی بدون test یا artifact نوشته نشود.
- هیچ ابزار خطرناکی فقط برای جذاب‌تر شدن demo اضافه نشود.
- credential داخل Git commit نشود.
- provider واقعی نباید policy را دور بزند.
- هر deny باید دلیل قابل فهم داشته باشد.
- هر قابلیت جدید باید test و documentation داشته باشد.
- اول مسئله و معیار موفقیت مشخص شود، بعد کد نوشته شود.
- اگر یک قابلیت برای مشتری واقعی ارزش ندارد، وارد MVP نشود.

## 18. تعریف نسخه‌ی نهایی قابل ارائه

نسخه‌ی نهایی قابل ارائه زمانی آماده است که:

- کاربر بتواند با یک دستور آن را اجرا کند.
- API سالم و مستند باشد.
- حداقل یک provider واقعی و mock provider داشته باشد.
- authentication پایه وجود داشته باشد.
- ابزارها deny-by-default باشند.
- audit پایدار و بدون داده‌ی حساس باشد.
- تست‌های امنیتی و functional در CI سبز باشند.
- Docker image ساخته و اجرا شود.
- یک demo قابل مشاهده وجود داشته باشد.
- threat model و محدودیت‌ها نوشته شده باشند.
- یک فرد بیرونی بتواند بدون توضیح شفاهی پروژه را اجرا کند.

## 19. وضعیت فعلی نسبت به مسیر صفر تا صد

```text
MVP پایه                         ███░░░░░░░  حدود 25٪
policy ساختاریافته               ░░░░░░░░░░  شروع نشده
provider واقعی                   ░░░░░░░░░░  شروع نشده
ابزار واقعی read-only            ░░░░░░░░░░  شروع نشده
audit پایدار                     ░░░░░░░░░░  شروع نشده
ارزیابی adversarial              ██░░░░░░░░  طرح اولیه
dashboard                        ░░░░░░░░░░  شروع نشده
deployment                       ░░░░░░░░░░  Docker آماده، اجرا نیازمند بررسی
case study مشتری                 ░░░░░░░░░░  شروع نشده
```

این درصدها کیفیت کلی رزومه نیستند؛ فقط میزان تکمیل همین پروژه را نشان می‌دهند.

## 20. تصمیم فعلی

این پروژه فعلاً یک پروژه‌ی پشتیبان برای نشان دادن علاقه و توانایی اولیه در AI security است. پروژه‌های اصلی رزومه همچنان این‌ها هستند:

1. PromoGuard برای محصول و بازار کار.
2. Calibrated Predictive Reliability برای عمق علمی و آماری.
3. AURALIS برای full-stack AI product engineering.

Secure AI Gateway زمانی به رتبه‌ی بالاتر می‌رود که یک مصرف‌کننده‌ی واقعی، provider واقعی، policy قابل تنظیم، ارزیابی adversarial و deployment قابل تکرار داشته باشد.

## 21. مسیر کاری از امروز

ترتیب کار پیشنهادی:

```text
پایدار کردن MVP
      ↓
policy قابل تنظیم
      ↓
provider واقعی با mock fallback
      ↓
ابزار read-only واقعی
      ↓
audit پایدار
      ↓
evaluation corpus
      ↓
Docker و deployment
      ↓
demo و case study
      ↓
پیدا کردن کاربر واقعی
```

هر مرحله باید با سه خروجی تمام شود:

- کد قابل اجرا
- test قابل تکرار
- توضیح ساده برای کاربر یا reviewer
