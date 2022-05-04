import React from 'react';
import MyInput from "./UI/input/MyInput";
import MyButton from "./UI/button/MyButton";

const ArticleFilter = ({timeConfig, setTimeConfig, getArticlesFunction, setArticles}) => {
    return (
        <div style={{display: 'flex', justifyContent: 'space-between', flexFlow: 'row nowrap'}}>
            <p style={{marginTop: '20px'}}>From time: </p>
            <MyInput
                value={timeConfig.fromTime}
                onChange={e => setTimeConfig({...timeConfig, fromTime: e.target.value})}
            />
            <p style={{marginTop: '20px'}}>To time: </p>
            <MyInput
                value={timeConfig.toTime}
                onChange={e => setTimeConfig({...timeConfig, toTime: e.target.value})}
            />
            <MyButton onClick={async () => setArticles(await getArticlesFunction(timeConfig.fromTime, timeConfig.toTime))}>Search</MyButton>
        </div>
    );
};

export default ArticleFilter;