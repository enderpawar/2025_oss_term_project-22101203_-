# 🔬 노드 그래프 → Python 코드 변환 상세 설명

## 📊 1단계: 노드 그래프 데이터 구조

사용자가 만든 노드 그래프는 다음과 같은 JSON 형태로 저장됩니다:

```json
{
  "nodes": [
    {
      "id": "node_abc123",
      "label": "데이터 로더",
      "kind": "dataLoader",
      "position": { "x": 100, "y": 200 },
      "controls": {
        "fileType": "CSV",
        "path": "iris.csv"
      }
    },
    {
      "id": "node_def456",
      "label": "데이터 분할",
      "kind": "dataSplit",
      "position": { "x": 400, "y": 200 },
      "controls": {
        "ratio": 0.8
      }
    },
    {
      "id": "node_ghi789",
      "label": "정규화",
      "kind": "scaler",
      "position": { "x": 700, "y": 200 },
      "controls": {
        "method": "StandardScaler"
      }
    },
    {
      "id": "node_jkl012",
      "label": "분류기",
      "kind": "classifier",
      "position": { "x": 1000, "y": 200 },
      "controls": {
        "algorithm": "RandomForest",
        "n_estimators": 100
      }
    },
    {
      "id": "node_mno345",
      "label": "평가",
      "kind": "evaluate",
      "position": { "x": 1300, "y": 200 },
      "controls": {}
    }
  ],
  "connections": [
    {
      "id": "conn_1",
      "source": "node_abc123",
      "target": "node_def456",
      "sourceOutput": "data",
      "targetInput": "data"
    },
    {
      "id": "conn_2",
      "source": "node_def456",
      "target": "node_ghi789",
      "sourceOutput": "train",
      "targetInput": "data"
    },
    {
      "id": "conn_3",
      "source": "node_ghi789",
      "target": "node_jkl012",
      "sourceOutput": "scaled",
      "targetInput": "train"
    },
    {
      "id": "conn_4",
      "source": "node_jkl012",
      "target": "node_mno345",
      "sourceOutput": "model",
      "targetInput": "model"
    }
  ]
}
```

---

## 🔄 2단계: Topological Sort (실행 순서 결정)

노드들을 **의존성 순서대로** 정렬합니다. (방향성 비순환 그래프 정렬)

### 알고리즘:

```typescript
function topologicalSort(nodes, connections) {
    // 1. 그래프 구조 만들기
    const graph = new Map()      // node → [children]
    const inDegree = new Map()   // node → incoming edge count
    
    nodes.forEach(node => {
        graph.set(node.id, [])
        inDegree.set(node.id, 0)
    })
    
    // 2. 연결 정보로 그래프 채우기
    connections.forEach(conn => {
        graph.get(conn.source).push(conn.target)
        inDegree.set(conn.target, inDegree.get(conn.target) + 1)
    })
    
    // 3. 진입 차수가 0인 노드들로 시작 (루트 노드)
    const queue = []
    inDegree.forEach((degree, nodeId) => {
        if (degree === 0) queue.push(nodeId)
    })
    
    // 4. 큐에서 하나씩 꺼내면서 정렬
    const sorted = []
    while (queue.length > 0) {
        const nodeId = queue.shift()
        sorted.push(nodeId)
        
        // 자식 노드들의 진입 차수 감소
        graph.get(nodeId).forEach(childId => {
            const newDegree = inDegree.get(childId) - 1
            inDegree.set(childId, newDegree)
            if (newDegree === 0) queue.push(childId)
        })
    }
    
    return sorted  // ["node_abc123", "node_def456", "node_ghi789", "node_jkl012", "node_mno345"]
}
```

### 실행 순서 결과:

```
1. node_abc123 (데이터 로더) - 의존성 없음
2. node_def456 (데이터 분할) - 데이터 로더에 의존
3. node_ghi789 (정규화)     - 데이터 분할에 의존
4. node_jkl012 (분류기)     - 정규화에 의존
5. node_mno345 (평가)       - 분류기에 의존
```

---

## 🎯 3단계: 각 노드를 Python 코드로 변환

각 노드 타입별로 **템플릿 코드**를 생성합니다.

### 예시 1: Data Loader 노드

