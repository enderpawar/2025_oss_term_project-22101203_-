import React, { useState } from 'react';

/**
 * 초보자를 위한 가이드 컴포넌트
 */
const BeginnerGuide = () => {
    const [isExpanded, setIsExpanded] = useState(false);

    const socketGuide = [
        {
            name: 'data',
            color: '#3b82f6',
            description: '로드된 원본 데이터 (DataFrame)'
        },
        {
            name: 'X_train',
            color: '#10b981',
            description: '훈련용 피처 데이터'
        },
        {
            name: 'y_train',
            color: '#8b5cf6',
            description: '훈련용 타겟 데이터'
        },
        {
            name: 'X_test',
            color: '#f59e0b',
            description: '테스트용 피처 데이터'
        },
        {
            name: 'y_test',
            color: '#ef4444',
            description: '테스트용 타겟 데이터'
        },
        {
            name: 'model',
            color: '#ec4899',
            description: '학습된 ML 모델'
        },
        {
            name: 'prediction',
            color: '#06b6d4',
            description: '모델의 예측 결과'
        },
        {
            name: 'metrics',
            color: '#6366f1',
            description: '모델 성능 평가 지표'
        }
    ];

    const commonPipelines = [
        {
            title: '기본 ML 파이프라인',
            steps: [
                '1️⃣ Data Loader: CSV 파일 로드',
                '2️⃣ Data Split: 훈련/테스트 분할',
                '3️⃣ Scaler: 데이터 정규화',
                '4️⃣ Classifier/Regressor: 모델 학습',
                '5️⃣ Evaluate: 성능 평가'
            ]
        },
        {
            title: '피처 엔지니어링 포함',
            steps: [
                '1️⃣ Data Loader',
                '2️⃣ Data Split',
                '3️⃣ Scaler',
                '4️⃣ Feature Selection: 중요 피처 선택',
                '5️⃣ Classifier/Regressor',
                '6️⃣ Evaluate'
            ]
        }
    ];

    return (
        <div className="p-4 bg-neutral-900/60 rounded-2xl border border-neutral-800/70">
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between text-left"
            >
                <h3 className="text-lg font-semibold text-blue-400 flex items-center gap-2">
                    📚 초보자 가이드
                </h3>
                <span className="text-gray-400">
                    {isExpanded ? '▼' : '▶'}
                </span>
            </button>

            {isExpanded && (
                <div className="mt-4 space-y-4">
                    {/* 소켓 색상 가이드 */}
                    <div className="p-3 bg-neutral-800/50 rounded-lg">
                        <h4 className="text-sm font-semibold text-gray-200 mb-3">
                            🔌 소켓 타입 가이드
                        </h4>
                        <div className="space-y-2">
                            {socketGuide.map((socket, idx) => (
                                <div key={idx} className="flex items-center gap-2 text-xs">
                                    <div 
                                        className="w-3 h-3 rounded-full"
                                        style={{ backgroundColor: socket.color }}
                                    />
                                    <code className="font-mono text-cyan-300 font-semibold">
                                        {socket.name}
                                    </code>
                                    <span className="text-gray-400">-</span>
                                    <span className="text-gray-300">
                                        {socket.description}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* 연결 규칙 */}
                    <div className="p-3 bg-neutral-800/50 rounded-lg">
                        <h4 className="text-sm font-semibold text-gray-200 mb-2">
                            🔗 연결 규칙
                        </h4>
                        <ul className="text-xs text-gray-300 space-y-1 list-disc list-inside">
                            <li>같은 이름의 소켓끼리 연결하세요</li>
                            <li>예: <code className="text-cyan-300">X_train</code> → <code className="text-cyan-300">X_train</code></li>
                            <li>출력 소켓에서 입력 소켓으로 드래그</li>
                            <li>한 출력은 여러 입력에 연결 가능</li>
                        </ul>
                    </div>

                    {/* 일반적인 파이프라인 */}
                    <div className="p-3 bg-neutral-800/50 rounded-lg">
                        <h4 className="text-sm font-semibold text-gray-200 mb-2">
                            🔄 일반적인 파이프라인
                        </h4>
                        {commonPipelines.map((pipeline, idx) => (
                            <div key={idx} className="mb-3 last:mb-0">
                                <div className="text-xs font-semibold text-blue-400 mb-1">
                                    {pipeline.title}
                                </div>
                                <ul className="text-xs text-gray-300 space-y-0.5">
                                    {pipeline.steps.map((step, stepIdx) => (
                                        <li key={stepIdx} className="ml-2">
                                            {step}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        ))}
                    </div>

                    {/* 팁 */}
                    <div className="p-3 bg-blue-900/20 border border-blue-700/30 rounded-lg">
                        <div className="text-xs text-blue-300 space-y-1">
                            <div><strong>💡 팁:</strong></div>
                            <ul className="list-disc list-inside ml-2 space-y-1">
                                <li>노드를 클릭하면 설정 변경 가능</li>
                                <li>연결을 더블클릭하면 삭제됩니다</li>
                                <li>빠른 시작 템플릿으로 시작하세요</li>
                                <li>AI 생성 기능으로 자동 구성 가능</li>
                            </ul>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default BeginnerGuide;
