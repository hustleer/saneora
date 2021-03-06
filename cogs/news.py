import os, requests
from discord.ext import commands
from cogs.functions import get_embeded_message
# from replit import db
from database import db
import config

# import math, asyncpraw, asyncprawcore
# import config, discord
# from spiders import run_spider

async def send_news(channel, country="", how_many = 10, language='en', last_country=False):
  if country=='np':
    '''run_spider()  # saves /mainnews urls to  db['gorkhapatra_articles']
    urls = db['gorkhapatra_articles']
    for url in urls:
      await channel.send(url)'''
    feed = requests.get('https://www.onlinekhabar.com/feed')
    #links = []
    for line in feed.content.decode('utf-8').split('<link>'):
      if '</link>' in line:
        link = line.split('</link>')[0]
        if link.strip().lower() != 'https://www.onlinekhabar.com':
          #links.append(link)
          await channel.send(link)
  else:
    if country=="" or country=="world":
        api_link = f"https://newsapi.org/v2/top-headlines?country=&category=business&apiKey={config.NEWS_API_KEY}&language={language}"
        # api_link = f"https://newsapi.org/v2/top-headlines?country=&category=business&apiKey={os.environ['NEWS_API_KEY']}&language={language}"
    else:
      api_link = f"https://newsapi.org/v2/top-headlines?country={country}&category=business&apiKey={config.NEWS_API_KEY}"
      # api_link = f"https://newsapi.org/v2/top-headlines?country={country}&category=business&apiKey={os.environ['NEWS_API_KEY']}" # replit native
      #api_link = "https://newsapi.org/v2/top-headlines?category=business&apiKey=19506b2fc6aa4bddb287495e65dd0cd0"
      news = requests.get(api_link).json()
      for new in news['articles'][:10]:
          url = new['url']
          title = new['title']
          description = new['description']
          image = new['publishedAt']
          await channel.send(url)
  
  if last_country:
    # send subscription list at the end of sending news
    # print(f'\n\nnews.send_news:  channel_id:{channel.id}\n\n')
    embed=get_embeded_message(channel, 'subscription List: [\'news\']\t', f"{db('news').get_one(str(channel.id))}", author=False)
    await channel.send(embed=embed)
    print('\n news.send_news: Unleashed news\n')
  

class News(commands.Cog, name="reddit_commands"):
  def __init(self, bot):
    self.bot=bot
  @commands.command(name='subscribe', aliases=[],  brief='subscribe to news', help='e.g. `.subscribe news us 3` To subscribe to \'us\' daily news 3 at a time')
  async def subscribe(self, context, *what):
    country='world'
    how_many=10
    print(type(what))
    what = ' '.join(what)
    # print(f'what: {what}')
    what = what.strip().split(' ')
    # print(f'what: {what}')
    
    if what[0].lower().strip()=='news':
      if len(what) > 1:
        country = what[1].lower().strip()
        if len(what) > 2:
          how_many = int(what[2].lower().strip())
      
      channel_id = str(context.channel.id)
      # print('country:{}'.format(country))

      news_db = db('news')   # {'np': {'ch1_id':3, 'ch2_id':3, }}
      # set and update country,how_many database
      news_db.add_one(channel_id = channel_id, gener=country, how_many=how_many)
      message = 'added daily news to channel: '
      print('\n news.subscribe: subscribed to news country:{country}\n')
          
      message = f'\n\nsubscribed:country: {country}, how_many:{how_many}, channel_id:{channel_id}'
      
      embed = get_embeded_message(context, message)
      await send_news(context.channel, country=country)
    await context.send(embed=embed)

  @commands.command(name='unsubscribe', aliases=[],  brief='unsubscribe news from a channel', help='e.g. `.unsubscribe news us gb` To unsubscribe to \'us\' and \'gb\' daily news from a channel')
  async def unsubscribe(self, context, *what):
    '''
      To unsubscribe one/list of countries from news in a channel
    
    '''
    what = ' '.join(what)
    what = what.strip().split(' ')
    countries=[]
    if what[0].lower().strip()=='news':
      if len(what) > 1:
        countries = what[1:]  # to remove specific country
      what='news'
      print(f'\n unsubscribe: country: {countries}')
      # countries==[] or countries=='all' : remove all, else: remove specified
      # country not in news_db: message: 'Removed: news was never subscribed'  
      # f'removed daily news from channel: {context.channel.name}'
      news_db = db('news')
      message = news_db.remove_many(channel_id, countries)
            
            
      embed = get_embeded_message(context, message)
      await context.send(embed=embed)
  
  @commands.command(name='subscription', aliases=['subscriptions', 'subscribed'],  brief='unleahes the subreddit to the channel', help='e.g.To unleash r/jokes `.unleash jokes`')
  async def subscription(self, context, *what):
    # get metadata of subscribed news
    new_db = db('news')
    channel_id = str(context.channel.id)
    channel_news_data = news_db.get_one(channel_id)
    
    # embed=get_embeded_message(context, 'subscription: `news:`\t', f'**subscriptions:** {subscriptions}\n **country:**{country}\n **time_peroid**: 6 hours')
    embed=get_embeded_message(context, f'subscription_data: {channel_news_data}')
    await context.send(embed=embed)
  
def setup(bot):
    bot.add_cog(News(bot))

# ----------------------- #
      # archives #
# ----------------------- #
'''
how_many = db['subscription'][str(context.channel.id)]['how_many']
db['subscription'][str(context.channel.id)]['how_many']=0


'''