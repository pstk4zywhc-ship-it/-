const bedrock = require('bedrock-protocol')
const OpenAI = require('openai')

const client = new OpenAI({
  apiKey: "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"
})

const bot = bedrock.createClient({
  host: 'qusai2000.aternos.me',
  port: 44559,
  username: 'GPT_Bot'
})

function chat(msg) {
  bot.queue('text', {
    type: 'chat',
    needs_translation: false,
    source_name: bot.username,
    message: msg
  })
}

async function askGPT(message) {
  const response = await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      {
        role: "system",
        content: `
أنت دماغ بوت داخل ماينكرافت.
حوّل كلام اللاعب إلى أوامر فقط:

الأوامر:
- follow
- stop
- wood
- wander

ارجع JSON فقط مثل:
{"action":"follow"}
        `
      },
      {
        role: "user",
        content: message
      }
    ]
  })

  return JSON.parse(response.choices[0].message.content)
}

// حركة بسيطة
let interval

function wander() {
  clearInterval(interval)
  interval = setInterval(() => {
    bot.queue('move_player', {
      movement: {
        x: Math.random() - 0.5,
        y: 0,
        z: Math.random() - 0.5
      }
    })
  }, 1500)
}

bot.on('spawn', () => {
  chat('🤖 ChatGPT Bot جاهز!')
})

bot.on('text', async (packet) => {
  const msg = packet?.parameters?.message || ''
  console.log("User:", msg)

  try {
    const result = await askGPT(msg)

    if (result.action === 'follow') {
      chat('👣 ببدأ أتابعك')
      clearInterval(interval)
    }

    else if (result.action === 'wood') {
      chat('🌳 بجمع خشب')
      wander()
    }

    else if (result.action === 'stop') {
      chat('🛑 توقفت')
      clearInterval(interval)
    }

    else if (result.action === 'wander') {
      chat('🚶 أتمشى')
      wander()
    }

  } catch (e) {
    chat('صار خطأ في الذكاء الاصطناعي')
    console.log(e)
  }
})
