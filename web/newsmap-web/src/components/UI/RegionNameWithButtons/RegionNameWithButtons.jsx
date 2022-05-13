import React from 'react';
import classes from './RegionNameWithButtons.module.css'
import MyButton from "../button/MyButton";
import {DEFAULT_LIMIT, OBLAST_TO_NUM} from "../../../constants";
import ArticleService from "../../../API/ArticleService";

const RegionNameWithButtons = ({regionTitle, setArticles, setRequestOffset, totalArticlesInRegion,
                                   requestOffset, selectedRegion, timeConfig}) => {

    async function modifyArticles(curOffset) {
        if (curOffset < 0) {
            return;
        }
        if (curOffset >= totalArticlesInRegion) {
            return;
        }
        setRequestOffset(curOffset)
        let newArticleData = await ArticleService.getArticlesByRegion(
            timeConfig.fromTime,
            timeConfig.toTime,
            selectedRegion,
            DEFAULT_LIMIT,
            curOffset
        )
        setArticles(newArticleData);
    }

    return (
        <div className={classes.RegionNameWithButtons}>
            <MyButton onClick={async () => modifyArticles(requestOffset - DEFAULT_LIMIT)}>⬅️</MyButton>
            <h2 className={classes.h2}>
                {selectedRegion === null
                    ? "Оберіть регіон"
                    : OBLAST_TO_NUM[selectedRegion.toString()]
                }
            </h2>
            <MyButton onClick={async () => modifyArticles(requestOffset + DEFAULT_LIMIT)}>➡️</MyButton>
        </div>
    );
};

export default RegionNameWithButtons;