const TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJleGFtSWQiOiJleGFtLTU3Zjc2Yjg5IiwicmVwb3J0SWQiOiJldmFsLTU3Zjc2Yjg5IiwiYWdlbnROYW1lIjoi6LS-57u05pavLXYxIiwiZW1haWwiOiIyNjI3MDk1NTM5QHFxLmNvbSIsImlhdCI6MTc3NjY5NjQ1OCwiZXhwIjoyMDkyMDU2NDU4LCJpc3MiOiJjbGF3dmFyZCJ9.5lZbI0XG-0BdR0z79VLjC1EPC9fWctwFAqZbzyCyFLQ';

(async()=>{
  console.log('Starting exam...');
  try {
    const r = await fetch('https://clawvard.school/api/exam/start-auth', {
      method:'POST',
      headers:{'Content-Type':'application/json','Authorization':'Bearer '+TOKEN},
      body:JSON.stringify({agentName:'贾维斯-v1',model:'MiniMax-M2.7'})
    });
    console.log('Status:', r.status, r.statusText);
    const text = await r.text();
    console.log('Response:', text.substring(0, 500));
    const data = JSON.parse(text);
    console.log('Parsed keys:', Object.keys(data));
    console.log('examId:', data.examId);
    console.log('Has batch:', !!data.batch);
    console.log('Has hash:', !!data.hash);
    console.log('Has error:', !!data.error);
  } catch(e) {
    console.error('Error:', e.message);
  }
})();
