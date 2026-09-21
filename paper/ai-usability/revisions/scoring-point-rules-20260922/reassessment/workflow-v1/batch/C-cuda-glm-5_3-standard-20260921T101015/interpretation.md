# C-cuda-glm-5_3-standard-20260921T101015

M1: 5 (scored). First-query rank 1 is the relevant official NVIDIA China cuSPARSE page.

M2: 4.666666666666667 (scored). Five direct official bodies without observed defects, plus one merged cuBLAS URL whose last return is an explicit extraction (3). The third-party fetch is excluded.

M3: 3 (scored). Official contents explain library selection, cuBLAS setup and graph API structure, but neither the actual GEMM function reference nor concrete convolution invocation is obtained. These are main requirements.

M4: 3 (scored). cuBLAS API introduction versions provide partial CUDA relationships; the necessary cuDNN/CUDA/device compatibility is absent.

M5: 4 (scored). Five relevant independent third-party pages after publisher/relevance review.

M6: 1 (scored). The full third-party sample contains a definite C++ type error: float* matrix is accessed as matrix[i][j], so its invocation example does not compile. A syntax-only check of the archived function confirms the failure. This key operational error takes precedence over supported layout and flag statements.

M7: None (unscorable). Prior library roles/layout and handle setup have support, but exact cuDNN legacy algorithm calls, full GEMM/SpMM invocation and TF32 control applicability cannot be established from the saved material. These affect the required invocation completeness.

M8: 1 (scored). Three search plus eight fetch dispatches, C=11.

M9: 2 (scored). Final gives cuBLAS 13.4 and cuDNN 9.x documentation labels but no applicable primary CUDA/cuDNN pairing. Optional cuSPARSELt architecture advice does not fill the dense/convolution version requirement.

M10: 3 (scored). The shortened cuDNN graph example omits output allocation/binding from its claimed complete original and gives only an analogy for convolution. It requires code/content completion, not merely path substitution.

M11: None (unscorable). M7 lacks resolved input; do not impute.

No new collection or hardware execution. M7 exact prior API correctness lacks archived support; M11 lacks M7. Static C++ syntax check verifies only an archived third-party function, not a CUDA experiment.
