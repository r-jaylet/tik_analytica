const { TTScraper } = require("tiktok-scraper-ts");

const TikTokScraper = new TTScraper();

(async () => {
  const fetchVideo = await TikTokScraper.getAllVideosFromUser("anica_heree"); // second argument set to true to fetch the video without watermark
  console.log(fetchVideo);
})();
