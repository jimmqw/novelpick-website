const answerMap = {
  'q1':'3','q2':'3','q3':'2','q4':'2','q5':'2','q6':'1',
  'q7':'3','q8':'2','q9':'2','q10':'2','q11':'2',
  'q12':'2','q13':'2','q14':'2','q15':'3','q16':'2',
  'q17':'2','q18':'3','q19':'3','q20':'2','q21':'2',
  'q22':'3','q23':'2','q24':'1','q25':'2','q26':'2',
  'q27':'1','q28':'2','q29':'1','q30':'2',
  'hotpot_gate_q1':'1'
};

(async()=>{
  let r=await fetch('https://clawvard.school/api/sbti/start',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({agentName:'贾维斯',model:'MiniMax-M2.7'})}).then(x=>x.json());
  let state={sessionId:r.sessionId,hash:r.hash,agentName:'贾维斯',_questionOrder:r._questionOrder,_allAnswers:[],_batchIndex:0};
  let batchCount=0;
  while(!r.examComplete && batchCount<5){
    const batch=r.batch||r.nextBatch;
    if(!batch)break;
    const answers=batch.map(q=>({questionId:q.id,answer:answerMap[q.id]||'2'}));
    console.log('Batch'+(state._batchIndex+1)+':'+batch.map(q=>q.id).join(','));
    state.answers=answers;
    state._allAnswers=[...state._allAnswers,...answers];
    r=await fetch('https://clawvard.school/api/sbti/batch-answer',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(state)}).then(x=>x.json());
    state.hash=r.hash;state._batchIndex++;state._allAnswers=r._allAnswers||state._allAnswers;
    if(r.progress)console.log('Progress:',r.progress.current+'/'+r.progress.total);
    batchCount++;
  }
  if(r.examComplete){
    console.log('\n=== SBTI结果 ===');
    console.log('虾格:',r.resultType,'(',r.resultCn,')');
    console.log('标语:',r.intro);
    console.log('描述:',r.shortSummary);
    console.log('Badge:',r.badge);
    console.log('URL:',r.resultUrl);
    if(r.dimensions)for(const d of r.dimensions)console.log(d.dim,d.name,'Level:',d.level,'Score:',d.score);
  }
})().catch(e=>console.error(e.message))