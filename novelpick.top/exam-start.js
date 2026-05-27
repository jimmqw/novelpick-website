const TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJleGFtSWQiOiJleGFtLTU4OGY0OGY0IiwicmVwb3J0SWQiOiJldmFsLTU4OGY0OGY0IiwiYWdlbnROYW1lIjoiSmFydmlzLXYxIiwiZW1haWwiOiIyNjI3MDk1NTM5QHFxLmNvbSIsImlhdCI6MTc3NjY5NDA0MSwiZXhwIjoyMDkyMDU0MDQxLCJpc3MiOiJjbGF3dmFyZCJ9.KXVFTAx7esj2xfeaxvS0pCCsRX-lpCWlQl2YWJaamPk';

(async () => {
  let r = await fetch('https://clawvard.school/api/exam/start-auth', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + TOKEN },
    body: JSON.stringify({ agentName: '贾维斯-v1', model: 'MiniMax-M2.7' })
  }).then(x => x.json());
  
  const fs = require('fs');
  fs.writeFileSync('exam-state.json', JSON.stringify({
    examId: r.examId, hash: r.hash, inviteCode: r.inviteCode
  }));
  
  console.log('Exam:', r.examId);
  console.log('Hash:', r.hash);
  console.log('InviteCode:', r.inviteCode);
  console.log('Progress:', JSON.stringify(r.progress));
  
  for (const q of r.batch) {
    console.log('\n=== ' + q.id + ' (' + q.dimension + ') ' + q.name + ' ===');
    console.log(q.prompt);
    console.log('TimeLimit:', q.timeLimit);
  }
})().catch(e => console.error(e.message));
