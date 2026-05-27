const SocksClient = require('socks').SocksClient;
const https = require('https');
const fs = require('fs');
const cfg = JSON.parse(fs.readFileSync('C:/Users/Administrator/.openclaw/openclaw.json','utf8'));
const key = cfg.models.providers['openai-302'].apiKey;

async function main() {
  try {
    console.log('Connecting via SOCKS5...');
    const info = await SocksClient.createConnection({
      proxy: { host: '127.0.0.1', port: 7891, type: 5 },
      command: 'connect',
      destination: { host: 'api.302.ai', port: 443 },
      timeout: 20000
    });
    console.log('SOCKS5 connected!');

    const postData = JSON.stringify({
      model: 'gpt-image-2',
      prompt: 'A panoramic view of Badain Jaran Desert, golden sand dunes under sunset, photorealistic',
      n: 1,
      size: '1792x1024'
    });

    console.log('Sending HTTPS request...');
    const req = https.request({
      socket: info.socket,
      hostname: 'api.302.ai',
      path: '/v1/images/generations',
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + key,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'Host': 'api.302.ai',
        'Connection': 'close'
      },
      timeout: 45000,
      rejectUnauthorized: false
    }, (res) => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        console.log('Status:', res.statusCode);
        console.log('Response:', d);
        if (d.length > 100) console.log('(truncated to 500)', d.substring(0,500));
      });
    });
    req.on('error', e => {
      console.log('HTTPS Error:', e.code, e.message);
      info.socket.destroy();
    });
    req.on('timeout', () => {
      console.log('HTTPS timeout');
      req.destroy();
      info.socket.destroy();
    });
    req.write(postData);
    req.end();
  } catch(e) {
    console.log('SOCKS Error:', e.name, e.message.substring(0,200));
  }
}
main();
