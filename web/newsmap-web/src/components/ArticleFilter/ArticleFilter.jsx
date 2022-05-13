import React from 'react';
import MyInput from "../UI/input/MyInput";
import MyButton from "../UI/button/MyButton";
import classes from './ArticleFilter.module.css'
import updateRegionsWithTotalArticles from "../../utils/data_manipulation";
import ArticleService from "../../API/ArticleService";

const ArticleFilter = ({timeConfig, setTimeConfig, totalArticles,
                           setTotalArticles, setArticles, setSelectedRegion}) => {
    return (
        <div className={classes.articleFilter}>
            <p className={classes.fromToText}>From time: </p>
            <MyInput
                value={timeConfig.fromTime}
                onChange={e => setTimeConfig({...timeConfig, fromTime: e.target.value})}
            />
            <p className={classes.fromToText}>To time: </p>
            <MyInput
                value={timeConfig.toTime}
                onChange={e => setTimeConfig({...timeConfig, toTime: e.target.value})}
            />
            <MyButton onClick={async () => {
                setTotalArticles(
                    updateRegionsWithTotalArticles(totalArticles,
                        await ArticleService.getTotalArticles(timeConfig.fromTime, timeConfig.toTime)))
                setArticles([]);
                setSelectedRegion(null);
            }
            }>Search</MyButton>
        </div>
    );
};

export default ArticleFilter;