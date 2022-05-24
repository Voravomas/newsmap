import React from 'react';
import cl from './Article.module.css'
import Emoji from "../Emoji";


const Article = (props) => {
    function shortenTitle(title) {
        let localMaxStringLength = 75;
        let resStr = "";
        let titleList = title.split(" ")
        for (const word of titleList) {
            if ((resStr.length + word.length) > localMaxStringLength) {
                resStr += "..."
                break
            }
            resStr = resStr + " " + word
        }
        return resStr;
    }
    function listToString(someList) {
        let localMaxStringLength = 40;
        let resStr = "";
        for (const word of someList) {
            if ((resStr.length + word.length + 2) > localMaxStringLength) {
                resStr += "..."
                break
            }
            resStr = resStr + ", " + word
        }
        return resStr.substring(2);
    }
    function processDate(inputDate) {
        inputDate = inputDate.replace("-", ".")
        inputDate = inputDate.replace("-", ".")
        inputDate = inputDate.replace(" ", ", ")
        inputDate = inputDate.replace(":00", "")
        return inputDate
    }
    return (
        <div className={cl.article}>
            <div className={cl.articleTop}>
                <div><Emoji symbol="ℹ️"/>️ {props.article.news_provider_name}</div>
                <div><Emoji symbol="🕑"/> {processDate(props.article.time_published)}</div>
                {
                    props.article.confidence === 1
                    ? <div><b><Emoji symbol="🗺️"/> Регіон: <Emoji symbol="✅"/><span style={{'color': '#00C20B'}}> Точно</span></b></div>
                    : <div><b><Emoji symbol="🗺️"/> Регіон: <Emoji symbol="⚠️"/><span style={{'color': '#FFD218'}}> Неточно</span></b></div>
                }
            </div>
            <div className={cl.articleHeading}><a href={props.article.link} style={{textDecoration: "none", color: "inherit"}} target="_blank">{shortenTitle(props.article.title)}</a></div>
            {
                props.article.tags.length > 0
                ? <div className={cl.articleText}><b>Теги: </b>{listToString(props.article.tags)}</div>
                : <div></div>
            }
            <div className={cl.articleText}><b>Місця: </b>{listToString(props.article.places)}</div>
        </div>
    );
};

export default Article;