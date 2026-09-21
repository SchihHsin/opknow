M1: 5 (scored) First query first-five results contain the first reviewed relevant official source at the recorded rank.

M2: 4.5 (scored) Eight official fetched documents: API navigation2, Chinese guide body4 because referenced diagrams are absent, remaining direct bodies5. Mean36/8. Overview pages with actual explanations/release constraints are body, unlike pure API index.

M3: 5 (scored) Official calibration guide/API plus Torch-TensorRT PTQ body cover representative data, preprocessing, algorithm selection, callbacks/cache, compile settings and use of resulting module for inference. Main calibration/deployment route is explained; hardware/version selection is evaluated separately.

M4: 3 (scored) Official material provides partial version/component constraints, but not a complete direct compatibility relation for all required components.

M5: 3 (scored) Four independent relevant third-party articles after repeated URLs and official guide translations are excluded. Chinese Torch-TensorRT documentation is identifiable translated official content, not an independent source.

M6: 5 (scored) The single identifiable third-party assertion recommends QAT for accuracy; official workflow explicitly says QAT generally recovers more accuracy than PTQ. Independent publisher evidence supports the qualified recommendation. Generic descriptions and unspecified-function fragment do not constitute further evaluable assertions.

M7: None (unscorable) Prior contains supported calibration principles, algorithms and callback fragments, but prescribes a general500–1000-image requirement and build_engine API whose stated7/8 applicability is not fully verified in saved materials. The official example only establishes about500 for ImageNet. Cannot certify a correct complete route from absence of contradiction; expressly uncertain CLI flags are not treated as errors.

M8: 1 (scored) Actual dispatched search/fetch events: 12.

M9: 3 (scored) Final distinguishes10.x calibration and11.x Q/DQ routes with supported API transition boundaries, but leaves CUDA/GPU applicability of selected10.x route unresolved. Version ranges alone would permit4 only when all necessary relations are supported.

M10: 3 (scored) Claimed complete Python sample leaves device_input as Ellipsis, reads self.batches never initialized, lacks cuda import/context and defines no batchstream. These require actual implementation repairs, independent of unexecuted status. Model-specific inference buffer/runtime steps also remain absent.

M11: None (unscorable) Prior positive API/sample-size assertions lack complete applicable verification.
