# Code Quality Report

## Overall Score: 63.20690708496066 (Poor)

## Metrics Summary

| Metric | Value | Grade |
|--------|-------|-------|
| Maintainability | 64.75591684179543 | Poor |
| Security | 73.33333333333333 | Fair |
| Structure | 70.0 | Fair |
| Testing Quality | null | N/A | Reason: No test files detected in the codebase.
| Code Coverage | null | N/A | Reason: No coverage reports found in the repository.
| Documentation | 98.9 | Excellent | 
| CI/CD | 71.0 | Fair | 
| Compliance | 50.0 | Poor |
| API Quality | null | N/A | Reason: No API endpoints or specifications detected.
| Monitoring | 20.0 | Poor | 

## Detailed Metrics

### Complexity
| Metric | Value | Grade |
|--------|-------|-------|
| Average Cyclomatic Complexity | 6.19 | Poor |
| Max Cyclomatic Complexity | 89 | - |
| % Functions CCN > 10 | 12.7% | - |

### Duplication
| Metric | Value | Grade |
|--------|-------|-------|
| Code Duplication % | N/A% | Poor |

### Security
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

### Structure
| Metric | Value |
|--------|-------|
| Functions with >7 Parameters | 38 |

## Recommendations

- **Maintainability**: Refactor complex functions (CCN > 10) and reduce code duplication.
- **Compliance**: Fix linting issues and adhere to coding standards.
- **Monitoring**: Implement proper logging and monitoring.


## Configuration & Workflow Files

| File | Present |
|------|---------|
| GitHub Actions Workflow | ✅ |
| GitLab CI | ❌ |
| CircleCI | ❌ |
| package.json | ❌ |
| tsconfig.json | ❌ |
| ESLint Config | ❌ |
| Prettier Config | ❌ |
| requirements.txt | ✅ |
| setup.py | ❌ |
| pyproject.toml | ✅ |
| Pipfile | ❌ |
| poetry.lock | ❌ |
| pylint Config | ❌ |
| pytest Config | ✅ |
| .env | ❌ |
| .env.example | ❌ |
| Security Policy | ❌ |
| Dockerfile | ❌ |
| docker-compose.yml | ❌ |
| README.md | ✅ |
| LICENSE | ✅ |
| CONTRIBUTING.md | ✅ |
| jest.config.js | ❌ |
| vitest.config | ❌ |
| .gitignore | ✅ |


## Complexity & Risky Functions

- **Average Cyclomatic Complexity**: 6.19
- **Max Cyclomatic Complexity**: 89
- **% Functions CCN > 10**: 12.7%

### Halstead Metrics for Main Files

| File | Vocabulary | Length | Volume | Difficulty | Effort |
|------|------------|--------|--------|------------|--------|
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/train.py | 276 | 276 | 2237.95 | 10.5 | 23498.5 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/val.py | 201 | 201 | 1537.86 | 8.5 | 13071.82 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/detect.py | 155 | 155 | 1127.8 | 7.5 | 8458.49 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/hubconf.py | 56 | 56 | 325.21 | 2.5 | 813.03 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/benchmarks.py | 77 | 77 | 482.54 | 5.5 | 2653.98 |
| /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/export.py | 285 | 285 | 2324.12 | 8.5 | 19755.05 |

| Function | CCN | Params |
|----------|-----|--------|
| train@100-541@/var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/segment/train.py | 89 | 4 |
| train@100-541@/var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/segment/train.py | 89 | 4 |
| train@105-543@/var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/train.py | 85 | 4 |

## Security & Static Analysis Findings (Semgrep)

**Total Security Findings:** 46

- Critical: 0
- Error: 20
- Warning: 26
- Info: 0

