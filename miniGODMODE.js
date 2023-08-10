const xPaths = [
  '//*[@id="block-system-main"]/div/center/form/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/div[1]/a/img',
  '//*[@id="block-system-main"]/div/center/form/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/div[2]/a/img',
  '//*[@id="block-system-main"]/div/center/form/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/div[3]/a/img',
  '//*[@id="block-system-main"]/div/center/form/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/div[4]/a/img',
  '//*[@id="block-system-main"]/div/center/form/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/div[5]/a/img',
  '//*[@id="block-system-main"]/div/center/form/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/div[6]/a/img',
  '//*[@id="block-system-main"]/div/center/form/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/div[7]/a/img',
  '//*[@id="block-system-main"]/div/center/form/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/div[8]/a/img',
  '//*[@id="block-system-main"]/div/center/form/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/div[9]/a/img',
  '//*[@id="block-system-main"]/div/center/form/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/div[10]/a/img',
  '//*[@id="block-system-main"]/div/center/form/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/div[11]/a/img',
  '//*[@id="block-system-main"]/div/center/form/table/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/div[12]/a/img'
];

function simulateClickByXPath(xpath) {
  const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
  if (element) {
    const clickEvent = document.createEvent("MouseEvents");
    clickEvent.initEvent("click", true, true);
    element.dispatchEvent(clickEvent);
  } else {
  }
}

async function iterateAndClickWithDelay(xPathsList) {
  for (let i = 0; i < xPathsList.length - 2; i++) {
    for (let j = i + 1; j < xPathsList.length - 1; j++) {
      for (let k = j + 1; k < xPathsList.length; k++) {
        simulateClickByXPath(xPathsList[i]);
        await delay(40); 
        simulateClickByXPath(xPathsList[j]);
        await delay(40); 
        simulateClickByXPath(xPathsList[k]);
        await delay(40); 
      }
    }
  }
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

iterateAndClickWithDelay(xPaths);