**입력:**
```json
{
  "id": "node_abc123",
  "kind": "dataLoader",
  "controls": {
    "fileType": "CSV",
    "path": "iris.csv"
  }
}
```

**생성되는 코드:**
```python
# Load Data
step_node_abc123 = pd.read_csv('iris.csv')  # File type: CSV
print(f"Data loaded: {step_node_abc123.shape}")
```

**변환 함수:**
```typescript
case 'dataLoader': {
    const fileType = node.controls.fileType || 'CSV'
    const path = node.controls.path || 'data.csv'
    const varName = `step_${node.id.replace(/[^a-zA-Z0-9]/g, '_')}`
    
    return `# Load Data
${varName} = pd.read_csv('${path}')  # File type: ${fileType}
print(f"Data loaded: {${varName}.shape}")`
}
```

---

### 예시 2: Data Split 노드

**입력:**
```json
{
  "id": "node_def456",
  "kind": "dataSplit",
  "controls": {
    "ratio": 0.8
  }
}
```

**연결 정보:**
```json
{
  "source": "node_abc123",
  "target": "node_def456",
  "sourceOutput": "data",
  "targetInput": "data"
}
```

**생성되는 코드:**
```python
# Train/Test Split
X = step_node_abc123.drop('target', axis=1)  # Adjust 'target' column name
y = step_node_abc123['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
```

**변환 함수:**
```typescript
case 'dataSplit': {
    const ratio = node.controls.ratio || 0.8
    
    // 이전 노드의 출력 찾기
    const inputConn = connections.find(c => 
        c.target === node.id && c.targetInput === 'data'
    )
    const sourceVar = inputConn 
        ? `step_${inputConn.source.replace(/[^a-zA-Z0-9]/g, '_')}` 
        : 'data'
    
    return `# Train/Test Split
