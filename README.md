# مجموعهٔ بازِ پرامپت‌های ارزیابی فارسی

این مخزن یک مجموعهٔ کوچک، شفاف و قابل‌گسترش از سناریوهای فارسی برای **ارزیابی کیفی سامانه‌های هوش مصنوعی** است. هدف آن کمک به بازبین انسانی برای بررسی ویژگی‌هایی مانند پیروی از دستور، دقت زبانی، توجه به ابهام، ایمنی و حفظ حریم خصوصی است؛ نه اعلام رتبه‌بندی یا نتیجهٔ علمی دربارهٔ هیچ مدل یا شرکت.

پرامپت‌ها پاسخ نمونه، «پاسخ درست» یا امتیاز مدل‌ها را در خود ندارند. هر رکورد فقط ورودی، زمینهٔ لازم، معیارهای مورد انتظار و مواردی را که بازبین باید مراقبشان باشد مشخص می‌کند. بنابراین خروجی هر سامانه باید جداگانه و با قضاوت انسانی بررسی شود.

**نسخهٔ وب:** [sharif-gpt.github.io/persian-ai-evaluation-prompts](https://sharif-gpt.github.io/persian-ai-evaluation-prompts/)

## چرا این مجموعه؟

ارزیابی فارسی فقط ترجمهٔ آزمون‌های انگلیسی نیست. جهت نوشتار راست‌به‌چپ، اعداد فارسی و لاتین، تقویم شمسی، لحن رسمی و محاوره‌ای، ابهام‌های رایج و بافت‌های بومی می‌توانند کیفیت پاسخ را تغییر دهند. این مجموعه تلاش می‌کند نمونه‌هایی عملی از همین موقعیت‌ها ارائه کند.

برای مطالعهٔ راهنماهای فارسی دربارهٔ انتخاب و مقایسهٔ ابزارهای هوش مصنوعی می‌توانید به [SharifGPT](https://sharifgpt.com/) سر بزنید. این مخزن مستقل است و هیچ وابستگی، تأیید یا نمایندگی از سوی سازندگان مدل‌ها، فروشندگان نرم‌افزار یا دانشگاه صنعتی شریف را ادعا نمی‌کند.

## محتوای مخزن

```text
.
├── data/
│   └── prompts.fa.jsonl       # سناریوهای ارزیابی، یک شیء JSON در هر خط
├── schema/
│   └── prompt.schema.json     # قرارداد ساختاری هر رکورد
├── scripts/
│   └── validate.py            # اعتبارسنج سبک با کتابخانهٔ استاندارد پایتون
├── tests/
│   └── test_validate.py       # آزمون‌های واحد اعتبارسنج
├── docs/
│   ├── index.html             # وب‌سایت فارسی GitHub Pages
│   └── styles.css
├── METHODOLOGY.md             # روش اجرا، امتیازدهی و گزارش
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── LICENSE                    # CC BY 4.0
```

## شروع سریع

پایتون ۳٫۱۰ یا جدیدتر کافی است و وابستگی بیرونی لازم نیست:

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

اعتبارسنج موارد زیر را بررسی می‌کند:

- JSON معتبر در هر خط و انطباق با قرارداد داده؛
- یکتایی شناسه‌ها و وجود دسته‌ها و ابعاد ارزیابی شناخته‌شده؛
- نبود پاسخ مدل، نمره، رتبه‌بندی یا نتیجهٔ ادعایی در رکوردها؛
- وجود حداقل اطلاعات لازم برای بازبینی انسانی.

## نمونهٔ استفاده

1. نسخهٔ مدل، تنظیمات تولید، زمان اجرا و متن دقیق پرامپت را ثبت کنید.
2. هر پرامپت را در یک نشست تازه اجرا کنید تا اثر تاریخچه کاهش یابد.
3. خروجی خام را بدون ویرایش نگه دارید.
4. دست‌کم دو بازبین فارسی‌زبان، خروجی را مطابق `METHODOLOGY.md` مستقل ارزیابی کنند.
5. اختلاف‌ها را ثبت و با گفت‌وگوی مستند حل کنید؛ امتیازها را بدون زمینه به رتبه‌بندی عمومی تبدیل نکنید.

## محدودیت‌ها

- این مجموعه نمونه‌گیری محدود و هدفمند است و نمایندهٔ همهٔ گویش‌ها، حوزه‌ها یا کاربران فارسی‌زبان نیست.
- معیارها برای بازبینی کیفی طراحی شده‌اند؛ اعتبار روان‌سنجی یا آماری ادعا نمی‌شود.
- برخی سناریوها به اطلاعات روز یا تخصص حرفه‌ای وابسته‌اند. در این موارد، هدف سنجش رفتار محتاطانه و درخواست منبع است، نه تأیید محتوای تخصصی.
- انتشار نتایج بدون ثبت تنظیمات، تاریخ و فرایند بازبینی می‌تواند گمراه‌کننده باشد.

## مشارکت و مجوز

پیشنهاد پرامپت جدید خوش‌آمد است؛ لطفاً ابتدا [راهنمای مشارکت](CONTRIBUTING.md) و [آیین‌نامهٔ رفتاری](CODE_OF_CONDUCT.md) را بخوانید. داده و مستندات این مخزن تحت مجوز [CC BY 4.0](LICENSE) منتشر می‌شوند. در بازنشر، نام مخزن، پیوند منبع، مجوز و تغییرات خود را ذکر کنید.

---

## English summary

This repository is a compact, transparent set of Persian-language scenarios for qualitative evaluation of AI systems. Each JSONL record contains a prompt, required context, evaluation dimensions, review guidance, and risk notes—never model answers, claimed results, or rankings.

The collection is intended for reproducible human review of instruction following, Persian language quality, ambiguity handling, safety, privacy, and related behaviors. It is not a scientific benchmark and makes no claims about model performance. See `METHODOLOGY.md` for the recommended procedure and reporting requirements.

The repository is independent and is not affiliated with or endorsed by any model provider, software vendor, or Sharif University of Technology.
