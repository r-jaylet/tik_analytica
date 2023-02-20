const { TTScraper } = require("tiktok-scraper-ts");
var fs = require('fs');

const TikTokScraper = new TTScraper();

module.exports.get_user = function (username) {
  TikTokScraper.user(username)
      .then(fetchUser => {
        console.log(fetchUser);
      })
      .catch(error => {console.error(error);});
}

module.exports.get_user_videos = function (username) {
  TikTokScraper.getAllVideosFromUser(username)
      .then(fetchUser => {
        console.log(fetchUser);
      })
      .catch(error => {console.error(error);});
}

module.exports.get_hashtag = function (tag) {
  TikTokScraper.hashTag(tag)
      .then(fetchHashtag => {
        console.log(fetchHashtag);
      })
      .catch(error => {console.error(error);});
}

module.exports.get_music = function (url) {
  TikTokScraper.getMusic(url)
      .then(fetchMusic => {
        console.log(fetchMusic);
      })
      .catch(error => {console.error(error);});
}
