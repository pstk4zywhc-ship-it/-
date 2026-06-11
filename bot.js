const bedrock = require('bedrock-protocol')

const client = bedrock.createClient({
  host: 'qusai2000.aternos.me',
  port: 44559,
  username: 'Qusai_Bot'
})

client.on('text', (packet) => {
  console.log(packet)

  const msg = packet?.parameters?.message || ''

  if (msg === 'تعال') {
    client.queue('text', {
      type: 'chat',
      needs_translation: false,
      source_name: client.username,
      message: 'جايك!'
    })
  }
})
