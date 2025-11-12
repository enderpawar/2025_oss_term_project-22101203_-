# 🧠 ML Pipeline Builder 사용 가이드

## 개요

**ML Pipeline Builder**는 시각적 노드 기반 인터페이스를 통해 머신러닝 파이프라인을 구성하고, 자동으로 Python 코드를 생성하는 교육용 도구입니다.

### 🎯 주요 기능

1. **시각적 파이프라인 구성**: 드래그 & 드롭으로 ML 워크플로우 설계
2. **Python 코드 자동 생성**: 노드 그래프를 실행 가능한 Python 코드로 변환
3. **Jupyter Notebook 내보내기**: .ipynb 파일로 저장하여 즉시 실행 가능
4. **Python 스크립트 내보내기**: .py 파일로 저장하여 배포 가능

---

## 🚀 빠른 시작

### 1. 새 파이프라인 생성

1. 메인 화면에서 **"새 로직 생성"** 버튼 클릭
2. 파이프라인 이름 입력 (예: "Iris Classification")
3. LogicEditor 화면으로 진입

### 2. 노드 추가

왼쪽 사이드바에서 노드를 드래그하여 캔버스에 추가:

#### 📊 Data Source
- **Data Loader**: CSV, JSON, SQL 데이터 로드

#### 🔧 Preprocessing
- **Data Split**: Train/Test 데이터 분할
- **Scaler**: 데이터 정규화 (StandardScaler, MinMaxScaler)
- **Feature Selection**: 중요 특성 선택

#### 🤖 Models
- **Classifier**: 분류 모델 (RandomForest, LogisticRegression, SVM)
- **Regressor**: 회귀 모델 (LinearRegression, Ridge)
- **Neural Network**: 다층 퍼셉트론 (MLP)

#### 📈 Evaluation
- **Evaluate Model**: 모델 성능 평가 (Accuracy, F1-Score 등)
- **Predict**: 새로운 데이터 예측

#### ⚙️ Optimization
- **Hyperparameter Tuning**: GridSearch로 최적 파라미터 탐색

### 3. 노드 연결

노드의 출력(오른쪽 소켓)을 다음 노드의 입력(왼쪽 소켓)으로 연결

### 4. Python 코드 생성

상단 버튼 사용:
- **🐍 코드 보기**: 생성된 Python 코드 미리보기
- **📓 Jupyter**: Jupyter Notebook (.ipynb) 다운로드
- **📄 .py**: Python 스크립트 (.py) 다운로드

---

## 📖 예제: Iris 분류 파이프라인

### 노드 구성

```
Data Loader → Data Split → Scaler → Classifier → Evaluate
```

### 설정

1. **Data Loader**
   - File Type: CSV
   - Path: `iris.csv`

2. **Data Split**
   - Ratio: 0.8 (80% 훈련, 20% 테스트)

3. **Scaler**
   - Method: StandardScaler

4. **Classifier**
   - Algorithm: RandomForest
   - N Estimators: 100

5. **Evaluate**
   - (연결만 하면 자동 평가)

### 생성된 Python 코드

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ========================================
# ML Pipeline Auto-Generated Code
# ========================================

# Load Data
step_node_1 = pd.read_csv('iris.csv')  # File type: CSV
print(f"Data loaded: {step_node_1.shape}")

# Train/Test Split
X = step_node_1.drop('target', axis=1)  # Adjust 'target' column name
y = step_node_1['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

# Scale Features
step_node_3 = StandardScaler()
X_train_scaled = step_node_3.fit_transform(X_train)
X_test_scaled = step_node_3.transform(X_test)
print("Features scaled using StandardScaler")

# Train Classifier
step_node_4 = RandomForestClassifier(n_estimators=100, random_state=42)
step_node_4.fit(X_train_scaled, y_train)
print("Model trained: RandomForest")

# Evaluate Model
y_pred = step_node_4.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ========================================
# Pipeline Complete!
# ========================================
```

---

## 🎓 교육적 활용

### 1. ML 입문자용
- 코드 작성 없이 ML 파이프라인 개념 학습
- 각 단계의 역할과 순서 이해
- 생성된 코드로 실제 구현 방법 학습

### 2. 프로토타이핑
- 빠른 파이프라인 테스트
- 다양한 모델/파라미터 비교
- 최적 구성 탐색

### 3. 코드 학습
- 시각적 구성 → Python 코드 변환 과정 이해
- sklearn API 사용법 학습
- Jupyter Notebook으로 인터랙티브 실습

---

## 🆚 Teachable Machine과의 차이점

| 기능 | Teachable Machine | ML Pipeline Builder |
|------|-------------------|---------------------|
| 타겟 사용자 | 완전 초보자 | 초보~중급 개발자 |
| 커스터마이징 | 제한적 (3가지 모델만) | 자유로운 파이프라인 구성 |
| 코드 생성 | ❌ 없음 | ✅ Python/Jupyter 생성 |
| 전처리 | 자동 | 직접 선택 가능 |
| 모델 선택 | 고정 (이미지/음성/포즈) | 다양한 sklearn 모델 |
| 하이퍼파라미터 | 숨겨짐 | 직접 설정 가능 |
| 학습 목적 | 체험형 | 교육형 (코드 학습) |

---

## 💡 고급 활용

### 앙상블 모델 구성

여러 Classifier 노드를 병렬로 구성하고 결과 비교

```
Data Loader → Data Split → Scaler ┬→ RandomForest → Evaluate
                                   ├→ SVM → Evaluate
                                   └→ LogisticRegression → Evaluate
```

### 하이퍼파라미터 튜닝

```
Data Loader → Data Split → Scaler → Hyperparameter Tuning → Evaluate
```

### Feature Engineering

```
Data Loader → Feature Selection → Scaler → Classifier → Evaluate
```

---

## 🔧 요구 사항

생성된 코드를 실행하려면:

```bash
pip install pandas numpy scikit-learn
```

Jupyter Notebook 실행:

```bash
pip install jupyter
jupyter notebook
```

---

## 📝 라이선스

MIT License

---

## 🤝 기여

이슈 및 Pull Request 환영합니다!

GitHub: https://github.com/enderpawar/2025_oss_term_project-22101203_-
