import {DEFAULT_LIMIT} from "../constants";

export function getCurrentPageString(curOffset, totalArticles) {
    if (curOffset === null || totalArticles === null ||
        curOffset === undefined || totalArticles === undefined) {
        return ''
    }
    let maxPage = Math.ceil(totalArticles / DEFAULT_LIMIT);
    let curPage = curOffset / DEFAULT_LIMIT + 1;
    return curPage + ' / ' + maxPage;
}