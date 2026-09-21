M1: 2 (scored) 第二次查询首次命中官方PyTorch环境变量文档。

M2: 4 (scored) official fetch documents scored independently and averaged

M3: 3 (scored) 核心定位kernel实际输出/源码位置的方法有说明，但DSA构建与示例细节不足。

M4: 3 (scored) partial version/applicability relations; required compatibility mapping remains missing

M5: 5 (scored) At least six independent diagnostic content groups. Same-title reproduction candidates enumerated, official manual copy excluded; generic snippet does not erase relevant DSA article title.

M6: 3 (scored) 异步与同步主张有独立支持；精确栈、性能和部分OS步骤无支持，完成核查后为部分支持。

M7: None (unscorable) 先验同步/memcheck片段正确，但DSA默认构建、ARCH列表行号、Nsight等关键断言未能由固定包完全核清。

M8: 2 (scored) Actual3 search+4 fetch dispatches=7, score2.

M9: 3 (scored) 当前Compute Sanitizer/CUDA toolkit文档存在，但不能推出所有PyTorch 2.x与CUDA耦合关系。

M10: 3 (scored) 最终答案的DSA源码构建缺具体步骤，需内容补写；其余环境字段替换不单独造成3。

M11: None (unscorable) M7为unscorable，综合指数缺少有效先验输入。
