const { TTScraper } = require("tiktok-scraper-ts");

const TikTokScraper = new TTScraper();


// Call user request to TikTok API
module.exports.get_user = function (username) {
  TikTokScraper.user(username)
      .then(fetchUser => {
        const jsonObj = JSON.stringify(fetchUser);
        console.log(jsonObj);
      })
      .catch(error => {console.error(error);});
}

// Call video request to TikTok API
module.exports.get_user_videos = function (username) {
  TikTokScraper.getAllVideosFromUser(username)
      .then(fetchUser => {
        const jsonObj = JSON.stringify(fetchUser);
        console.log(jsonObj);
      })
      .catch(error => {console.error(error);});
}

// Call hashtag request to TikTok API
module.exports.get_hashtag = function (tag) {
  TikTokScraper.hashTag(tag)
      .then(fetchHashtag => {
        const jsonObj = JSON.stringify(fetchHashtag);
        console.log(jsonObj);
      })
      .catch(error => {console.error(error);});
}

// Call music request to TikTok API
module.exports.get_music = function (url) {
  TikTokScraper.getMusic(url)
      .then(fetchMusic => {
        const jsonObj = JSON.stringify(fetchMusic);
        console.log(jsonObj);
      })
      .catch(error => {console.error(error);});
}
