const bedrock = require('bedrock-protocol')

const client = bedrock.createClient({
  host: 'qusai2000.aternos.me',
  port: 44559,
  username: 'Qusai_AI'
})

function chat(msg) {
  client.queue('text', {
    type: 'chat',
    needs_translation: false,
    source_name: client.username,
    message: msg
  })
}

// 🧠 “دماغ AI بسيط”
function brain(msg) {
  msg = msg.toLowerCase()

  if (msg.includes('تعال')) return 'follow'
  if (msg.includes('خشب')) return 'wood'
  if (msg.includes('قف')) return 'stop'
  if (msg.includes('تجول')) return 'wander'

  return 'unknown'
}

// 🏃 حركة عشوائية (محاكاة ذكاء)
let interval

function wander() {
  clearInterval(interval)

  interval = setInterval(() => {
    client.queue('move_player', {
      movement: {
        x: (Math.random() - 0.5),
        y: 0,
        z: (Math.random() - 0.5)
      }
    })
  }, 1500)
}

client.on('spawn', () => {
  console.log('AI Bot online')
  chat('🤖 جاهز أساعدك!')
})

client.on('text', (packet) => {
  const msg = packet?.parameters?.message || ''
  console.log('User:', msg)

  const action = brain(msg)

  if (action === 'follow') {
    chat('تمام، بتبعك 👣')
    clearInterval(interval)
  }

  else if (action === 'wood') {
    chat('🌳 بجمع خشب الآن (تقريباً)...')
    wander()
  }

  else if (action === 'stop') {
    chat('🛑 وقفت')
    clearInterval(interval)
  }

  else if (action === 'wander') {
    chat('أتمشى شوي 🤖')
    wander()
  }

  else {
    chat('ما فهمت، جرب: تعال / خشب / قف')
  }
})
