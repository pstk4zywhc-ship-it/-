const bedrock = require('bedrock-protocol')

const bot = bedrock.createClient({
  host: 'qusai2000.aternos.me',
  port: 44559,
  username: 'Qusai_Bot'
})

bot.on('join', () => {
  console.log('Bot joined!')
})

bot.on('disconnect', (reason) => {
  console.log('Disconnected:', reason)
})

bot.on('error', (err) => {
  console.log('Error:', err)
})
