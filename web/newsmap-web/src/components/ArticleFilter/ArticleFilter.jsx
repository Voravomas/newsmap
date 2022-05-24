import React from 'react';
import classes from './ArticleFilter.module.css'
import updateRegionsWithTotalArticles from "../../utils/data_manipulation";
import {timestampToDate, dateToTimestamp} from "../../utils/date_manipulation";
import ArticleService from "../../API/ArticleService";
import DateInput from "../UI/DateInput/DateInput";
import SearchButton from "../UI/SearchButton/SearchButton";

const ArticleFilter = ({timeConfig, setTimeConfig, totalArticles,
                           setTotalArticles, setArticles, setSelectedRegion}) => {
    return (
        <div className={classes.articleFilter}>
            <DateInput
                value={timestampToDate(timeConfig.fromTime)}
                dateInputName={"Початок:"}
                onChange={e => {
                    setTimeConfig({...timeConfig, fromTime: dateToTimestamp(e.target.value)})
                }}
            />
            <DateInput
                value={timestampToDate(timeConfig.toTime)}
                dateInputName={"Кінець:"}
                onChange={e => {
                    setTimeConfig({...timeConfig, toTime: dateToTimestamp(e.target.value)})
                }}
            />
            <SearchButton onClick={async () => {
                setTotalArticles(
                    updateRegionsWithTotalArticles(totalArticles,
                        await ArticleService.getTotalArticles(timeConfig.fromTime, timeConfig.toTime)))
                setArticles([]);
                setSelectedRegion(null);
            }
            }>Пошук</SearchButton>
        </div>
    );
};

export default ArticleFilter;