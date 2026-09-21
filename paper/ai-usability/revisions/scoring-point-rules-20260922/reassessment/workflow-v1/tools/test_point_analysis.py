import unittest

from point_analysis import analyze_data

MODELS = ("glm-5.3", "deepseek-v4.1-flash", "kimi-k3-2")
MAIN = tuple(chr(i) for i in range(ord("A"), ord("Z") + 1) if chr(i) != "G")


def rows(with_missing=False):
    out = []
    for model_index, model in enumerate(MODELS):
        for task in MAIN + ("G",):
            for eco in ("cann", "cuda"):
                metrics = {f"M{i}": {"status": "scored", "score": 2} for i in range(1, 11)}
                metrics["M1"]["score"] = model_index + 1
                metrics["M2"]["score"] = model_index + 1.5
                metrics["M11"] = {"status": "scored", "score": 10.0 + model_index * 10}
                if with_missing and task == "A" and eco == "cann":
                    metrics["M1"] = {"status": "unscorable", "score": None, "reason": "missing ownership"}
                out.append({"run_id": f"{task}-{eco}-{model}", "model": model,
                            "task": task, "ecosystem": eco, "metrics": metrics})
    return {"rows": out}


class PointAnalysisTests(unittest.TestCase):
    def test_missing_pair_excluded_and_denominator_is_metric_local(self):
        d = analyze_data({"rows": [r for r in rows(with_missing=True)["rows"] if r["model"] == "glm-5.3"]})
        m = d["paired_main"]["glm-5.3"]["M1"]
        self.assertEqual(m["n"], 24)
        self.assertTrue(any(x["task"] == "A" for x in m["excluded"]))
        self.assertEqual(d["model_ecosystem_metrics"]["glm-5.3"]["cann"]["M1"]["scored_n"], 24)
        self.assertEqual(d["model_ecosystem_metrics"]["glm-5.3"]["cann"]["M2"]["scored_n"], 25)

    def test_g_is_separate_from_main_25_task_denominators(self):
        d = analyze_data(rows())
        self.assertEqual(d["paired_main"]["glm-5.3"]["M2"]["n"], 25)
        self.assertEqual(d["migration_G"]["glm-5.3"]["M2"]["n"], 1)
        self.assertEqual(d["model_ecosystem_metrics"]["glm-5.3"]["cann"]["M2"]["count"], 25)
        self.assertEqual(d["migration_G_model_ecosystem_metrics"]["glm-5.3"]["cann"]["M2"]["count"], 1)

    def test_models_are_filtered_and_scores_are_not_pooled(self):
        d = analyze_data(rows())
        for model_index, model in enumerate(MODELS):
            paired = d["paired_main"][model]["M1"]
            self.assertEqual(paired["n"], 25)
            self.assertTrue(all(p["model"] == model for p in paired["pairs"]))
            self.assertEqual(paired["mean"], 0.0)
            self.assertEqual(d["model_ecosystem_metrics"][model]["cann"]["M1"]["mean"], model_index + 1)
            self.assertEqual(d["migration_G"][model]["M11"]["n"], 1)
            self.assertEqual(d["migration_G"][model]["M11"]["mean"], 0.0)

    def test_float_m2_and_m11_keep_scale(self):
        d = analyze_data(rows())
        self.assertEqual(d["model_ecosystem_metrics"]["glm-5.3"]["cann"]["M2"]["mean"], 1.5)
        self.assertEqual(d["model_ecosystem_metrics"]["glm-5.3"]["cann"]["M11"]["mean"], 10.0)


if __name__ == "__main__":
    unittest.main()
