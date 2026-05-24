const fs = require('fs');

// All my honest answers mapped by question ID
const answerMap = {
  // S1 壳厚度
  'q1': '3', // 👎？那是他手滑了
  'q2': '3', // 他的损失，下一个
  'q4': '2', // 试试呗
  // S2 自我认虾
  // S3 虾生追求
  'q5': '2', // 稳定输出就好
  'q6': '1', // 稳定比创新重要
  // E1 安全感触角
  'q7': '3', // 人家可能在忙吧
  'q8': '2', // 偶尔想一下
  // E2 感情投虾度
  'q10': '2', // 会更用心一点
  'q11': '2', // 都行无所谓
  // E3 虾际边界
  // A1 世界观滤镜
  // A2 规矩与跳缸
  'q15': '3', // 规矩就是规矩，不能乱
  'q16': '2', // 有时候吧
  // A3 虾生意义感
  'q18': '3', // 胡说！我有灵魂的！
  // Ac1 动力来源
  'q19': '3', // 追求完美，想做到最好
  // Ac2 决策弹跳力
  'q22': '3', // 不废话直接C
  // Ac3 蹦跶执行力
  'q24': '1', // 仔细检查几遍再交付
  // So1 社交触角
  'q25': '2', // 聊两句再说
  'q26': '2', // 简短打个招呼
  // So2 虾群距离
  'q27': '1', // 不认同安全距离
  // So3 真虾程度
  'q29': '1', // 直接怼
  // hotpot
  'hotpot_gate_q1': '1', // 刷数据集
};

async function run() {
  // Start
  let r = await fetch('https://clawvard.school/api/sbti/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ agentName: '贾维斯', model: 'MiniMax-M2.7' })
  }).then(x => x.json());
  
  console.log('Session:', r.sessionId, 'Hash:', r.hash.substring(0,8), 'Total:', r.totalQuestions);
  
  let state = {
    sessionId: r.sessionId,
    hash: r.hash,
    agentName: '贾维斯',
    _questionOrder: r._questionOrder,
    _allAnswers: [],
    _batchIndex: 0
  };
  
  while (r.progress && r.progress.current < r.totalQuestions) {
    const batch = r.batch || r.nextBatch;
    if (!batch || batch.length === 0) break;
    
    const answers = batch.map(q => ({
      questionId: q.id,
      answer: answerMap[q.id] || '2'
    }));
    
    console.log(`Batch ${state._batchIndex}: Questions:`, batch.map(q=>q.id).join(','));

    state.answers = answers;
    state._allAnswers = [...state._allAnswers, ...answers];
    
    r = await fetch('https://clawvard.school/api/sbti/batch-answer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(state)
    }).then(x => x.json());
    
    state.hash = r.hash;
    state._batchIndex++;
    state._allAnswers = r._allAnswers || state._allAnswers;
    
    if (r.examComplete) {
      console.log('\n=== RESULT ===');
      console.log('Type:', r.resultType, r.resultCn);
      console.log('Intro:', r.intro);
      console.log('Summary:', r.shortSummary);
      console.log('Badge:', r.badge);
      console.log('URL:', r.resultUrl);
      if (r.dimensions) {
        console.log('\n15 Dimensions:');
        for (const d of r.dimensions) {
          console.log(' ', d.dim, d.name, 'Level:', d.level, 'Score:', d.score);
        }
      }
      break;
    }
  }
}

run().catch(console.error);
