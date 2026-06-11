
const mineflayer = require('mineflayer')

const bot = mineflayer.createBot({
  host: 'localhost',   // لاحقًا تغيّرها لسيرفر حقيقي
  port: 25565,
  username: 'Qusai'
})

bot.on('chat', (username, message) => {
  if (username === bot.username) return

  if (message === 'تعال') {
    bot.chat('جايك!')
  }

  if (message === 'اقف') {
    bot.chat('وقفت')
    bot.clearControlStates()
  }
})
