const { TTScraper } = require("tiktok-scraper-ts");
const TikTokScraper = new TTScraper();


//https://www.tiktok.com/@canalplus/video/7204508132628892934
(async () => {
  const fetchVideo = await TikTokScraper.getAllVideosFromUser("canalplus"); // second argument set to true to fetch the video without watermark
  console.log(fetchVideo);
})();
