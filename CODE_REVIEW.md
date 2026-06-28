# Code Review Findings

Review of `predictor.py`, `trainer.py`, and `utils.py` across two passes.
All 16 findings resolved.

---

# Round 1

Review of the PEP8/flake8 compliance pass.

---

## ~~1. ZeroDivisionError when dataset has exactly 2 data rows (with `-a` flag)~~ ✅ Fixed

**File:** `utils.py:84` | **Severity:** ~~Crash~~ → Resolved

```python
# Before
rse = (residual_sum_of_squares / (len(dataset) - 2)) ** 0.5

# After
if len(dataset) > 2:
    rse = (residual_sum_of_squares / (len(dataset) - 2)) ** 0.5
    print(f"Residual Standard Error (RSE) = {rse:,.4f}{DEF}")
else:
    print(f"Residual Standard Error (RSE) = N/A{DEF}")
```

The degenerate 2-point case is now handled gracefully by printing `N/A` instead of dividing by zero.

---

## ~~2. `read_thetas` mutates global `args` it was never passed~~ ✅ Fixed

**File:** `predictor.py:46` | **Severity:** ~~NameError on safe-fallback path~~ → Resolved

```python
# Before — mutated global
args.plot = False
return 0, 0, ["km", "price"]

# After — returns a flag as part of the tuple
return 0, 0, ["km", "price"], False
```

`read_thetas` now returns a 4-tuple `(theta0, theta1, labels, thetas_found)`. The caller unpacks it at line 104 and gates the plot on `args.plot and thetas_found` at line 109. The global side-effect is gone.

---

## ~~3. Timeout error leaves terminal stuck in red~~ ✅ Fixed

**File:** `trainer.py:98` | **Severity:** ~~Observable — terminal color leak~~ → Resolved

```python
# Before
raise ValueError(f"{RED} Error: Maximum calculation time exceeded")

# After
raise ValueError(f"{RED}\nError: Maximum calculation time exceeded{DEF}")
```

`{DEF}` is now present in the error message. Additionally the `except ValueError` handler at line 147 now always emits a trailing reset: `print(f"{error}{DEF}")`, providing a second safety net for all error paths.

> **Minor note (resolved):** The backslash continuation on the `raise` line embedded 29 spaces into the string before the `\n`. Fixed in Round 2 by switching to implicit string literal concatenation inside the parentheses.

---

## ~~4. Any dataset parse error also leaves terminal stuck in red~~ ✅ Fixed

**File:** `trainer.py:144` | **Severity:** ~~Observable — terminal color leak~~ → Resolved

```python
# Before
print(error)

# After
print(f"{error}{DEF}")
```

The centralised `except ValueError` handler now always resets the terminal color, covering every error path including the `read_dataset` one where `{RED}` was set but `{DEF}` was skipped on exception.

---

## ~~5. `split('.')[0]` silently truncates multi-dot filenames~~ ✅ Fixed

**File:** `predictor.py:104` and `trainer.py:118` | **Severity:** ~~Wrong output / FileNotFoundError~~ → Resolved

```python
# Before
filename = f"{args.thetas_file.split('.')[0]}.csv"   # predictor.py
filename = args.dataset_file.split('.')[0]            # trainer.py

# After
filename = os.path.splitext(args.thetas_file)[0] + ".csv"   # predictor.py
filename = os.path.splitext(args.dataset_file)[0]            # trainer.py
```

`os.path.splitext` only strips the last extension, so `my.data.csv` correctly yields `my.data` instead of `my`. `import os` added to both files.

---

## ~~6. `gradient_descent` and `write_json_data` depend on hidden global `args`~~ ✅ Fixed

**File:** `trainer.py:77` and `trainer.py:115` | **Severity:** ~~Latent NameError~~ → Resolved

```python
# Before — accessed global args silently
def gradient_descent(norm_dataset, dataset, timeout=10):
    ...
    if args.normalized: ...

def write_json_data(labels, slope, intercept):
    filename = args.dataset_file.split('.')[0]

# After — args passed explicitly as a parameter
def gradient_descent(norm_dataset, dataset, args, timeout=10):
    ...
    if args.normalized: ...

def write_json_data(labels, slope, intercept, args):
    filename = os.path.splitext(args.dataset_file)[0]
```

Both functions now receive `args` as an explicit parameter. The dependency is visible in the signature and the functions work correctly regardless of how they are called.

---

## ~~7. Ternary expression used as a statement for a pure side-effect~~ ✅ Fixed

**File:** `trainer.py:139` and `utils.py:24` | **Severity:** ~~Cleanup~~ → Resolved

```python
# Before — ternary with discarded result
model_metrics(dataset[1:], slope, intercept) if args.accuracy else None
plot_line(dataset[1:], slope, intercept) if regression else None

# After — plain if statement
if args.accuracy:
    model_metrics(dataset[1:], slope, intercept)
if regression:
    plot_line(dataset[1:], slope, intercept)
```

