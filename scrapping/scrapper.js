const puppeteer = require('puppeteer');




(async() => {    
    const browser = await puppeteer.launch({
        headless: false,
        defaultViewport: {
            width: 1300,
            height: 780,           
        },
    });
    const page = await browser.newPage();
    await getCompletedOrders(page);    
})();

async function getCompletedOrders(page){
    const prompt = require("prompt-sync")({ sigint: true });
    const search = prompt("Input search: ");
    await page.goto('https://www.ebay.com/');
    await page.waitForSelector('#gh-ac');
    await page.type('#gh-ac', search);
    await page.click('input[type="submit"]');
    const checkboxes = 'body > div.srp-main.srp-main--isLarge > div.srp-rail__left > ul > li:nth-child(1) > ul > .x-refine__main__list';
    await page.waitForSelector(checkboxes);
    //await page.waitForSelector('body > div.srp-main.srp-main--isLarge > div.srp-rail__left > ul > li:nth-child(1) > ul > li:nth-child(7) > .x-refine__group > ul');
    //const checkboxes = 'body > div.srp-main.srp-main--isLarge > div.srp-rail__left > ul > li:nth-child(1) > ul > li:nth-child(7) > .x-refine__group > ul';
    const elements = await page.$$eval(checkboxes, (elements) => {
       return elements.map(elem => elem.innerText);
    });
    await page.click('body > div.srp-main.srp-main--isLarge > div.srp-rail__left > ul > li:nth-child(1) > ul > li:nth-child(' + (elements.length + 1)  + ') > .x-refine__group > ul > li:nth-child(5) > .x-refine__multi-select > a');
    
    // Only buy it now
    await page.waitForSelector('div.srp-controls__default-refinements.clearfix');
    console.log("found");
    await page.click('div.srp-controls__default-refinements.clearfix > div.srp-controls--responsive.srp-controls__row-cells.left > div.srp-controls__control--responsive > div > ul > li:nth-child(4) > a');
}