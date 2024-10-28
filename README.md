# LEX Project (EnhancedUXI)
# پروژه لکس

 Overview | نمای کلی 🔍

This project implements a Bash command parser and analyzer using LEX for lexical analysis. The application provides a graphical interface for analyzing shell scripts and displaying detailed token breakdowns. The system features a modern GUI with theme selection, real-time token analysis, and comprehensive command recognition capabilities. It supports advanced syntax validation, detailed error reporting, and handles various token types including commands, operators, variables, and special characters. The project is designed to work seamlessly with both English and Persian text through bidirectional text support, making it a versatile tool for shell script analysis and development.

این پروژه یک تجزیه‌کننده و تحلیل‌گر دستورات Bash را با استفاده از LEX برای تحلیل لغوی پیاده‌سازی می‌کند. برنامه یک رابط گرافیکی برای تحلیل اسکریپت‌های شل و نمایش جزئیات توکن‌ها ارائه می‌دهد. سیستم دارای رابط کاربری مدرن با قابلیت انتخاب تم، تحلیل توکن در زمان واقعی و قابلیت‌های جامع تشخیص دستورات است.

<details>
<summary> Project Structure | ساختار پروژه 📁</summary>

| File | Description | توضیحات |
|------|-------------|----------|
| `main.py` 🚀 | Entry point with theme management | نقطه ورود با مدیریت تم |
| `gui.py` 🎨 | GUI implementation with ttkbootstrap | پیاده‌سازی رابط گرافیکی |
| `tokenizer.py` 🔍 | Token processing and LEX integration | پردازش توکن و یکپارچه‌سازی LEX |
| `tokenizer.lex` 📝 | LEX rules for Bash command tokenization | قوانین LEX برای توکن‌سازی دستورات |
| `INPUT.sh` 📄 | Sample shell script for testing | اسکریپت شل نمونه برای تست |
| `INPUT.txt` 📑 | Alternative input file format | فرمت فایل ورودی جایگزین |
| `documentation.pdf` 📚 | Detailed project documentation | مستندات کامل پروژه |

</details>

<details>
<summary> Features | ویژگی‌ها ✨</summary>

1. **Modern GUI Interface | رابط کاربری مدرن** 🎯
    - Theme selection with multiple styles | انتخاب تم با سبک‌های متنوع
    - Code editor with syntax highlighting | ویرایشگر کد با هایلایت سینتکس
    - Real-time token analysis | تحلیل توکن در زمان واقعی
    - Bidirectional text support | پشتیبانی متن دو جهته

2. **Token Analysis | تحلیل توکن** 🔎
    - Command recognition | تشخیص دستورات
    - Syntax validation | اعتبارسنجی سینتکس
    - Error detection | تشخیص خطا
    - Token statistics | آمار توکن‌ها

</details>

<details>
<summary> Usage Instructions | دستورالعمل استفاده 📋</summary>

1. **Setup Environment | راه‌اندازی محیط** 🛠️

# Install system packages | نصب پکیج‌های سیستمی
sudo pacman -S flex gcc python python-pip

# Install Python dependencies | نصب وابستگی‌های پایتون
pip install ttkbootstrap arabic-reshaper python-bidi


2. **Compile LEX | کامپایل LEX** ⚙️

flex tokenizer.lex
gcc lex.yy.c -o a.out


3. **Run Application | اجرای برنامه** 🚀

python main.py

</details>

<details>
<summary> System Requirements | نیازمندی‌های سیستم 💻</summary>

- **OS**: Arch Linux | سیستم‌عامل: آرچ لینوکس
- **Python**: 3.8+ | پایتون: نسخه ۳.۸ به بالا
- **Packages | پکیج‌ها**:
  - flex ⚡
  - gcc 🔧
  - python-pip 📦
  - ttkbootstrap 🎨
  - arabic-reshaper 🔤
  - python-bidi ↔️

</details>

<details>
<summary> Token Types | انواع توکن 🏷️</summary>

- **Commands | دستورات** 💻
- **Keywords | کلمات کلیدی** 🔑
- **Operators | عملگرها** ⚡
- **Variables | متغیرها** 📊
- **Literals | مقادیر ثابت** 📝
- **Delimiters | جداکننده‌ها** 🔲
- **Comments | توضیحات** 💭

</details>

<details>
<summary> Analysis Features | ویژگی‌های تحلیل 📊</summary>

- Real-time syntax checking | بررسی سینتکس در لحظه 🔄
- Error detection | تشخیص خطا ⚠️
- Token frequency analysis | تحلیل فراوانی توکن 📈
- Color-coded visualization | نمایش رنگی 🎨
- Performance statistics | آمار عملکرد 📊

</details>
