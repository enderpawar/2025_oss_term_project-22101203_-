"""
실제 CSV 파일로 테스트하는 예제
사용자가 파이프라인 빌더에서 만들 수 있는 코드와 동일
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("="*60)
print("🤖 ML Pipeline Builder - 실제 작동 데모")
print("="*60)

# 1. 샘플 CSV 데이터 생성 (실제로는 사용자가 업로드)
print("\n📁 Step 1: 데이터 생성 중...")
np.random.seed(42)

# 가짜 고객 이탈 데이터 생성
n_samples = 1000
data = pd.DataFrame({
    '나이': np.random.randint(18, 70, n_samples),
    '월_사용액': np.random.randint(10000, 200000, n_samples),
    '사용_기간_개월': np.random.randint(1, 120, n_samples),
    '고객_등급': np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], n_samples),
    '민원_횟수': np.random.randint(0, 10, n_samples),
})

# 타겟 변수 생성 (이탈 여부)
# 민원이 많고, 사용액이 적고, 기간이 짧으면 이탈 확률 높음
churn_prob = (
    (data['민원_횟수'] > 5).astype(int) * 0.3 +
    (data['월_사용액'] < 50000).astype(int) * 0.3 +
    (data['사용_기간_개월'] < 24).astype(int) * 0.2 +
    np.random.random(n_samples) * 0.2
)
data['이탈'] = (churn_prob > 0.5).astype(int)

# 범주형 변수 인코딩
data['고객_등급_코드'] = data['고객_등급'].map({
    'Bronze': 1, 'Silver': 2, 'Gold': 3, 'Platinum': 4
})

print(f"✅ 데이터 생성 완료: {data.shape}")
print("\n📊 데이터 미리보기:")
print(data.head())
print(f"\n이탈 비율: {data['이탈'].mean():.1%}")

# 2. 데이터 분할
print("\n" + "="*60)
print("✂️ Step 2: Train/Test Split")
print("="*60)

# 특성과 타겟 분리
X = data[['나이', '월_사용액', '사용_기간_개월', '고객_등급_코드', '민원_횟수']]
y = data['이탈']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"✅ 훈련 데이터: {len(X_train)}개")
print(f"✅ 테스트 데이터: {len(X_test)}개")

# 3. 스케일링
print("\n" + "="*60)
print("⚖️ Step 3: 데이터 스케일링")
print("="*60)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"✅ StandardScaler 적용 완료")
print(f"   Train shape: {X_train_scaled.shape}")
print(f"   Test shape: {X_test_scaled.shape}")

# 4. 모델 훈련
print("\n" + "="*60)
print("🎓 Step 4: 모델 훈련")
print("="*60)

# 두 가지 모델 비교
models = {
    'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
    'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000)
}

results = {}

for name, model in models.items():
    print(f"\n🔄 {name} 훈련 중...")
    model.fit(X_train_scaled, y_train)
    
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    print(f"   ✅ 훈련 정확도: {train_score:.4f}")
    print(f"   ✅ 테스트 정확도: {test_score:.4f}")
    
    results[name] = {
        'model': model,
        'train_score': train_score,
        'test_score': test_score
    }

# 5. 평가
print("\n" + "="*60)
print("📊 Step 5: 상세 평가")
print("="*60)

for name, result in results.items():
    print(f"\n{'='*60}")
    print(f"🎯 {name} 결과")
    print(f"{'='*60}")
    
    model = result['model']
    y_pred = model.predict(X_test_scaled)
    
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n✅ Accuracy: {accuracy:.4f}")
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['유지', '이탈']))
    print("\n📊 Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    print(f"\n해석:")
    print(f"  - 실제 유지, 예측 유지: {cm[0][0]}명")
    print(f"  - 실제 유지, 예측 이탈: {cm[0][1]}명 (False Positive)")
    print(f"  - 실제 이탈, 예측 유지: {cm[1][0]}명 (False Negative)")
    print(f"  - 실제 이탈, 예측 이탈: {cm[1][1]}명")

# 6. 특성 중요도 (RandomForest만)
print("\n" + "="*60)
print("🔍 Step 6: 특성 중요도 분석")
print("="*60)

rf_model = results['RandomForest']['model']
feature_importance = pd.DataFrame({
    '특성': X.columns,
    '중요도': rf_model.feature_importances_
}).sort_values('중요도', ascending=False)

print("\n📊 특성 중요도 (높을수록 중요):")
print(feature_importance.to_string(index=False))

# 7. 실제 예측 예제
print("\n" + "="*60)
print("🔮 Step 7: 신규 고객 이탈 예측")
print("="*60)

# 새로운 고객 데이터
new_customers = pd.DataFrame({
    '나이': [25, 45, 60],
    '월_사용액': [30000, 150000, 80000],
    '사용_기간_개월': [6, 48, 24],
    '고객_등급_코드': [1, 4, 3],
    '민원_횟수': [7, 1, 3]
})

print("\n📝 예측할 고객 정보:")
print(new_customers)

new_customers_scaled = scaler.transform(new_customers)
predictions = rf_model.predict(new_customers_scaled)
probabilities = rf_model.predict_proba(new_customers_scaled)

print("\n🎯 예측 결과:")
for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
    status = "⚠️ 이탈 위험" if pred == 1 else "✅ 유지 예상"
    print(f"\n고객 {i+1}: {status}")
    print(f"  - 이탈 확률: {prob[1]:.1%}")
    print(f"  - 유지 확률: {prob[0]:.1%}")

# 최종 요약
print("\n" + "="*60)
print("🎉 파이프라인 실행 완료!")
print("="*60)
print("\n✅ 이 모든 과정을 파이프라인 빌더에서")
print("   드래그 앤 드롭만으로 만들 수 있습니다!")
print("\n📝 생성된 코드:")
print("   1. 즉시 실행 가능")
print("   2. scikit-learn 베스트 프랙티스 준수")
print("   3. 초보자도 이해 가능한 주석")
print("   4. 실전 프로젝트 수준의 품질")
print("\n🚀 지금 바로 시작하세요!")
print("="*60)
