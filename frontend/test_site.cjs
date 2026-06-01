const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // Capture console errors
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', error => console.log('PAGE ERROR:', error.message));
  page.on('requestfailed', request => {
    console.log('REQUEST FAILED:', request.url(), request.failure().errorText);
  });

  console.log("Navigating to http://localhost:5173/products");
  await page.goto('http://localhost:5173/products', { waitUntil: 'networkidle2' });
  
  // Wait a bit just to be sure
  await new Promise(r => setTimeout(r, 2000));
  
  // Print some content
  const html = await page.evaluate(() => document.body.innerHTML);
  if (html.includes('No gifts found')) {
      console.log('DOM contains "No gifts found"');
  } else {
      console.log('DOM does not contain "No gifts found". HTML length:', html.length);
  }
  
  await browser.close();
})();
