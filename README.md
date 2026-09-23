# LLM Eval Kit

A small, deterministic, offline Python toolkit for regression-testing LLM outputs with reusable JSON test cases.

> **EN** below · [العربية](#العربية)

## Overview

LLM outputs change as prompts, models, or application code evolve. LLM Eval Kit provides a deliberately simple evaluation layer for assertions that should remain stable: exact normalized text, required phrases, forbidden phrases, regular expressions, and maximum output length. It evaluates already-produced text; it does **not** call an LLM provider.

## Why it exists

Model-based judges can be useful, but many acceptance rules do not need another model. Deterministic checks are fast, reproducible, inexpensive, easy to review in Git, and suitable for CI. This project gives those checks a consistent file format, Python API, report format, and exit-code contract.

## Features

- Exact matching with case/whitespace normalization.
- Multiple required (`contains`) and forbidden (`excludes`) phrases.
- Python regular-expression assertions and maximum character length.
- Per-case score plus suite pass/fail summary.
- UTF-8 and Arabic text support.
- JSON reports suitable for CI artifacts and downstream tools.
- Validation command that catches malformed suites, duplicate IDs, invalid regexes, and missing assertions.
- CLI and importable Python API; no runtime dependencies.
- Offline by design: no provider calls, credentials, telemetry, or evaluated-code execution.
- Exit codes: `0` all pass, `1` assertions fail, `2` invalid input/configuration.

## Preview

```text
$ llm-eval run examples/basic.json
LLM Eval Kit — 2/2 passed (100%)
PASS concise-answer score=100%
PASS arabic-answer score=100%
```

This is a CLI project, so screenshots are not required. A terminal screenshot of the command above is appropriate if a visual preview is desired later.

## Requirements & installation

- Python 3.10+

```bash
git clone https://github.com/rad03i2/llm-eval-kit.git
cd llm-eval-kit
python -m pip install -e .
```

For development:

```bash
python -m pip install -e . pytest
```

## Usage

Validate a suite without scoring it:

```bash
llm-eval validate examples/basic.json
```

Run it:

```bash
llm-eval run examples/basic.json
llm-eval run examples/basic.json --json
llm-eval run examples/basic.json --output reports/latest.json
```

Module execution also works:

```bash
python -m llm_eval_kit run examples/basic.json
```

### Evaluation format

```json
{
  "cases": [
    {
      "id": "answer-1",
      "output": "Paris is the capital of France.",
      "contains": ["Paris", "France"],
      "excludes": ["London"],
      "regex": ["capital\\s+of"],
      "max_length": 80
    }
  ]
}
```

`expected` performs normalized exact matching. `contains` and `excludes` are case-insensitive and whitespace-normalized. `regex` uses Python's regular-expression engine against the original output. `max_length` counts Python characters. A case must have a non-empty unique `id`, string `output`, and at least one assertion.

### Python API

```python
from llm_eval_kit import Case, evaluate

result = evaluate(Case("greeting", "Hello world", contains=("hello",)))
print(result.passed, result.score)
```

## Configuration

There are no environment variables, API keys, or hidden configuration files. The JSON evaluation suite is the configuration. This keeps runs portable and reviewable.

## Project structure

```text
src/llm_eval_kit/   package, engine, CLI
examples/           runnable evaluation suites
tests/              engine and CLI tests
.github/workflows/  cross-platform CI
```

## Testing

```bash
python -m compileall -q src tests
python -m pytest -q
llm-eval validate examples/basic.json
```

CI runs on Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.

## Security & privacy

Evaluation is local. The tool does not send prompts or outputs anywhere and does not execute them. Avoid committing confidential evaluation data. Only use trusted regular-expression rules in shared automation because pathological regex patterns can consume excessive CPU. See `SECURITY.md`.

## Limitations

This is a deterministic assertion toolkit, not a semantic judge. It does not measure factuality, creativity, toxicity, embeddings, latency, token cost, or model quality by itself. It does not call providers or generate candidate outputs. Exact/contains checks normalize case and whitespace but do not perform linguistic stemming. Regex behavior follows Python's `re` engine.

## Optional roadmap

Potential future additions include numeric-tolerance assertions, JSON-structure assertions, JUnit export, and pluggable user-defined scorers. These are not required for the current core workflow.

## Contributing

See `CONTRIBUTING.md`. Keep additions deterministic and offline by default, add tests, and document user-visible changes in both languages.

## License

MIT — see `LICENSE`.

## Author

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

# العربية

## نظرة عامة

**LLM Eval Kit** أداة Python صغيرة وحتمية وتعمل محليًا لاختبار مخرجات نماذج اللغة باستخدام حالات اختبار JSON قابلة لإعادة الاستخدام. تساعد على اكتشاف تغيّر السلوك عند تعديل البرومبت أو النموذج أو كود التطبيق. الأداة تفحص نصوصًا مولدة مسبقًا ولا تتصل بأي مزود نماذج.

## لماذا هذا المشروع؟

ليس كل تقييم يحتاج إلى نموذج آخر ليحكم على الإجابة. كثير من المتطلبات يمكن فحصها بقواعد واضحة وسريعة وقابلة للتكرار داخل CI. لذلك يوفر المشروع صيغة موحدة للحالات، وواجهة سطر أوامر، وPython API، وتقارير JSON، ورموز خروج ثابتة.

## الميزات

- مطابقة نص كامل بعد توحيد حالة الأحرف والمسافات.
- اشتراط كلمات أو عبارات متعددة ومنع عبارات غير مرغوبة.
- دعم التعبيرات النمطية وحد أقصى لطول الإجابة.
- درجة لكل حالة وملخص نجاح/فشل للمجموعة.
- دعم UTF-8 والنص العربي.
- تقارير JSON قابلة للحفظ والاستخدام في CI.
- أمر تحقق يكشف JSON غير الصحيح والمعرفات المكررة وregex غير الصالح والحالات بلا شروط.
- CLI وPython API دون اعتماديات تشغيل خارجية.
- يعمل دون شبكة أو مفاتيح API أو telemetry ولا ينفذ النص المقيم ككود.
- رموز الخروج: `0` نجاح كامل، `1` فشل شروط، `2` خطأ إدخال أو إعداد.

## المعاينة

```text
llm-eval run examples/basic.json
LLM Eval Kit — 2/2 passed (100%)
PASS concise-answer score=100%
PASS arabic-answer score=100%
```

المشروع سطري، لذلك لا يحتاج لقطة شاشة. يمكن لاحقًا استخدام لقطة طرفية للأمر أعلاه كصورة معاينة.

## المتطلبات والتثبيت

يتطلب Python 3.10 أو أحدث:

```bash
git clone https://github.com/rad03i2/llm-eval-kit.git
cd llm-eval-kit
python -m pip install -e .
```

للتطوير والاختبارات:

```bash
python -m pip install -e . pytest
```

## الاستخدام

```bash
llm-eval validate examples/basic.json
llm-eval run examples/basic.json
llm-eval run examples/basic.json --json
llm-eval run examples/basic.json --output reports/latest.json
python -m llm_eval_kit run examples/basic.json
```

ملف التقييم يمكن أن يحتوي على `expected` للمطابقة الكاملة، و`contains` لعبارات مطلوبة، و`excludes` لعبارات ممنوعة، و`regex` لأنماط Python، و`max_length` لحد طول النص. يجب أن يكون لكل حالة `id` فريد و`output` نصي وشرط واحد على الأقل.

## Python API

```python
from llm_eval_kit import Case, evaluate

result = evaluate(Case("arabic", "أهلًا بالموصل", contains=("الموصل",)))
print(result.passed, result.score)
```

## الإعداد

لا توجد متغيرات بيئة أو مفاتيح API أو ملفات إعداد مخفية. ملف JSON نفسه هو إعداد مجموعة التقييم، مما يجعل التشغيل واضحًا وقابلًا للمراجعة داخل Git.

## بنية المشروع

```text
src/llm_eval_kit/   الحزمة والمحرك وCLI
examples/           أمثلة قابلة للتشغيل
tests/              اختبارات المحرك وCLI
.github/workflows/  التكامل المستمر
```

## الاختبارات

```bash
python -m compileall -q src tests
python -m pytest -q
llm-eval validate examples/basic.json
```

يشغّل CI الاختبارات على Ubuntu وWindows وmacOS باستخدام Python 3.10 و3.12 و3.13.

## الأمان والخصوصية

كل التقييم محلي. لا تُرسل البرومبتات أو المخرجات إلى أي جهة ولا يتم تنفيذها. لا تضع بيانات سرية داخل ملفات الاختبار المرفوعة إلى Git. استخدم أنماط regex موثوقة فقط في البيئات المشتركة لأن النمط السيئ قد يستهلك المعالج. راجع `SECURITY.md`.

## القيود

الأداة ليست حكمًا دلاليًا ولا تقيس وحدها صحة المعلومات أو الإبداع أو السمية أو جودة النموذج أو التكلفة أو زمن الاستجابة. لا تستدعي نماذج ولا تولد الإجابات. فحوص النص توحد حالة الأحرف والمسافات لكنها لا تقوم بالاشتقاق اللغوي، وregex يتبع محرك Python `re`.

## تطوير اختياري مستقبلًا

يمكن إضافة فحوص الأرقام مع هامش سماح، والتحقق من بنية JSON، وتصدير JUnit، ومقيّمين مخصصين. هذه إضافات اختيارية وليست أجزاء ناقصة من الوظيفة الحالية.

## المساهمة

راجع `CONTRIBUTING.md`. يُفضّل إبقاء الوظائف حتمية ومحلية افتراضيًا، وإضافة اختبارات وتحديث التوثيق باللغتين لأي تغيير ظاهر للمستخدم.

## الترخيص

MIT — راجع `LICENSE`.

## المؤلف

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
