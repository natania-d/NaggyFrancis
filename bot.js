var token = '424538023:AAG_WU0hiDPABPFKnm94UiatzjUFOuA6CP0';

var Bot = require('node-telegram-bot-api'),
    bot = new Bot(token, { polling: true });

console.log('bot server started...');

bot.onText(/^\/say_hello (.+)$/, function (msg, match) {
  var name = match[1];
  bot.sendMessage(msg.chat.id, 'Hello ' + name + '!').then(function () {
    // reply sent!
  });
});

bot.onText(/^\/sum((\s+\d+)+)$/, function (msg, match) {
  var result = 0;
  match[1].trim().split(/\s+/).forEach(function (i) {
    result += (+i || 0);
  })
  bot.sendMessage(msg.chat.id, result);
});



bot.onText(/\/inline/, function(msg, match) {
  var text = 'Telegram bot sucks';
 
  var keyboardStr = JSON.stringify({
      inline_keyboard: [
        [
          {text:'Get good',callback_data:'sandwich'},
          {text:'Weh',callback_data:'steak1'}
        ]
      ]
  });
 
  var keyboard = {reply_markup: JSON.parse(keyboardStr)};
  bot.sendMessage(msg.chat.id, text, keyboard);
});


bot.on('callback_query', function (msg) {
  bot.answerCallbackQuery(msg.id, 'You hit a button!', false);
  bot.editMessageText(msg.chat.id, msg.id, "edited! :)")
});







