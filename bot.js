const mineflayer = require('mineflayer')

const bot = mineflayer.createBot({
  host: 'localhost',   // غيّرها إلى IP السيرفر إذا عندك
  port: 25565,
  username: 'Qusai'
})

bot.on('spawn', () => {
  console.log('Bot spawned in game!')
})

bot.on('chat', (username, message) => {
  if (username === bot.username) return

  if (message === 'تعال') {
    bot.chat('جايك يا ' + username)
  }

  else if (message === 'اقف') {
    bot.chat('تمام وقفت')
    bot.clearControlStates()
  }

  else if (message === 'مرحبا') {
    bot.chat('هلا والله 👋')
  }

  else {
    bot.chat('فهمت: ' + message)
  }
})
