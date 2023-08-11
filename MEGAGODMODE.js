const targetURL = "http://www.setgame.com/sites/all/modules/setgame_set/assets/images/new";
const excludedImage = "http://www.setgame.com/sites/all/modules/setgame_set/assets/images/new/empty_card.gif";

const images = document.querySelectorAll('img');
const numberArray = [];

images.forEach((image, index) => {
    const src = image.src;
    if (src.startsWith(targetURL) && src !== excludedImage) {
        const startIndex = src.indexOf("new/") + 4; // "new/".length = 4
        const endIndex = src.indexOf(".png");
        if (startIndex !== -1 && endIndex !== -1) {
            const numberString = src.substring(startIndex, endIndex);
            const number = parseInt(numberString);
            if (!isNaN(number)) {
                numberArray.push(number);
            }
        }
    }
});

console.log("Array of integers extracted from the image URLs:");
console.log(numberArray);

let clickCounter = 0;

function clickTargetImage(number) {
    const targetImagePath = `/sites/all/modules/setgame_set/assets/images/new/${number}.png`;
    const targetImage = document.querySelector(`img[src="${targetImagePath}"]`);
    if (targetImage) {
        targetImage.click();
        clickCounter++;
        console.log("Clicked on image:", targetImagePath);
    } else {
        console.log("Image not found:", targetImagePath);
    }
}

function isSet(x, y, z) {
    for (let i = 0; i < 4; i++) {
        if (Math.floor((x - 1) / (3 ** i)) % 3 == Math.floor((y - 1) / (3 ** i)) % 3 && Math.floor((y - 1) / (3 ** i)) % 3 == Math.floor((z - 1) / (3 ** i)) % 3) {
            continue;
        }
        if (Math.floor((x - 1) / (3 ** i)) % 3 != Math.floor((y - 1) / (3 ** i)) % 3  &&  Math.floor((y - 1) / (3 ** i)) % 3 != Math.floor((z - 1) / (3 ** i)) % 3 && Math.floor((x - 1) / (3 ** i)) % 3 != Math.floor((z - 1) / (3 ** i)) % 3) {
            continue;
        }
        return false;
    }
    return true;
}

const dummy = [];
const maxClicks = 17;

async function findAndClickSets() {
    for (let i = 0; i < numberArray.length - 2; i++) {
        for (let j = i + 1; j < numberArray.length - 1; j++) {
            for (let k = j + 1; k < numberArray.length; k++) {
                const x = numberArray[i];
                const y = numberArray[j];
                const z = numberArray[k];
                if (isSet(x, y, z)) {
                    dummy.push([x, y, z]);
                    clickTargetImage(x);
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    if (clickCounter >= maxClicks) {
                        console.log("Reached max clicks:", maxClicks);
                        return;
                    }
                    clickTargetImage(y);
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    if (clickCounter >= maxClicks) {
                        console.log("Reached max clicks:", maxClicks);
                        return;
                    }
                    clickTargetImage(z);
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    if (clickCounter >= maxClicks) {
                        console.log("Reached max clicks:", maxClicks);
                        return;
                    }
                    console.log("Found a set: ", x, y, z);
                }
            }
        }
    }
}

findAndClickSets();
console.log("Sets found:");
console.log(dummy);