X = ${sourceVar}.drop('target', axis=1)
y = ${sourceVar}['target']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=${1 - ratio}, random_state=42
)
print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")`
}
```

---

### 예시 3: Classifier 노드

**입력:**
```json
{
  "id": "node_jkl012",
  "kind": "classifier",
  "controls": {
    "algorithm": "RandomForest",
    "n_estimators": 100
  }
}
```

**생성되는 코드:**
```python
# Train Classifier
step_node_jkl012 = RandomForestClassifier(n_estimators=100, random_state=42)
step_node_jkl012.fit(X_train_scaled, y_train)
print("Model trained: RandomForest")
```

**변환 함수:**
```typescript
case 'classifier': {
    const algorithm = node.controls.algorithm || 'RandomForest'
    const nEstimators = node.controls.n_estimators || 100
    const varName = `step_${node.id.replace(/[^a-zA-Z0-9]/g, '_')}`
    
    let modelCode = ''
    if (algorithm === 'RandomForest') {
        modelCode = `RandomForestClassifier(n_estimators=${nEstimators}, random_state=42)`
    } else if (algorithm === 'LogisticRegression') {
        modelCode = `LogisticRegression(random_state=42)`
    } else if (algorithm === 'SVM') {
        modelCode = `SVC(random_state=42)`
    }
    
    return `# Train Classifier
${varName} = ${modelCode}
${varName}.fit(X_train_scaled, y_train)
print("Model trained: ${algorithm}")`
}
```

---

## 🔗 4단계: Import 문 자동 생성

사용된 노드 타입을 기반으로 필요한 라이브러리를 자동으로 import합니다.

```typescript
function generateImports(nodes) {
    const imports = new Set()
    
    imports.add('import pandas as pd')
    imports.add('import numpy as np')
    
    nodes.forEach(node => {
        switch (node.kind) {
            case 'dataSplit':
                imports.add('from sklearn.model_selection import train_test_split')
                break
            case 'scaler':
                imports.add('from sklearn.preprocessing import StandardScaler, MinMaxScaler')
                break
            case 'classifier':
                imports.add('from sklearn.ensemble import RandomForestClassifier')
                imports.add('from sklearn.linear_model import LogisticRegression')
                imports.add('from sklearn.svm import SVC')
                break
            case 'evaluate':
                imports.add('from sklearn.metrics import accuracy_score, classification_report, confusion_matrix')
                break
        }
    })
    
    return Array.from(imports).join('\n')
}
```

---

## 📝 5단계: 최종 코드 조립

```typescript
function generatePythonCode(graph) {
    // 1. ML 노드만 필터링
    const mlNodes = graph.nodes.filter(n => 
        ['dataLoader', 'dataSplit', 'scaler', 'classifier', 'evaluate'].includes(n.kind)
    )
    
    // 2. 실행 순서 정렬
    const sortedNodes = topologicalSort(mlNodes, graph.connections)
    
    // 3. Import 문 생성
    const imports = generateImports(mlNodes)
    
    // 4. 각 노드를 코드로 변환
    const codeBlocks = sortedNodes.map(node => 
        nodeToCode(node, graph.connections)
    )
    
    // 5. 최종 조립
    return `${imports}

# ========================================
# ML Pipeline Auto-Generated Code
# ========================================

${codeBlocks.join('\n\n')}

# ========================================
# Pipeline Complete!
# ========================================
`
}
```

---

## 🎯 실제 예시: 위 그래프의 최종 출력

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ========================================
# ML Pipeline Auto-Generated Code
# ========================================

# Load Data
step_node_abc123 = pd.read_csv('iris.csv')  # File type: CSV
print(f"Data loaded: {step_node_abc123.shape}")

# Train/Test Split
X = step_node_abc123.drop('target', axis=1)
y = step_node_abc123['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

# Scale Features
step_node_ghi789 = StandardScaler()
X_train_scaled = step_node_ghi789.fit_transform(X_train)
X_test_scaled = step_node_ghi789.transform(X_test)
print("Features scaled using StandardScaler")

# Train Classifier
step_node_jkl012 = RandomForestClassifier(n_estimators=100, random_state=42)
step_node_jkl012.fit(X_train_scaled, y_train)
print("Model trained: RandomForest")

# Evaluate Model
y_pred = step_node_jkl012.predict(X_test_scaled)
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

## 🔧 핵심 알고리즘 정리

### 1. **Topological Sort (위상 정렬)**
- **목적**: 노드 실행 순서 결정
- **입력**: 노드 목록 + 연결 목록
- **출력**: 정렬된 노드 ID 배열
- **복잡도**: O(V + E) - V: 노드 수, E: 연결 수

### 2. **Template-based Code Generation**
- **목적**: 각 노드를 Python 코드로 변환
- **방법**: Switch-case로 노드 타입별 템플릿 선택
- **변수 이름**: `step_${nodeId}` 형식으로 고유하게 생성

### 3. **Variable Tracking (변수 추적)**
- **목적**: 노드 간 데이터 흐름 파악
- **방법**: 연결 정보에서 source 노드의 변수명 찾기
- **예**: `X_train_scaled = scaler.fit_transform(X_train)`

### 4. **Dependency Resolution (의존성 해결)**
- **목적**: 필요한 라이브러리 자동 import
- **방법**: 사용된 노드 타입 분석
- **최적화**: Set 사용으로 중복 제거

---

## 💡 추가 고급 기능

### 1. 순환 참조 감지
```typescript
if (sorted.length !== nodes.length) {
    throw new Error('Circular dependency detected in pipeline!')
}
```

### 2. 변수명 충돌 방지
```typescript
const varName = `step_${node.id.replace(/[^a-zA-Z0-9]/g, '_')}`
// node_abc-123 → step_node_abc_123
```

### 3. 에러 처리
```typescript
try {
    const code = generatePythonCode(graph)
} catch (error) {
    console.error('Code generation failed:', error)
    return '# Error: Unable to generate code'
}
```

---

## 🎓 학습 포인트

1. **그래프 이론**: Topological Sort는 DAG(방향성 비순환 그래프)에서 의존성 순서를 찾는 표준 알고리즘
2. **템플릿 패턴**: 노드 타입별 코드 템플릿으로 확장성 확보
3. **메타프로그래밍**: 코드를 생성하는 코드 작성
4. **AST 개념**: 추후 더 정교한 파싱을 위해 Abstract Syntax Tree 활용 가능

---

**파일 위치:**
- `src/utils/pipelineToCode.ts` - 코드 생성 엔진
- `src/rete/app-editor.ts` - 그래프 export/import
- `src/components/LogicEditorPage.jsx` - UI 통합
