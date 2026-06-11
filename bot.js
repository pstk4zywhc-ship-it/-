const bedrock = require('bedrock-protocol')

const client = bedrock.createClient({
  host: 'qusai2000.aternos.me',
  port: 44559,
  username: 'Qusai_Bot'
})

function chat(msg) {
  client.queue('text', {
    type: 'chat',
    needs_translation: false,
    source_name: client.username,
    message: msg
  })
}

client.on('spawn', () => {
  console.log('Bot spawned!')
  chat('دخلت السيرفر 👋')
})

client.on('text', (packet) => {
  const msg = packet?.parameters?.message || ''

  console.log('Chat:', msg)

  // أوامر عربية
  if (msg === 'تعال') {
    chat('جايك!')
  }

  if (msg === 'خشب') {
    chat('ببدأ أجمع خشب 🌳')

    // حركة بسيطة (تقريب فكرة)
    setInterval(() => {
      client.queue('move_player', {
        movement: {
          x: Math.random() - 0.5,
          y: 0,
          z: Math.random() - 0.5
        }
      })
    }, 2000)
  }

  if (msg === 'قف') {
    chat('وقفت 🛑')
  }
})
