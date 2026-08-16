# intent_classifier.py

from intent_keywords import KEYWORDS
from intent_weights_base import BASE_WEIGHTS
from intent_weights_dynamic import DynamicWeights
from intent_score import compute_intent_score
from intent_fallback import fallback_intent

from axis_extractor import extract_axis_weights        # ← 新規：意味軸抽出
from reasoning_mapper import map_axis_to_reasoning     # ← 新規：推論タイプ決定
from direction_intent import get_direction_intent      # ← 新規：推論方向ベクトル
from final_vector import build_final_vector            # ← 新規：方向ベクトル生成
from fallback_axis import apply_axis_fallback          # ← 新規：安全軸補正


class IntentClassifier:
    def __init__(self):
        self.base_weights = BASE_WEIGHTS
        self.dynamic_weights = DynamicWeights()

    def extract_features(self, text, source_bias):
        """
        あなたがロジックを書く場所：
        - KeywordStrength
        - ContextStrength
        - StructureStrength
        - SourceStrength

        ここは「特徴量抽出」だけ。
        意味軸の重みはここでは決めない。
        """
        features = {
            "keyword_strength": None,
            "context_strength": None,
            "structure_strength": None,
            "source_strength": None,
        }
        return features

    def classify(self, text, source_bias):
        """
        Intent Layer のメイン処理。
        """

        # ① 特徴量抽出（あなたが書く）
        features = self.extract_features(text, source_bias)

        # ② 意味軸の重み抽出（あなたが書く）
        axis_weight = extract_axis_weights(text, features)

        # ③ 曖昧さ検知 → 安全軸補正（あなたが書く）
        axis_weight = apply_axis_fallback(axis_weight, text, features)

        # ④ 推論タイプ決定（あなたが書く）
        reasoning_type = map_axis_to_reasoning(axis_weight)

        # ⑤ 推論方向ベクトル（あなたが書く）
        direction = get_direction_intent(reasoning_type)

        # ⑥ final_vector 生成（あなたが書く）
        final_vec = build_final_vector(axis_weight, direction)

        # ⑦ intent スコア計算（既存）
        scores = self.score_intents(features)
        intent, score = self.select_intent(scores)

        # ⑧ intent fallback（既存）
        if score < 0.25:
            intent = fallback_intent(text)

        return {
            "intent": intent,
            "score": score,
            "axis_weight": axis_weight,
            "reasoning_type": reasoning_type,
            "direction_vector": direction,
            "final_vector": final_vec,
            "features": features,
            "scores": scores
        }
