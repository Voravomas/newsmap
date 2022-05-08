import React from 'react';
import MyInput from "../UI/input/MyInput";
import MyButton from "../UI/button/MyButton";
import classes from './ArticleFilter.module.css'

const ArticleFilter = ({timeConfig, setTimeConfig, getArticlesFunction, setArticles}) => {
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
            <MyButton onClick={async () => setArticles(await getArticlesFunction(timeConfig.fromTime, timeConfig.toTime))}>Search</MyButton>
        </div>
    );
};

export default ArticleFilter;