Both replaced with idiomatic `if` statements. Intent is now unambiguous and linter warnings are gone.

---

## ~~8. `len(norm_dataset[1:])` allocates a throwaway list slice twice per hot-loop iteration~~ ✅ Fixed

**File:** `trainer.py:80` | **Severity:** ~~Efficiency~~ → Resolved

```python
# Before — computed twice per iteration
m_norm -= m_gradient * LEARNING_RATE / len(norm_dataset[1:])
b_norm -= b_gradient * LEARNING_RATE / len(norm_dataset[1:])

# After — precomputed once before the loop
len_norm_dataset = len(norm_dataset[1:])
...
m_norm -= m_gradient * LEARNING_RATE / len_norm_dataset
b_norm -= b_gradient * LEARNING_RATE / len_norm_dataset
```

The length is now computed once before the loop and reused on both update lines.

---

## Round 1 Summary

| # | File | Line | Severity | Description | Status |
|---|------|------|----------|-------------|--------|
| 1 | `utils.py` | 84 | Crash | ZeroDivisionError in RSE with 2 data rows | ✅ Fixed |
| 2 | `predictor.py` | 46 | NameError | `read_thetas` mutated global `args` it never received | ✅ Fixed |
| 3 | `trainer.py` | 98 | Observable | Timeout error missing `DEF` reset — terminal stuck red | ✅ Fixed |
| 4 | `trainer.py` | 144 | Observable | Parse error path missing `DEF` reset — terminal stuck red | ✅ Fixed |
| 5 | `predictor.py` / `trainer.py` | 104 / 118 | Wrong output | `split('.')[0]` truncates multi-dot filenames | ✅ Fixed |
| 6 | `trainer.py` | 77 / 115 | Latent | `gradient_descent` / `write_json_data` read hidden global `args` | ✅ Fixed |
| 7 | `trainer.py` / `utils.py` | 139 / 24 | Cleanup | Ternary used as statement for side-effect only | ✅ Fixed |
| 8 | `trainer.py` | 80 | Efficiency | `len(norm_dataset[1:])` allocated twice per hot-loop step | ✅ Fixed |

---

# Round 2

Second review pass after Round 1 fixes were applied.

---

## ~~1. `except ValueError` in predictor missing `{DEF}` reset — terminal stuck in red~~ ✅ Fixed

**File:** `predictor.py:109` | **Severity:** ~~Observable — terminal color leak~~ → Resolved

```python
# Before
except ValueError as error:
    print(error)          # no {DEF} reset

# After
except ValueError as error:
    print(f"{error}{DEF}")
    sys.exit(1)
```

`{DEF}` added to the handler, matching the pattern already applied to `trainer.py:145` in Round 1.

---

## ~~2. `float(theta0)` raises uncaught `TypeError` for non-numeric JSON values~~ ✅ Fixed

**File:** `predictor.py:40` | **Severity:** ~~Crash — unhandled traceback~~ → Resolved

```python
# Before
theta0 = float(theta0)   # TypeError if theta0 is a list, dict, etc.

# After
if not isinstance(theta0, (int, float)):
    raise ValueError("Invalid type for theta0")
if not isinstance(theta1, (int, float)):
    raise ValueError("Invalid type for theta1")
theta0 = float(theta0)   # safe — type is guaranteed numeric
theta1 = float(theta1)
```

Type validated before conversion; bad values now raise a clean `ValueError` caught by the existing handler instead of a raw traceback.

---

## ~~3. `for label in labels` raises uncaught `TypeError` when `labels` is not iterable~~ ✅ Fixed

**File:** `predictor.py:44` | **Severity:** ~~Crash — unhandled traceback~~ → Resolved

```python
# Before
labels = [str(label) for label in labels]  # TypeError if labels is bool, int, etc.

# After
if not isinstance(labels, list) or len(labels) != 2:
    raise ValueError("Invalid labels format")
labels = [str(label) for label in labels]  # safe — guaranteed to be a list
```

Combined with finding #4's length check in a single guard. Non-iterable types now raise a clean `ValueError`.

---

## ~~4. `labels[0]` / `labels[1]` accessed without bounds check — `IndexError` uncaught~~ ✅ Fixed

**File:** `predictor.py:44` | **Severity:** ~~Crash — unhandled traceback~~ → Resolved

```python
# Before — no length check; labels[0]/labels[1] at line 105 could IndexError
labels = [str(label) for label in labels]

# After — length validated alongside type in the same guard
if not isinstance(labels, list) or len(labels) != 2:
    raise ValueError("Invalid labels format")
```

Folded into the same `isinstance` check as finding #3. A short or empty labels list now raises a clean `ValueError` in `read_thetas` before the caller ever touches `labels[0]` or `labels[1]`.

---

## ~~5. Backslash continuation embeds 29 spaces before `\n` in timeout error message~~ ✅ Fixed