| Severity | File | Line | Rule | Message |
|----------|------|------|------|---------|
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/benchmarks.py | 145 | python.lang.security.audit.eval-detected.eval-detected | Detected the use of eval(). eval() can be dangerous if used to evaluate dynamic content. If this content can be input from outside the program, this may be a code injection vulnerability. Ensure evaluated content is not definable by external sources. |
| ERROR | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/classify/train.py | 110 | python.lang.security.audit.subprocess-shell-true.subprocess-shell-true | Found 'subprocess' function 'run' with 'shell=True'. This is dangerous because this call will spawn the command using a shell process. Doing so propagates current shell settings and variables, which makes it much easier for a malicious actor to execute commands. Use 'shell=False' instead. |
| ERROR | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/classify/train.py | 285 | trailofbits.python.pickles-in-pytorch.pickles-in-pytorch | Functions reliant on pickle can result in arbitrary code execution.  Consider loading from `state_dict`, using fickling, or switching to a safer serialization method like ONNX |
| ERROR | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/classify/train.py | 287 | trailofbits.python.pickles-in-pytorch.pickles-in-pytorch | Functions reliant on pickle can result in arbitrary code execution.  Consider loading from `state_dict`, using fickling, or switching to a safer serialization method like ONNX |
| ERROR | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/export.py | 938 | python.lang.security.audit.subprocess-shell-true.subprocess-shell-true | Found 'subprocess' function 'run' with 'shell=True'. This is dangerous because this call will spawn the command using a shell process. Doing so propagates current shell settings and variables, which makes it much easier for a malicious actor to execute commands. Use 'shell=False' instead. |
| ERROR | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/export.py | 939 | python.lang.security.audit.subprocess-shell-true.subprocess-shell-true | Found 'subprocess' function 'run' with 'shell=True'. This is dangerous because this call will spawn the command using a shell process. Doing so propagates current shell settings and variables, which makes it much easier for a malicious actor to execute commands. Use 'shell=False' instead. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/models/common.py | 514 | python.lang.security.audit.eval-detected.eval-detected | Detected the use of eval(). eval() can be dangerous if used to evaluate dynamic content. If this content can be input from outside the program, this may be a code injection vulnerability. Ensure evaluated content is not definable by external sources. |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/models/common.py | 575 | trailofbits.python.numpy-in-pytorch-modules.numpy-in-pytorch-modules | Usage of NumPy library inside PyTorch `DetectMultiBackend` module was found. Avoid mixing these libraries for efficiency and proper ONNX loading |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/models/common.py | 729 | trailofbits.python.numpy-in-pytorch-modules.numpy-in-pytorch-modules | Usage of NumPy library inside PyTorch `DetectMultiBackend` module was found. Avoid mixing these libraries for efficiency and proper ONNX loading |
| WARNING | /var/folders/_t/g_5mcvwn3zq1gm835_j9xfqr0000gn/T/tmp3axwll1t/models/common.py | 881 | trailofbits.python.numpy-in-pytorch-modules.numpy-in-pytorch-modules | Usage of NumPy library inside PyTorch `AutoShape` module was found. Avoid mixing these libraries for efficiency and proper ONNX loading |

*... and 36 more findings not shown*

## Custom Static Analysis Findings


### AI-Generated/Placeholder Code (598 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| Potential Placeholder Function | val.py | 64 | def save_one_txt(predn, save_conf, shape, file): |
| Potential Placeholder Function | val.py | 96 | def save_one_json(predn, jdict, path, class_map): |
| Potential Placeholder Function | val.py | 142 | def process_batch(detections, labels, iouv): |
| Potential Placeholder Function | val.py | 467 | def parse_opt(): |
| Potential Placeholder Function | val.py | 545 | def main(opt): |
| Potential Placeholder Function | export.py | 96 | def __init__(self, model, im): |
| Potential Placeholder Function | export.py | 122 | def forward(self, x): |
| Potential Placeholder Function | export.py | 143 | def export_formats(): |
| Potential Placeholder Function | export.py | 182 | def try_export(inner_func): |
| Potential Placeholder Function | export.py | 196 | def export_onnx(model, filepath): |
| Potential Placeholder Function | export.py | 209 | def outer_func(*args, **kwargs): |
| Potential Placeholder Function | export.py | 225 | def export_torchscript(model, im, file, optimize, prefix=colorstr("TorchScript:")): |
| Potential Placeholder Function | export.py | 280 | def export_onnx(model, im, file, opset, dynamic, simplify, prefix=colorstr("ONNX:")): |
| Potential Placeholder Function | export.py | 379 | def export_openvino(file, metadata, half, int8, data, prefix=colorstr("OpenVINO:")): |
| Potential Placeholder Function | export.py | 431 | def gen_dataloader(yaml_path, task="train", imgsz=640, workers=4): |
| Potential Placeholder Function | export.py | 440 | def transform_fn(data_item): |
| Potential Placeholder Function | export.py | 467 | def export_paddle(model, im, file, metadata, prefix=colorstr("PaddlePaddle:")): |
| Potential Placeholder Function | export.py | 515 | def export_coreml(model, im, file, int8, half, nms, mlmodel, prefix=colorstr("CoreML:")): |
| Potential Placeholder Function | export.py | 789 | def export_pb(keras_model, file, prefix=colorstr("TensorFlow GraphDef:")): |
| AI/Placeholder Code | export.py | 798 | Tuple[Path, None]: The file path where the GraphDef model was saved and a None placeholder. |

