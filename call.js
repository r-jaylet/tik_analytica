const { TTScraper } = require("tiktok-scraper-ts");
var fs = require('fs');

const TikTokScraper = new TTScraper();

module.exports.get_user = function (username) {
  TikTokScraper.user(username)
      .then(fetchUser => {
        const jsonObj = JSON.stringify(fetchUser);
        console.log(jsonObj);
      })
      .catch(error => {console.error(error);});
}

module.exports.get_user_videos = function (username) {
  TikTokScraper.getAllVideosFromUser(username)
      .then(fetchUser => {
        const jsonObj = JSON.stringify(fetchUser);
        console.log(jsonObj);
      })
      .catch(error => {console.error(error);});
}

module.exports.get_hashtag = function (tag) {
  TikTokScraper.hashTag(tag)
      .then(fetchHashtag => {
        const jsonObj = JSON.stringify(fetchHashtag);
        console.log(jsonObj);
      })
      .catch(error => {console.error(error);});
}

module.exports.get_music = function (url) {
  TikTokScraper.getMusic(url)
      .then(fetchMusic => {
        const jsonObj = JSON.stringify(fetchMusic);
        console.log(jsonObj);
      })
      .catch(error => {console.error(error);});
}
