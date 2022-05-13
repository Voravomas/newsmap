import React from 'react';
import MyInput from "../UI/input/MyInput";
import MyButton from "../UI/button/MyButton";
import classes from './ArticleFilter.module.css'
import updateRegionsWithTotalArticles from "../../utils/data_manipulation";
import ArticleService from "../../API/ArticleService";
import DateInput from "../UI/dateInput/dateInput";

const ArticleFilter = ({timeConfig, setTimeConfig, totalArticles,
                           setTotalArticles, setArticles, setSelectedRegion}) => {
    function dateToTimestamp(inputDate) {
        let normalDate = inputDate;
        console.log(normalDate)
        normalDate = normalDate.split("-")
        var newDate = new Date( normalDate[0], normalDate[1] - 1, normalDate[2]);
        return newDate.getTime() / 1000;
    }

    function timestampToDate(UNIX_timestamp){
        var a = new Date(UNIX_timestamp * 1000);
        var year = a.getFullYear();
        var month = a.getMonth() + 1;
        var date = a.getDate();
        var monthZero = month < 10 ? '0' : ''
        return year + '-' + monthZero + month + '-' + date;
    }

    return (
        <div className={classes.articleFilter}>
            <p className={classes.fromToText}>From time: </p>
            <DateInput
                value={timestampToDate(timeConfig.fromTime)}
                onChange={e => {
                    setTimeConfig({...timeConfig, fromTime: dateToTimestamp(e.target.value)})
                }}
            />
            <p className={classes.fromToText}>To time: </p>
            <DateInput
                value={timestampToDate(timeConfig.toTime)}
                onChange={e => {
                    setTimeConfig({...timeConfig, toTime: dateToTimestamp(e.target.value)})
                }}
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