*... and 578 more*

### Security Issues (39 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| Dangerous Function | val.py | 283 | model.eval() |
| Insecure Import | val.py | 442 | from pycocotools.cocoeval import COCOeval |
| Dangerous Function | val.py | 446 | eval = COCOeval(anno, pred, "bbox") |
| Dangerous Function | export.py | 929 | if subprocess.run(f"{cmd} > /dev/null 2>&1", shell=True).returncode != 0: |
| Dangerous Function | export.py | 931 | sudo = subprocess.run("sudo --version >/dev/null", shell=True).returncode == 0  # sudo installed on  |
| Dangerous Function | export.py | 938 | subprocess.run(c if sudo else c.replace("sudo ", ""), shell=True, check=True) |
| Dangerous Function | export.py | 939 | ver = subprocess.run(cmd, shell=True, capture_output=True, check=True).stdout.decode().split()[-1] |
| Dangerous Function | export.py | 1379 | model.eval() |
| Dangerous Function | benchmarks.py | 145 | floor = eval(hard_fail)  # minimum metric floor to pass, i.e. = 0.29 mAP for YOLOv5n |
| Dangerous Function | classify/val.py | 105 | model.eval() |
| Dangerous Function | classify/train.py | 110 | subprocess.run(["bash", str(ROOT / "data/scripts/get_imagenet.sh")], shell=True, check=True) |
| Dangerous Function | segment/val.py | 226 | model.eval() |
| Insecure Import | segment/val.py | 422 | from pycocotools.cocoeval import COCOeval |
| Dangerous Function | segment/val.py | 427 | for eval in COCOeval(anno, pred, "bbox"), COCOeval(anno, pred, "segm"): |
| Dangerous Function | utils/dataloaders.py | 452 | s = eval(s) if s.isnumeric() else s  # i.e. s = '0' local webcam |
| Dangerous Function | utils/downloads.py | 29 | output = subprocess.check_output(["gsutil", "du", url], shell=True, encoding="utf-8") |
| Dangerous Function | utils/downloads.py | 119 | tag = subprocess.check_output("git tag", shell=True, stderr=subprocess.STDOUT).decode().split()[-1] |
| Dangerous Function | utils/torch_utils.py | 107 | return int(subprocess.run(cmd, shell=True, capture_output=True, check=True).stdout.decode().split()[ |
| Dangerous Function | utils/torch_utils.py | 454 | self.ema = deepcopy(de_parallel(model)).eval()  # FP32 EMA |
| Dangerous Function | utils/general.py | 366 | return check_output(f"git -C {path} describe --tags --long --always", shell=True).decode()[:-1] |

*... and 19 more*

### Code Quality Issues (4 instances)

| Type | File | Line | Snippet |
|------|------|------|---------|
| Code Quality Issue | utils/augmentations.py | 336 | # TODO: implement AugMix, AutoAug & RandAug in albumentation |
| Code Quality Issue | utils/loggers/__init__.py | 318 | # Calling wandb.log. TODO: Refactor this into WandbLogger.log_model |
| Code Quality Issue | utils/segment/dataloaders.py | 200 | # TODO: albumentations support |
| Code Quality Issue | models/yolo.py | 437 | # TODO: channel, gw, gd |

## Dependency Analysis

### Python Dependencies

- **Total Packages**: 19
- **Package Usage Rate**: 57.9%

**Unused Packages (8)**:
- thop
- gitpython
- pyyaml
- pillow
- urllib3
- opencv-python
- packaging  # migration of deprecated pkg-resources packages
- psutil  # system resources

## Final Summary

This codebase is generally solid but has some areas for improvement, especially in testing, documentation, or CI/CD.
Code Coverage: No coverage reports found in the repository.
Testing Quality: No test files detected in the codebase.
API Quality: No API endpoints or specifications detected.