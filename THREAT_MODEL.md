# Threat model

## دارایی‌ها و مرز اعتماد

- ورودی کاربر، promptهای سیستم و نتیجه‌ی ابزارها دارایی حساس‌اند.
- client بیرونی غیرقابل اعتماد است؛ gateway نقطه‌ی کنترل است؛ provider و tool runner پایین‌تر از policy قرار دارند.
- audit باید برای incident response مفید باشد، بدون نگهداری متن خام prompt.

## تهدیدها و کنترل‌ها

| تهدید | کنترل MVP | محدودیت شناخته‌شده |
|---|---|---|
| prompt injection مستقیم/غیرمستقیم | scan الگوهای override/exfiltration | bypassهای زبانی و چندمرحله‌ای ممکن است |
| اجرای ابزار خطرناک | allowlist نام ابزار و اعتبارسنجی argument | tool واقعی و sandbox در این MVP وجود ندارد |
| سوءاستفاده‌ی پرتعداد | rate limit حافظه‌ای | برای چند replica باید storage توزیع‌شده استفاده شود |
| نشت متن در log | hash و اندازه به‌جای متن خام | hash برای داده‌ی کم‌entropy ممکن است قابل حدس باشد |
| نبود credential | provider deterministic محلی | کیفیت پاسخ LLM واقعی ارزیابی نمی‌شود |

## non-goals

احراز هویت production، مدیریت secret، اجرای shell، sandbox کانتینری ابزارها، تضمین کامل در برابر prompt injection و claims مربوط به کیفیت یا throughput خارج از scope هستند.
