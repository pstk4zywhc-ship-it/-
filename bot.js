const mineflayer = require('mineflayer')

const bot = mineflayer.createBot({
  host: 'localhost',
  port: 25565,
  username: 'AI_Bot'
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

  bot.chat('سمعت: ' + message)
})
