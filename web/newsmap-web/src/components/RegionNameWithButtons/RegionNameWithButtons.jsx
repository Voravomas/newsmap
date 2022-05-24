import React from 'react';
import classes from './RegionNameWithButtons.module.css'
import {DEFAULT_LIMIT, OBLAST_TO_NUM} from "../../constants";
import ArticleService from "../../API/ArticleService";
import RegionName from "../UI/RegionName/RegionName";
import NextPageButton from "../UI/NextPageButton/NextPageButton";
import PageNumber from "../UI/PageNumber/PageNumber";

const RegionNameWithButtons = ({setArticles, setRequestOffset, totalArticlesInRegion,
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

    if (selectedRegion === null) {
        return (
            <div className={classes.RegionNameWithButtons}>
                <RegionName name={"Оберіть регіон"}/>
            </div>
        )
    }

    if (totalArticlesInRegion === undefined || totalArticlesInRegion === 0) {
        return (
            <div className={classes.RegionNameWithButtons}>
                <RegionName name={OBLAST_TO_NUM[selectedRegion.toString()]}/>
            </div>
        )
    }

    return (
        <div className={classes.RegionNameWithButtons}>
            <RegionName name={OBLAST_TO_NUM[selectedRegion.toString()]}/>
            <div className={classes.PageAndArrows}>
                <NextPageButton position={"l"} onClick={async () => modifyArticles(requestOffset - DEFAULT_LIMIT)}/>
                <PageNumber totalArticlesInRegion={totalArticlesInRegion} requestOffset={requestOffset}/>
                <NextPageButton position={"r"} onClick={async () => modifyArticles(requestOffset + DEFAULT_LIMIT)}/>
            </div>
        </div>
    );
};

export default RegionNameWithButtons;