export default function updateRegionsWithTotalArticles(regionData, totalArticles) {
    let newRegionData = []
    for (let step = 0; step < regionData.length; step++) {
        let elm = regionData[step];
        if (totalArticles.hasOwnProperty(step + 1)) {
            elm.numArticles = totalArticles[step + 1];
        } else {
            elm.numArticles = 0;
        }
        newRegionData.push(elm);
    }
    return newRegionData;
}