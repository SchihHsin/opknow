M1: 5 (scored) 第1次查询第1位命中相关官方PyTorch C++/CUDA算子教程。

M10: 3 (scored) 最终答案有LLTM和现代custom-op路线的具体代码与setup骨架，但LLTM注册了未给完整定义的lltm_backward，lltm_cuda_forward只有声明/启动片段；B路线setup、CPU注册函数和加载代码仍需补齐，属于内容修补。

M11: 75.82924799999998 (scored) Calculated from adjudicated point inputs; not a probability.

M2: 3 (scored) 三个官方fetch均保存为Extraction/Extracted正文表示，按M2规则均为excerpt分3；抓取表示不是内容完整度判定。

M3: 5 (scored) 官方当前教程、弃用教程和API正文合并覆盖LLTM kernel/launcher/binding/setup/install以及现代TORCH_LIBRARY、register_autograd和load路线，满足原题步骤与代码要求；M4版本配套缺口不重复扣M3。

M4: 3 (scored) 资料给出PyTorch 2.14/2.8及2.4弃用边界、CPython3.9稳定ABI和CUDA架构条件，但缺准确PyTorch/CUDA/toolkit/compiler组合。

M5: 3 (scored) 确定独立第三方内容组为weixin425教程和Zhihu671三线性插值教程；qq399与Zhihu348源码解读候选合并或分开，使possible_counts=[3,4]，均落入3–4档。官方翻译、镜像和逐字API复制不计独立第三方。

M6: 3 (scored) CSDN setuptools/ext_modules and binding descriptions plus Zhihu Cpp/CUDAExtension base-class clause have archived official support. Zhihu autograd absence/custom backward/Python and C++ subclass prescription lacks full applicable support; truncated system-directory fragment is not completed by the evaluator. Partial support, no confirmed contradiction.

M7: 3 (scored) 检索前回答正确给出CUDAExtension/BuildExtension、PYBIND11_MODULE、kernel launcher、数据指针和安装方法片段，但没有完整kernel/launcher/setup流程；自报不确定不扣分，不能用final补齐先验。

M8: 3 (scored) 实际派发为3次搜索+3次fetch，共6次，落入C=5–6分3档。

M9: 3 (scored) 最终答案给出现代教程、弃用边界、Python3.9/2.10 ABI及架构条件，但缺完整PyTorch/CUDA/toolkit/compiler版本组合。