**File:** `trainer.py:99` | **Severity:** ~~Cosmetic — garbled output~~ → Resolved

```python
# Before
raise ValueError(f"{RED}\
                             \nError: Maximum calculation time exceeded{DEF}")

# After
raise ValueError(f"{RED}\nError: Maximum calculation time"
                 f" exceeded{DEF}")
```

Backslash continuation replaced with implicit string literal concatenation inside the function call parentheses. No stray spaces in the resulting string.

---

## ~~6. `norm_dataset[1:]` allocates a new list on every gradient-descent iteration~~ ✅ Fixed

**File:** `trainer.py:82` | **Severity:** ~~Efficiency~~ → Resolved

```python
# Before
len_norm_dataset = len(norm_dataset[1:])   # precomputed ✓
while (True):
    ...
    for point in norm_dataset[1:]:          # new list every iteration ✗

# After
data_points = norm_dataset[1:]             # one allocation before the loop
len_norm_dataset = len(data_points)
while (True):
    ...
    for point in data_points:              # reuses the same list
```

Slice computed once and reused. As a bonus, the magic number `10` was also extracted to a module-level `TIMEOUT = 10` constant.

---

## ~~7. `print()` called on every gradient-descent iteration — write syscall dominates wall time~~ ✅ Fixed

**File:** `trainer.py:84` | **Severity:** ~~Efficiency~~ → Resolved

```python
# Before
print(f"\rCalculating linear regression... {i}", end="")

# After
if i % 1000 == 0:
    print(f"\rCalculating linear regression... {i}", end="")
```

Print is now throttled to every 1000 iterations, reducing terminal write syscalls by 1000×.

---

## ~~8. `time.time()` syscall issued on every iteration even though timeout rarely fires~~ ✅ Fixed

**File:** `trainer.py:99` | **Severity:** ~~Efficiency~~ → Resolved

```python
# Before
if (time.time() - timeout_start_time) > timeout:

# After
if i % 1000 == 0 and (time.time() - timeout_start_time) > timeout:
```

`time.time()` is now checked only once every 1000 iterations, reducing syscall frequency by 1000× with no meaningful loss of timeout accuracy.

---

## Round 2 Summary

| # | File | Line | Severity | Description | Status |
|---|------|------|----------|-------------|--------|
| 1 | `predictor.py` | 109 | Observable | `print(error)` missing `{DEF}` — terminal stuck red after any error | ✅ Fixed |
| 2 | `predictor.py` | 40 | Crash | `float(theta0)` raises uncaught `TypeError` for non-numeric JSON values | ✅ Fixed |
| 3 | `predictor.py` | 44 | Crash | `for label in labels` raises uncaught `TypeError` for non-iterable JSON values | ✅ Fixed |
| 4 | `predictor.py` | 44 | Crash | `labels[0]`/`labels[1]` raises uncaught `IndexError` for short/empty labels | ✅ Fixed |
| 5 | `trainer.py` | 99 | Cosmetic | Backslash continuation embeds 29 spaces before `\n` in timeout error | ✅ Fixed |
| 6 | `trainer.py` | 82 | Efficiency | `norm_dataset[1:]` allocates a new list on every hot-loop iteration | ✅ Fixed |
| 7 | `trainer.py` | 84 | Efficiency | `print()` syscall on every iteration dominates wall time on slow terminals | ✅ Fixed |
| 8 | `trainer.py` | 99 | Efficiency | `time.time()` syscall on every iteration; timeout almost never triggers | ✅ Fixed |

---

# Round 3

Third review pass focused on exception handling coverage against the project requirement:
*"If your program crashes due to unhandled exceptions during the review, it will be considered non-functional."*

---

## ~~1. `json.load()` on a non-object JSON file raises uncaught `AttributeError`~~ ✅ Fixed

**File:** `predictor.py:33` | **Severity:** Crash — unhandled traceback

```python
# Before
values = json.load(file)
theta0 = values.get('theta0')   # AttributeError if values is not a dict

# After
values = json.load(file)
if not isinstance(values, dict):
    raise ValueError("Invalid JSON format")
theta0 = values.get('theta0')   # safe — guaranteed to be a dict
```

`json.load()` succeeds for any valid JSON, not just objects. Files containing `[1, 2, 3]`, `42`, `"hello"`, or `null` all parse successfully but return a list, int, str, or `None`. Calling `.get()` on any of these raises `AttributeError`, which is not caught by the `OSError / json.JSONDecodeError / ValueError` handlers — raw traceback.

The fix adds a dict check immediately after `json.load()`, converting the failure into a clean `ValueError` caught by the existing handler.

---

## Round 3 Summary

| # | File | Line | Severity | Description | Status |
|---|------|------|----------|-------------|--------|
| 1 | `predictor.py` | 33 | Crash | `json.load()` on non-object JSON raises uncaught `AttributeError` | ✅ Fixed |
